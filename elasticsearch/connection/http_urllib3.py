import time
import ssl
import urllib3
from urllib3.exceptions import ReadTimeoutError, SSLError as UrllibSSLError
from urllib3.util.retry import Retry
import warnings

from .base import Connection
from ..exceptions import (
    ConnectionError,
    ImproperlyConfigured,
    ConnectionTimeout,
    SSLError,
)
from ..compat import urlencode

# sentinel value for `verify_certs` and `ssl_show_warn`.
# This is used to detect if a user is passing in a value
# for SSL kwargs if also using an SSLContext.
VERIFY_CERTS_DEFAULT = object()
SSL_SHOW_WARN_DEFAULT = object()

CA_CERTS = None

try:
    import certifi

    CA_CERTS = certifi.where()
except ImportError:
    pass


def create_ssl_context(**kwargs):
    """
    A helper function around creating an SSL context

    https://docs.python.org/3/library/ssl.html#context-creation

    Accepts kwargs in the same manner as `create_default_context`.
    """
    ctx = ssl.create_default_context(**kwargs)
    return ctx


class Urllib3HttpConnection(Connection):
    """
    Default connection class using the `urllib3` library and the http protocol.

    :arg host: hostname of the node (default: localhost)
    :arg port: port to use (integer, default: 9200)
    :arg url_prefix: optional url prefix for elasticsearch
    :arg timeout: default timeout in seconds (float, default: 10)
    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple
    :arg use_ssl: use ssl for the connection if `True`
    :arg verify_certs: whether to verify SSL certificates
    :arg ssl_show_warn: show warning when verify certs is disabled
    :arg ca_certs: optional path to CA bundle.
        See https://urllib3.readthedocs.io/en/latest/security.html#using-certifi-with-urllib3
        for instructions how to get default set
    :arg client_cert: path to the file containing the private key and the
        certificate, or cert only if using client_key
    :arg client_key: path to the file containing the private key if using
        separate cert and key files (client_cert will contain only the cert)
    :arg ssl_version: version of the SSL protocol to use. Choices are:
        SSLv23 (default) SSLv2 SSLv3 TLSv1 (see ``PROTOCOL_*`` constants in the
        ``ssl`` module for exact options for your environment).
    :arg ssl_assert_hostname: use hostname verification if not `False`
    :arg ssl_assert_fingerprint: verify the supplied certificate fingerprint if not `None`
    :arg maxsize: the number of connections which will be kept open to this
        host. See https://urllib3.readthedocs.io/en/1.4/pools.html#api for more
        information.
    :arg headers: any custom http headers to be add to requests
    :arg http_compress: Use gzip compression
    :arg cloud_id: The Cloud ID from ElasticCloud. Convenient way to connect to cloud instances.
        Other host connection params will be ignored.
    :arg api_key: optional API Key authentication as either base64 encoded string or a tuple.
    :arg opaque_id: Send this value in the 'X-Opaque-Id' HTTP header
        For tracing all requests made by this transport.
    """

    def __init__(
        self,
        host="localhost",
        port=None,
        http_auth=None,
        use_ssl=False,
        verify_certs=VERIFY_CERTS_DEFAULT,
        ssl_show_warn=SSL_SHOW_WARN_DEFAULT,
        ca_certs=None,
        client_cert=None,
        client_key=None,
        ssl_version=None,
        ssl_assert_hostname=None,
        ssl_assert_fingerprint=None,
        maxsize=10,
        headers=None,
        ssl_context=None,
        http_compress=None,
        cloud_id=None,
        api_key=None,
        opaque_id=None,
        **kwargs
    ):
        # Initialize headers before calling super().__init__().
        self.headers = urllib3.make_headers(keep_alive=True)

        super(Urllib3HttpConnection, self).__init__(
            host=host,
            port=port,
            use_ssl=use_ssl,
            headers=headers,
            http_compress=http_compress,
            cloud_id=cloud_id,
            api_key=api_key,
            opaque_id=opaque_id,
            **kwargs
        )
        if http_auth is not None:
            if isinstance(http_auth, (tuple, list)):
                http_auth = ":".join(http_auth)
            self.headers.update(urllib3.make_headers(basic_auth=http_auth))

        pool_class = urllib3.HTTPConnectionPool
        kw = {}

        # if providing an SSL context, raise error if any other SSL related flag is used
        if ssl_context and (
            (verify_certs is not VERIFY_CERTS_DEFAULT)
            or (ssl_show_warn is not SSL_SHOW_WARN_DEFAULT)
            or ca_certs
            or client_cert
            or client_key
            or ssl_version
        ):
            warnings.warn(
                "When using `ssl_context`, all other SSL related kwargs are ignored"
            )

        # if ssl_context provided use SSL by default
        if ssl_context and self.use_ssl:
            pool_class = urllib3.HTTPSConnectionPool
            kw.update(
                {
                    "assert_fingerprint": ssl_assert_fingerprint,
                    "ssl_context": ssl_context,
                }
            )

        elif self.use_ssl:
            pool_class = urllib3.HTTPSConnectionPool
            kw.update(
                {
                    "ssl_version": ssl_version,
                    "assert_hostname": ssl_assert_hostname,
                    "assert_fingerprint": ssl_assert_fingerprint,
                }
            )

            # Convert all sentinel values to their actual default
            # values if not using an SSLContext.
            if verify_certs is VERIFY_CERTS_DEFAULT:
                verify_certs = True
            if ssl_show_warn is SSL_SHOW_WARN_DEFAULT:
                ssl_show_warn = True

            ca_certs = CA_CERTS if ca_certs is None else ca_certs
            if verify_certs:
                if not ca_certs:
                    raise ImproperlyConfigured(
                        "Root certificates are missing for certificate "
                        "validation. Either pass them in using the ca_certs parameter or "
                        "install certifi to use it automatically."
                    )

                kw.update(
                    {
                        "cert_reqs": "CERT_REQUIRED",
                        "ca_certs": ca_certs,
                        "cert_file": client_cert,
                        "key_file": client_key,
                    }
                )
            else:
                kw["cert_reqs"] = "CERT_NONE"
                if ssl_show_warn:
                    warnings.warn(
                        "Connecting to %s using SSL with verify_certs=False is insecure."
                        % self.host
                    )
                if not ssl_show_warn:
                    urllib3.disable_warnings()

        self.pool = pool_class(
            self.hostname, port=self.port, timeout=self.timeout, maxsize=maxsize, **kw
        )

    def perform_request(
        self, method, url, params=None, body=None, timeout=None, ignore=(), headers=None
    ):
        url = self.url_prefix + url
        if params:
            url = "%s?%s" % (url, urlencode(params))
        full_url = self.host + url

        start = time.time()
        orig_body = body
        try:
            kw = {}
            if timeout:
                kw["timeout"] = timeout

            # in python2 we need to make sure the url and method are not
            # unicode. Otherwise the body will be decoded into unicode too and
            # that will fail (#133, #201).
            if not isinstance(url, str):
                url = url.encode("utf-8")
            if not isinstance(method, str):
                method = method.encode("utf-8")

            request_headers = self.headers.copy()
            request_headers.update(headers or ())

            if self.http_compress and body:
                body = self._gzip_compress(body)
                request_headers["content-encoding"] = "gzip"

            response = self.pool.urlopen(
                method, url, body, retries=Retry(False), headers=request_headers, **kw
            )
            duration = time.time() - start
            raw_data = response.data.decode("utf-8")
        except Exception as e:
            self.log_request_fail(
                method, full_url, url, orig_body, time.time() - start, exception=e
            )
            if isinstance(e, UrllibSSLError):
                raise SSLError("N/A", str(e), e)
            if isinstance(e, ReadTimeoutError):
                raise ConnectionTimeout("TIMEOUT", str(e), e)
            raise ConnectionError("N/A", str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status < 300) and response.status not in ignore:
            self.log_request_fail(
                method, full_url, url, orig_body, duration, response.status, raw_data
            )
            self._raise_error(response.status, raw_data)

        self.log_request_success(
            method, full_url, url, orig_body, response.status, raw_data, duration
        )

        return response.status, response.getheaders(), raw_data

    def close(self):
        """
        Explicitly closes connection
        """
        self.pool.close()

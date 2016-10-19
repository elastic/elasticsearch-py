import time
import warnings
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from .base import Connection
from ..exceptions import ConnectionError, ImproperlyConfigured, ConnectionTimeout, SSLError
from ..compat import urlencode, string_types

class RequestsHttpConnection(Connection):
    """
    Connection using the `requests` library.

    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple. Any value will be passed into requests as `auth`.
    :arg use_ssl: use ssl for the connection if `True`
    :arg verify_certs: whether to verify SSL certificates
    :arg ca_certs: optional path to CA bundle. By default standard requests'
        bundle will be used.
    :arg client_cert: path to the file containing the private key and the
        certificate, or cert only if using client_key
    :arg client_key: path to the file containing the private key if using
        separate cert and key files (client_cert will contain only the cert)
    :arg headers: any custom http headers to be add to requests
    """
    def __init__(self, host='localhost', port=9200, http_auth=None,
        use_ssl=False, verify_certs=True, ca_certs=None, client_cert=None,
        client_key=None, headers=None, **kwargs):
        if not REQUESTS_AVAILABLE:
            raise ImproperlyConfigured("Please install requests to use RequestsHttpConnection.")

        super(RequestsHttpConnection, self).__init__(host=host, port=port, **kwargs)
        self.session = requests.Session()
        self.session.headers = headers
        if http_auth is not None:
            if isinstance(http_auth, (tuple, list)):
                http_auth = tuple(http_auth)
            elif isinstance(http_auth, string_types):
                http_auth = tuple(http_auth.split(':', 1))
            self.session.auth = http_auth
        self.base_url = 'http%s://%s:%d%s' % (
            's' if use_ssl else '',
            host, port, self.url_prefix
        )
        self.session.verify = verify_certs
        if not client_key:
            self.session.cert = client_cert
        elif client_cert:
            # cert is a tuple of (certfile, keyfile)
            self.session.cert = (client_cert, client_key)
        if ca_certs:
            if not verify_certs:
                raise ImproperlyConfigured("You cannot pass CA certificates when verify SSL is off.")
            self.session.verify = ca_certs

        if use_ssl and not verify_certs:
            warnings.warn(
                'Connecting to %s using SSL with verify_certs=False is insecure.' % self.base_url)

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        url = self.base_url + url
        if params:
            url = '%s?%s' % (url, urlencode(params or {}))

        start = time.time()
        try:
            response = self.session.request(method, url, data=body, timeout=timeout or self.timeout)
            duration = time.time() - start
            raw_data = response.text
        except requests.exceptions.SSLError as e:
            self.log_request_fail(method, url, response.request.path_url, body, time.time() - start, exception=e)
            raise SSLError('N/A', str(e), e)
        except requests.Timeout as e:
            self.log_request_fail(method, url, response.request.path_url, body, time.time() - start, exception=e)
            raise ConnectionTimeout('TIMEOUT', str(e), e)
        except requests.ConnectionError as e:
            self.log_request_fail(method, url, response.request.path_url, body, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status_code < 300) and response.status_code not in ignore:
            self.log_request_fail(method, url, response.request.path_url, body, duration, response.status_code, raw_data)
            self._raise_error(response.status_code, raw_data)

        self.log_request_success(method, url, response.request.path_url, body, response.status_code, raw_data, duration)

        return response.status_code, response.headers, raw_data

    def close(self):
        """
        Explicitly closes connections
        """
        self.session.close()

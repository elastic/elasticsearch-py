import asyncio
import ssl
import os
import warnings

import aiohttp
import yarl
from aiohttp.client_exceptions import ServerFingerprintMismatch

from ..connection import Connection
from ..compat import urlencode
from ..exceptions import (
    ConnectionError,
    ConnectionTimeout,
    ImproperlyConfigured,
    SSLError,
)


# sentinel value for `verify_certs`.
# This is used to detect if a user is passing in a value
# for SSL kwargs if also using an SSLContext.
VERIFY_CERTS_DEFAULT = object()

CA_CERTS = None

try:
    import certifi

    CA_CERTS = certifi.where()
except ImportError:
    pass


class AIOHttpConnection(Connection):
    def __init__(
        self,
        host="localhost",
        port=None,
        http_auth=None,
        use_ssl=False,
        verify_certs=True,
        ca_certs=None,
        client_cert=None,
        client_key=None,
        ssl_version=None,
        ssl_assert_fingerprint=None,
        maxsize=10,
        headers=None,
        ssl_context=None,
        http_compress=None,
        cloud_id=None,
        api_key=None,
        opaque_id=None,
        loop=None,
        **kwargs,
    ):
        self.headers = {}

        super().__init__(
            host=host,
            port=port,
            use_ssl=use_ssl,
            headers=headers,
            http_compress=http_compress,
            cloud_id=cloud_id,
            api_key=api_key,
            opaque_id=opaque_id,
            **kwargs,
        )

        if http_auth is not None:
            if isinstance(http_auth, str):
                http_auth = tuple(http_auth.split(":", 1))

            if isinstance(http_auth, (tuple, list)):
                http_auth = aiohttp.BasicAuth(*http_auth)

        # if providing an SSL context, raise error if any other SSL related flag is used
        if ssl_context and (
            (verify_certs is not VERIFY_CERTS_DEFAULT)
            or ca_certs
            or client_cert
            or client_key
            or ssl_version
        ):
            warnings.warn(
                "When using `ssl_context`, all other SSL related kwargs are ignored"
            )

        self.ssl_assert_fingerprint = ssl_assert_fingerprint
        if self.use_ssl and ssl_context is None:
            ssl_context = ssl.SSLContext(ssl_version or ssl.PROTOCOL_TLS)

            # Convert all sentinel values to their actual default
            # values if not using an SSLContext.
            if verify_certs is VERIFY_CERTS_DEFAULT:
                verify_certs = True

            ca_certs = CA_CERTS if ca_certs is None else ca_certs
            if verify_certs:
                if not ca_certs:
                    raise ImproperlyConfigured(
                        "Root certificates are missing for certificate "
                        "validation. Either pass them in using the ca_certs parameter or "
                        "install certifi to use it automatically."
                    )
            if os.path.isfile(ca_certs):
                ssl_context.load_verify_locations(cafile=ca_certs)
            elif os.path.isdir(ca_certs):
                ssl_context.load_verify_locations(capath=ca_certs)
            else:
                raise ImproperlyConfigured("ca_certs parameter is not a path")

        self.headers.setdefault("connection", "keep-alive")
        self.loop = loop
        self.session = None

        # Parameters for creating an aiohttp.ClientSession later.
        self._limit = maxsize
        self._http_auth = http_auth
        self._verify_certs = verify_certs
        self._ssl_context = ssl_context

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def perform_request(
        self, method, url, params=None, body=None, timeout=None, ignore=(), headers=None
    ):
        if self.session is None:
            self._create_aiohttp_session()

        url_path = url
        if params:
            query_string = urlencode(params)
        else:
            query_string = ""

        # Provide correct URL object to avoid string parsing in low-level code
        url = yarl.URL.build(
            scheme=self.scheme,
            host=self.hostname,
            port=self.port,
            path=url,
            query_string=query_string,
            encoded=True,
        )

        timeout = aiohttp.ClientTimeout(
            total=timeout if timeout is not None else self.timeout
        )

        if headers:
            req_headers = self.headers.copy()
            req_headers.update(headers)
        else:
            req_headers = self.headers

        start = self.loop.time()
        try:
            async with self.session.request(
                method,
                url,
                data=body,
                headers=req_headers,
                timeout=timeout,
                fingerprint=self.ssl_assert_fingerprint,
            ) as response:
                raw_data = await response.text()
                duration = self.loop.time() - start

        # We want to reraise a cancellation.
        except asyncio.CancelledError:
            raise

        except Exception as e:
            self.log_request_fail(
                method, url, url_path, body, self.loop.time() - start, exception=e
            )
            if isinstance(e, ServerFingerprintMismatch):
                raise SSLError("N/A", str(e), e)
            if isinstance(e, asyncio.TimeoutError):
                raise ConnectionTimeout("TIMEOUT", str(e), e)
            raise ConnectionError("N/A", str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status < 300) and response.status not in ignore:
            self.log_request_fail(
                method,
                url,
                url_path,
                body,
                duration,
                status_code=response.status,
                response=raw_data,
            )
            self._raise_error(response.status, raw_data)

        self.log_request_success(
            method, url, url_path, body, response.status, raw_data, duration
        )

        return response.status, response.headers, raw_data

    def _create_aiohttp_session(self):
        """Creates an aiohttp.ClientSession(). This is delayed until
        the first call to perform_request() so that AsyncTransport has
        a chance to set AIOHttpConnection.loop
        """
        self.session = aiohttp.ClientSession(
            auth=self._http_auth,
            headers=self.headers,
            auto_decompress=True,
            loop=self.loop,
            connector=aiohttp.TCPConnector(
                limit=self._limit,
                verify_ssl=self._verify_certs,
                use_dns_cache=True,
                ssl_context=self._ssl_context,
            ),
        )

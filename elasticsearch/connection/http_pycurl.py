import os
import time
from io import BytesIO
from threading import Semaphore
import urllib3
from collections import deque
from .base import Connection
from ..exceptions import ImproperlyConfigured
from ..compat import urlencode


try:
    import pycurl

    PYCURL_AVAILABLE = True
except ImportError:
    PYCURL_AVAILABLE = False


class PyCurlHttpConnection(Connection):
    def __init__(
        self,
        host="localhost",
        port=None,
        http_auth=None,
        use_ssl=False,
        verify_certs=True,
        ssl_show_warn=True,
        ca_certs=None,
        client_cert=None,
        client_key=None,
        maxsize=10,
        headers=None,
        http_compress=None,
        cloud_id=None,
        api_key=None,
        opaque_id=None,
        **kwargs
    ):
        if not PYCURL_AVAILABLE:
            raise ImproperlyConfigured(
                "Please install pycurl to use PyCurlHttpConnection."
            )

        self.headers = {}
        self.verify_certs = verify_certs
        self.ssl_show_warn = ssl_show_warn
        self.ca_certs = ca_certs
        self.client_cert = client_cert
        self.client_key = client_key

        if http_auth is not None:
            if isinstance(http_auth, (tuple, list)):
                http_auth = ":".join(http_auth)
            self.headers.update(urllib3.make_headers(basic_auth=http_auth))

        super(PyCurlHttpConnection, self).__init__(
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

        # Default headers
        self.headers.setdefault("connection", "keep-alive")
        self.headers.setdefault("user-agent", self._get_default_user_agent())
        self.headers.setdefault("accept", "*/*")
        self.headers.pop("accept-encoding", None)

        self._semaphore = Semaphore(maxsize)
        self._handles = deque()

    def get_handle(self):
        self._semaphore.acquire()
        try:
            handle = self._handles.pop()
        except IndexError:
            handle = None

        if handle is None:
            handle = pycurl.Curl()
            if self.http_compress:
                handle.setopt(pycurl.ACCEPT_ENCODING, "gzip")
            handle.setopt(pycurl.FOLLOWLOCATION, 1)
            handle.setopt(pycurl.MAXREDIRS, 10)
            if self.use_ssl:
                handle.setopt(pycurl.SSL_VERIFYHOST, 2 if self.verify_certs else 0)
                handle.setopt(pycurl.SSL_VERIFYPEER, 1 if self.verify_certs else 0)
                if self.client_cert:
                    handle.setopt(pycurl.SSLCERT, self.client_cert)
                if self.client_key:
                    handle.setopt(pycurl.SSLKEY, self.client_key)
                if self.ca_certs:
                    if os.path.isdir(self.ca_certs):
                        handle.setopt(pycurl.CAPATH, self.ca_certs)
                    else:
                        handle.setopt(pycurl.CAINFO, self.ca_certs)
        return handle

    def put_handle(self, handle):
        self._handles.append(handle)
        self._semaphore.release()

    def perform_request(
        self, method, url, params=None, body=None, timeout=None, ignore=(), headers=None
    ):
        url = self.url_prefix + url
        if params:
            url = "%s?%s" % (url, urlencode(params))
        full_url = self.host + url

        orig_body = body
        start = time.time()
        resp_headers = {}

        def write_resp_header(header):
            # Filters out the leading status line
            key, delim, value = header.partition(b":")
            if not delim:
                return
            key = key.strip()
            if key:  # Filters out the trailing '\r\n'
                resp_headers[key.decode().lower()] = value.strip().decode()

        curl = self.get_handle()
        try:
            # HTTP options
            curl.setopt(pycurl.URL, full_url)
            curl.setopt(pycurl.CUSTOMREQUEST, method)
            curl.setopt(pycurl.HEADERFUNCTION, write_resp_header)

            req_headers = self.headers.copy()
            if headers:
                req_headers.update(headers)

            # Timeout options
            if timeout is not None:
                curl.setopt(pycurl.CONNECTTIMEOUT, timeout)
                curl.setopt(pycurl.TIMEOUT, timeout)
            else:
                curl.setopt(pycurl.TIMEOUT, 10)

            # Body options
            if body:
                curl.setopt(pycurl.UPLOAD, 1)
                if self.http_compress and body:
                    body = self._gzip_compress(body)
                    req_headers["content-encoding"] = "gzip"
                req_buf = BytesIO(body)
                curl.setopt(pycurl.READDATA, req_buf)
            else:
                curl.setopt(pycurl.UPLOAD, 0)

            curl.setopt(
                pycurl.HTTPHEADER, ["%s: %s" % kv for kv in req_headers.items()]
            )
            resp_body = curl.perform_rb()
            status_code = curl.getinfo(pycurl.RESPONSE_CODE)
            duration = time.time() - start

            # raise errors based on http status codes, let the client handle those if needed
            if not (200 <= status_code < 300) and status_code not in ignore:
                self.log_request_fail(
                    method, full_url, url, orig_body, duration, status_code, resp_body
                )
                self._raise_error(status_code, resp_body)

            self.log_request_success(
                method, full_url, url, orig_body, status_code, resp_body, duration
            )
        finally:
            self.put_handle(curl)

        return status_code, resp_headers, resp_body

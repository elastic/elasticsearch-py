from io import BytesIO
from .base import Connection
from ..exceptions import (
    ConnectionError,
    ImproperlyConfigured,
    ConnectionTimeout,
    SSLError,
)
from ..compat import urlencode, string_types


try:
    import pycurl

    PYCURL_AVAILABLE = True
except ImportError:
    PYCURL_AVAILABLE = False


class PyCurlHttpConnection(Connection):
    def __init__(
        self,
        host="localhost",
        port=9200,
        http_auth=None,
        use_ssl=False,
        verify_certs=True,
        ssl_show_warn=True,
        ca_certs=None,
        client_cert=None,
        client_key=None,
        headers=None,
        http_compress=False,
        cloud_id=None,
        api_key=None,
        **kwargs
    ):
        if not PYCURL_AVAILABLE:
            raise ImproperlyConfigured(
                "Please install pycurl to use RequestsHttpConnection."
            )

        super(PyCurlHttpConnection, self).__init__(
            host=host,
            port=port,
            use_ssl=use_ssl,
            **kwargs
        )

    def perform_request(
        self, method, url, params=None, body=None, timeout=None, ignore=(), headers=None
    ):
        url = self.url_prefix + url
        if params:
            url = "%s?%s" % (url, urlencode(params))
        full_url = self.host + url

        resp_buf = BytesIO()
        resp_headers = {}

        def write_resp_header(header):
            key, _, value = header.partition(":")
            resp_headers[key] = value.strip()

        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, full_url)
        curl.setopt(pycurl.CUSTOMREQUEST, method)
        curl.setopt(pycurl.HTTPHEADER, ["%s: %s" % kv for kv in headers.items()])
        curl.setopt(pycurl.WRITEFUNCTION, resp_buf.write)
        curl.setopt(pycurl.WRITEHEADER, write_resp_header)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)

        if timeout is not None:
            curl.setopt(pycurl.CONNECTTIMEOUT, timeout)
            curl.setopt(pycurl.TIMEOUT, timeout)
        if body:
            req_buf = BytesIO(body)
            curl.setopt(pycurl.READDATA, req_buf)

        curl.perform()
        status_code = curl.getinfo(pycurl.RESPONSE_CODE)
        return status_code, resp_headers, resp_buf.getvalue()

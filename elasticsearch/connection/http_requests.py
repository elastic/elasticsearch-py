import time
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from .base import Connection
from ..exceptions import ConnectionError, ImproperlyConfigured, ConnectionTimeout
from ..compat import urlencode

class RequestsHttpConnection(Connection):
    """
    Connection using the `requests` library.

    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple
    :arg use_ssl: use ssl for the connection if `True`
    """
    def __init__(self, host='localhost', port=9200, http_auth=None, use_ssl=False, **kwargs):
        if not REQUESTS_AVAILABLE:
            raise ImproperlyConfigured("Please install requests to use RequestsHttpConnection.")

        super(RequestsHttpConnection, self).__init__(host= host, port=port, **kwargs)
        self.session = requests.session()
        if http_auth is not None:
            if not isinstance(http_auth, (tuple, list)):
                http_auth = http_auth.split(':', 1)
            http_auth = tuple(http_auth)
            self.session.auth = http_auth
        self.base_url = 'http%s://%s:%d%s' % (
            's' if use_ssl else '',
            host, port, self.url_prefix
        )


    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        url = self.base_url + url
        if params:
            url = '%s?%s' % (url, urlencode(params or {}))

        start = time.time()
        try:
            response = self.session.request(method, url, data=body, timeout=timeout or self.timeout)
            duration = time.time() - start
            raw_data = response.text
        except requests.Timeout as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise ConnectionTimeout('TIMEOUT', str(e), e)
        except requests.ConnectionError as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status_code < 300) and response.status_code not in ignore:
            self.log_request_fail(method, url, body, duration, response.status_code)
            self._raise_error(response.status_code, raw_data)

        self.log_request_success(method, url, response.request.path_url, body, response.status_code, raw_data, duration)

        return response.status_code, response.headers, raw_data

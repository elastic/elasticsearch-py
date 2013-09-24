import time
import requests
import urllib3
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .base import Connection
from ..exceptions import ConnectionError

class RequestsHttpConnection(Connection):
    """
    Connection using the `requests` library.

    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple
    """
    def __init__(self, host='localhost', port=9200, http_auth=None, **kwargs):
        super(RequestsHttpConnection, self).__init__(host=host, port=port, **kwargs)
        self.session = requests.session()
        if http_auth is not None: 
            if not isinstance(http_auth, tuple):
                http_auth = tuple(http_auth.split(':', 1))
            self.session.auth = http_auth


    def perform_request(self, method, url, params=None, body=None, timeout=None):
        url = self.host + self.url_prefix + url

        # use prepared requests so that requests formats url and params for us to log
        request = requests.Request(method, url, params=params or {}, data=body).prepare()
        start = time.time()
        try:
            response = self.session.send(request, timeout=timeout or self.timeout)
            duration = time.time() - start
            raw_data = response.text
        except (requests.ConnectionError, requests.Timeout) as e:
            self.log_request_fail(method, request.url, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status_code < 300):
            self.log_request_fail(method, request.url, duration, response.status_code)
            self._raise_error(response.status_code, raw_data)

        self.log_request_success(method, request.url, request.path_url, body, response.status_code, raw_data, duration)

        return response.status_code, raw_data

class Urllib3HttpConnection(Connection):
    """
    Default connection class using the `urllib3` library and the http protocol.

    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple
    """
    def __init__(self, host='localhost', port=9200, http_auth=None, **kwargs):
        super(Urllib3HttpConnection, self).__init__(host=host, port=port, **kwargs)
        headers = {}
        if http_auth is not None:
            if isinstance(http_auth, (tuple, list)):
                http_auth = ':'.join(http_auth)
            headers = urllib3.make_headers(basic_auth=http_auth)

        self.pool = urllib3.HTTPConnectionPool(host, port=port, timeout=kwargs.get('timeout', None), headers=headers)

    def perform_request(self, method, url, params=None, body=None, timeout=None):
        url = self.url_prefix + url
        if params:
            url = '%s?%s' % (url, urlencode(params or {}))
        full_url = self.host + url

        start = time.time()
        try:
            kw = {}
            if timeout:
                kw['timeout'] = timeout
            response = self.pool.urlopen(method, url, body, **kw)
            duration = time.time() - start
            raw_data = response.data.decode('utf-8')
        except Exception as e:
            self.log_request_fail(method, full_url, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        if not (200 <= response.status < 300):
            self.log_request_fail(method, url, duration, response.status)
            self._raise_error(response.status, raw_data)

        self.log_request_success(method, full_url, url, body, response.status,
            raw_data, duration)

        return response.status, raw_data



import time
import urllib3
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .base import Connection
from ..exceptions import ConnectionError

class Urllib3HttpConnection(Connection):
    """
    Default connection class using the `urllib3` library and the http protocol.

    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple
    :arg use_ssl: use ssl for the connection if `True`
    :arg maxsize: the maximum number of connections which will be kept open to
        this host.  Useful to set this higher than 1 for multithreaded situations.
    """
    def __init__(self, host='localhost', port=9200, http_auth=None, use_ssl=False, maxsize=1, **kwargs):
        super(Urllib3HttpConnection, self).__init__(host=host, port=port, **kwargs)
        headers = {}
        if http_auth is not None:
            if isinstance(http_auth, (tuple, list)):
                http_auth = ':'.join(http_auth)
            headers = urllib3.make_headers(basic_auth=http_auth)

        pool_class = urllib3.HTTPConnectionPool
        if use_ssl:
            pool_class = urllib3.HTTPSConnectionPool

        self.pool = pool_class(host, port=port, timeout=kwargs.get('timeout', None), headers=headers, maxsize=maxsize)

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
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

        if not (200 <= response.status < 300) and response.status not in ignore:
            self.log_request_fail(method, url, duration, response.status)
            self._raise_error(response.status, raw_data)

        self.log_request_success(method, full_url, url, body, response.status,
            raw_data, duration)

        return response.status, raw_data




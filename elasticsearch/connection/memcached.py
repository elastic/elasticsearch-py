import time
import json
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ..exceptions import TransportError, ConnectionError, ImproperlyConfigured
from .pooling import PoolingConnection

class MemcachedConnection(PoolingConnection):
    """
    Client using the `pylibmc` python library to communicate with elasticsearch
    using the memcached protocol. Requires plugin in the cluster.

    See https://github.com/elasticsearch/elasticsearch-transport-memcached for more details.
    """
    transport_schema = 'memcached'

    method_map = {
        'PUT': 'set',
        'POST': 'set',
        'DELETE': 'delete',
        'HEAD': 'get',
        'GET': 'get',
    }

    def __init__(self, host='localhost', port=11211, **kwargs):
        try:
            import pylibmc
        except ImportError:
            raise ImproperlyConfigured("You need to install pylibmc to use the MemcachedConnection class.")
        super(MemcachedConnection, self).__init__(host=host, port=port, **kwargs)
        self._make_connection = lambda: pylibmc.Client(['%s:%s' % (host, port)], behaviors={"tcp_nodelay": True})

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        mc = self._get_connection()
        url = self.url_prefix + url
        if params:
            url = '%s?%s' % (url, urlencode(params or {}))
        full_url = self.host + url

        mc_method = self.method_map.get(method, 'get')

        start = time.time()
        try:
            status = 200
            if mc_method == 'set':
                # no response from set commands
                response = ''
                if not json.dumps(mc.set(url, body)):
                    status = 500
            else:
                response = mc.get(url)

            duration = time.time() - start
            if response:
                response = response.decode('utf-8')
        except Exception as e:
            self.log_request_fail(method, full_url, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)
        finally:
            self._release_connection(mc)

        # try not to load the json every time
        if response and response[0] == '{' and ('"status"' in response or '"error"' in response):
            data = json.loads(response)
            if 'status' in data:
                status = data['status']
            elif 'error' in data:
                raise TransportError('N/A', data['error'])

        if not (200 <= status < 300) and status not in ignore:
            self.log_request_fail(method, url, duration, status)
            self._raise_error(status, response)

        self.log_request_success(method, full_url, url, body, status,
            response, duration)

        return status, response




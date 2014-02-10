import time
import json
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from ..exceptions import TransportError, ConnectionError, ImproperlyConfigured
from .pooling import PoolingConnection

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

if REDIS_AVAILABLE:
    class ElasticsearchRedis(redis.Redis):
        """
        Override to disable parse response so set command can return JSON result
        """
        def parse_response(self, connection, command_name, **options):
            response = connection.read_response()
            return response


class RedisConnection(PoolingConnection):
    """
    Client using the `redis-py` python library to communicate with elasticsearch
    using the redis protocol. Requires plugin in the cluster.

    See https://github.com/kzwang/elasticsearch-transport-redis
    """
    transport_schema = 'redis'

    method_map = {
        'PUT': 'SET',
        'POST': 'SET',
        'DELETE': 'DEL',
        'HEAD': 'EXISTS',
        'GET': 'GET',
    }

    def __init__(self, host='localhost', port=6379, **kwargs):
        if not REDIS_AVAILABLE:
            raise ImproperlyConfigured("You need to install redis-py to use the RedisConnection class.")
        port = int(port)
        super(RedisConnection, self).__init__(host=host, port=port, **kwargs)
        self._make_connection = lambda: ElasticsearchRedis(host=host, port=port)

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        r = self._get_connection()
        url = self.url_prefix + url
        if params:
            url = '%s?%s' % (url, urlencode(params or {}))
        full_url = self.host + url

        redis_method = self.method_map.get(method, 'GET')

        start = time.time()
        response = ""
        try:
            status = 200
            commands = list()
            commands.append(redis_method)
            commands.append(url)
            if body:
                if isinstance(body, dict):
                    body = json.dumps(body)
                if method == 'PUT':
                    body = 'PUT' + body
                commands.append(body)

            response = str(r.execute_command(*commands))

            if redis_method == 'DEL':  # DELETE may return JSON or 1/0 depends on setting
                if response == '0':
                    status = 500  # has error
                if not response[0] == '{':  # not JSON, don't return
                    response = ""
            elif redis_method == 'SET':  # SET may return JSON or OK/Error depends on setting
                if response == 'Error':
                    status = 500  # has error
                if not response[0] == '{':  # not JSON, don't return
                    response = ""
            elif redis_method == "EXISTS":
                # exists will return 0 for fail and one for success
                if response == "0":
                    status = 404  # not found

            duration = time.time() - start
        except redis.exceptions.ResponseError as e:
            status = 500
            duration = time.time() - start
        except Exception as e:
            self.log_request_fail(method, full_url, body, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)
        finally:
            self._release_connection(r)

        # try not to load the json every time
        if response and response[0] == '{' and ('"status"' in response or '"error"' in response):
            data = json.loads(response)
            if 'status' in data and isinstance(data['status'], int):
                status = data['status']
            elif 'error' in data:
                raise TransportError('N/A', data['error'])

        if not (200 <= status < 300) and status not in ignore:
            self.log_request_fail(method, url, body, duration, status)
            self._raise_error(status, response)

        self.log_request_success(method, full_url, url, body, status, response, duration)

        return status, {}, response


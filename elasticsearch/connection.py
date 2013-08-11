import logging
import time
import requests
import json
import urllib3
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .exceptions import TransportError, HTTP_EXCEPTIONS, ConnectionError

logger = logging.getLogger('elasticsearch')
tracer = logging.getLogger('elasticsearch.trace')
tracer.propagate = False

class Connection(object):
    """
    Class responsible for maintaining a connection to an Elasticsearch node. It
    holds persistent connection pool to it and it's main interface
    (`perform_request`) is thread-safe.

    Also responsible for logging.
    """
    transport_schema = 'http'

    def __init__(self, host='localhost', port=9200, url_prefix='', timeout=10, **kwargs):
        """
        :arg host: hostname of the node (default: localhost)
        :arg port: port to use (default: 9200)
        :arg url_prefix: optional url prefix for elasticsearch
        :arg timeout: default timeout in seconds (default: 10)
        """
        self.host = '%s://%s:%s' % (self.transport_schema, host, port)
        if url_prefix:
            url_prefix = '/' + url_prefix.strip('/')
        self.url_prefix = url_prefix
        self.timeout = 10

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.host)

    def log_request_success(self, method, full_url, path, body, status_code, response, duration):
        """ Log a successful API call.  """
        def _pretty_json(data):
            # pretty JSON in tracer curl logs
            try:
                return json.dumps(json.loads(data), sort_keys=True, indent=2, separators=(',', ': '))
            except (ValueError, TypeError):
                # non-json data or a bulk request
                return repr(data)

        logger.info(
            '%s %s [status:%s request:%.3fs]', method, full_url,
            status_code, duration
        )
        logger.debug('> %s', body)
        logger.debug('< %s', response)

        if tracer.isEnabledFor(logging.INFO):
            # include pretty in trace curls
            path = path.replace('?', '?pretty&', 1) if '?' in path else path + '?pretty'
            if self.url_prefix:
                path = path.replace(self.url_prefix, '', 1)
            tracer.info("curl -X%s 'http://localhost:9200%s' -d '%s'", method, path, _pretty_json(body) if body else '')

        if tracer.isEnabledFor(logging.DEBUG):
            tracer.debug('# [%s] (%.3fs)\n#%s', status_code, duration, _pretty_json(response).replace('\n', '\n#') if response else '')

    def log_request_fail(self, method, full_url, duration, status_code=None, exception=None):
        """ Log an unsuccessful API call.  """
        logger.warning(
            '%s %s [status:%s request:%.3fs]', method, full_url,
            status_code or 'N/A', duration, exc_info=exception is not None
        )

    def _raise_error(self, status_code, raw_data):
        """ Locate appropriate exception and raise it. """
        error_message = raw_data
        additional_info = None
        try:
            additional_info = json.loads(raw_data)
            error_message = additional_info.get('error', error_message)
        except:
            # we don't care what went wrong
            pass

        raise HTTP_EXCEPTIONS.get(status_code, TransportError)(status_code, error_message, additional_info)


class RequestsHttpConnection(Connection):
    """ Connection using the `requests` library. """
    def __init__(self, **kwargs):
        super(RequestsHttpConnection, self).__init__(**kwargs)
        self.session = requests.session()

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
    def __init__(self, host='localhost', port=9200, **kwargs):
        super(Urllib3HttpConnection, self).__init__(host=host, port=port, **kwargs)
        self.pool = urllib3.HTTPConnectionPool(host, port=port, timeout=kwargs.get('timeout', None))

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

class MemcachedConnection(Connection):
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
        self.mc = pylibmc.Client(['%s:%s' % (host, port)],behaviors={"tcp_nodelay": True})

    def perform_request(self, method, url, params=None, body=None, timeout=None):
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
                if not json.dumps(self.mc.set(url, body)):
                    status = 500
            else:
                response = self.mc.get(url)

            duration = time.time() - start
            if response:
                response = response.decode('utf-8')
        except Exception as e:
            self.log_request_fail(method, full_url, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        # try not to load the json every time
        if response and response[0] == '{' and ('"status"' in response or '"error"' in response):
            data = json.loads(response)
            if 'status' in data:
                status = data['status']
            elif 'error' in data:
                raise TransportError('N/A', data['error'])

        if not (200 <= status < 300):
            self.log_request_fail(method, url, duration, status)
            self._raise_error(status, response)

        self.log_request_success(method, full_url, url, body, status,
            response, duration)

        return status, response

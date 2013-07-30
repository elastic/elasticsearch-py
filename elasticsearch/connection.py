import logging
import time
import requests
import json

from .exceptions import TransportError, HTTP_EXCEPTIONS, ConnectionError

logger = logging.getLogger('elasticsearch')
tracer = logging.getLogger('elasticsearch.trace')
tracer.propagate = False

class Connection(object):
    transport_schema = 'http'

    def __init__(self, host='localhost', port=9200, url_prefix='', timeout=10, **kwargs):
        self.host = '%s://%s:%s' % (self.transport_schema, host, port)
        if url_prefix:
            url_prefix = '/' + url_prefix.strip('/')
        self.url_prefix = url_prefix
        self.timeout = 10

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.host)

    def log_request_success(self, method, full_url, path, body, status_code, response, duration):
        def _pretty_json(data):
            # pretty JSON in tracer curl logs
            try:
                data = json.dumps(json.loads(data), sort_keys=True, indent=2, separators=(',', ': '))
            except ValueError:
                # non-json data or a bulk request
                pass
            return data

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
        logger.warning(
            '%s %s [status:%s request:%.3fs]', method, full_url,
            status_code or 'N/A', duration, exc_info=exception is not None
        )

    def _raise_error(self, status_code, raw_data):
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


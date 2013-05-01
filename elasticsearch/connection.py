import logging
import time
import requests
import json

from .exceptions import TransportError, HTTP_EXCEPTIONS

logger = logging.getLogger('elasticsearch')
tracer = logging.getLogger('elasticsearch.trace')
tracer.propagate = False

class Connection(object):
    transport_schema = 'http'

    def __init__(self, host='localhost', port=9200, **kwargs):
        self.host = '%s://%s:%s' % (self.transport_schema, host, port)

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self.host)


class RequestsHttpConnection(Connection):
    def __init__(self, **kwargs):
        super(RequestsHttpConnection, self).__init__(**kwargs)
        self.session = requests.session()

    def perform_request(self, method, url, params=None, body=None):
        url = self.host + url

        request = requests.Request(method, url, params=params or {}, data=body).prepare()
        try:
            response = self.session.send(request)
            raw_data = response.text
        except requests.ConnectionError as e:
            raise TransportError(e)

        # raise errors based on http status codes, let the client handle those if needed
        if response.status_code >= 300:

            if response.status_code in HTTP_EXCEPTIONS:
                raise HTTP_EXCEPTIONS[response.status_code]()

            raise TransportError()

        return response.status_code, raw_data


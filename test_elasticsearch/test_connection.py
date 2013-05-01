from unittest import TestCase

from mock import Mock

from elasticsearch.connection import RequestsHttpConnection

class TestRequestsConnection(TestCase):
    def _get_mock_connection(self, connection_params={}, status_code=200, response_body=u'{}'):
        con = RequestsHttpConnection(**connection_params)

        con.session.send = Mock()

        dummy_response = Mock()
        con.session.send.return_value = dummy_response
        dummy_response.status_code = status_code
        dummy_response.text = response_body
        return con

    def _get_request(self, connection, *args, **kwargs):
        status, data = connection.perform_request(*args, **kwargs)
        self.assertEquals(200, status)
        self.assertEquals(u'{}', data)

        self.assertEquals(1, connection.session.send.call_count)

        args, kwargs = connection.session.send.call_args
        self.assertEquals({}, kwargs)
        self.assertEquals(1, len(args))
        return args[0]

    def test_defaults(self):
        con = self._get_mock_connection()
        request = self._get_request(con, 'GET', '/')

        self.assertEquals('http://localhost:9200/', request.url)
        self.assertEquals('GET', request.method)
        self.assertEquals(None, request.body)

    def test_params_properly_encoded(self):
        con = self._get_mock_connection()
        request = self._get_request(con, 'GET', '/', params={'param': 'value with spaces'})

        self.assertEquals('http://localhost:9200/?param=value+with+spaces', request.url)
        self.assertEquals('GET', request.method)
        self.assertEquals(None, request.body)

    def test_body_attached(self):
        con = self._get_mock_connection()
        request = self._get_request(con, 'GET', '/', body='{"answer": 42}')

        self.assertEquals('http://localhost:9200/', request.url)
        self.assertEquals('GET', request.method)
        self.assertEquals('{"answer": 42}', request.body)

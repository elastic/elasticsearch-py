from unittest import TestCase

from mock import Mock, patch

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


    @patch('elasticsearch.connection.tracer')
    @patch('elasticsearch.connection.logger')
    def test_success_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(response_body='{"answer": 42}')
        status, data = con.perform_request('GET', '/', {'param': 42}, '{}')

        # trace request
        self.assertEquals(1, tracer.info.call_count)
        self.assertEquals(
            "curl -XGET 'http://localhost:9200/?pretty&param=42' -d '{}'",
            tracer.info.call_args[0][0] % tracer.info.call_args[0][1:]
        )
        # trace response
        self.assertEquals(1, tracer.debug.call_count)
        self.assertEquals(
            '# [200] (0.000s)\n#{\n#  "answer": 42\n#}',
            tracer.debug.call_args[0][0] % tracer.debug.call_args[0][1:]
        )

        # log url and duration
        self.assertEquals(1, logger.info.call_count)
        self.assertEquals(
            'GET http://localhost:9200/?param=42 [status:200 request:0.000s]',
            logger.info.call_args[0][0] % logger.info.call_args[0][1:]
        )
        # log request body and response
        self.assertEquals(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list
        self.assertEquals(
            '> {}',
            req[0][0] % req[0][1:]
        )
        self.assertEquals(
            '< {"answer": 42}',
            resp[0][0] % resp[0][1:]
        )

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

import re
from mock import Mock, patch
import urllib3

from elasticsearch.exceptions import TransportError, ConflictError, RequestError, NotFoundError
from elasticsearch.connection import RequestsHttpConnection, \
    Urllib3HttpConnection, THRIFT_AVAILABLE, ThriftConnection, \
    THRIFTPY_AVAILABLE, ThriftpyConnection

from .test_cases import TestCase, SkipTest


class TestThriftConnection(TestCase):
    def setUp(self):
        if not THRIFT_AVAILABLE:
            raise SkipTest('Thrift is not available.')
        super(TestThriftConnection, self).setUp()

    def test_use_ssl_uses_ssl_socket(self):
        from thrift.transport import TSSLSocket
        con = ThriftConnection(use_ssl=True)
        self.assertIs(con._tsocket_class, TSSLSocket.TSSLSocket)

    def test_use_normal_tsocket_by_default(self):
        from thrift.transport import TSocket
        con = ThriftConnection()
        self.assertIs(con._tsocket_class, TSocket.TSocket)

    def test_timeout_set(self):
        con = ThriftConnection(timeout=42)
        self.assertEquals(42, con.timeout)


class TestThriftpyConnection(TestCase):
    def setUp(self):
        if not THRIFTPY_AVAILABLE:
            raise SkipTest('Thriftpy is not available.')
        super(TestThriftpyConnection, self).setUp()

    def test_timeout_set(self):
        con = ThriftpyConnection(timeout=42)
        self.assertEquals(42, con.timeout)


class TestUrllib3Connection(TestCase):
    def test_timeout_set(self):
        con = Urllib3HttpConnection(timeout=42)
        self.assertEquals(42, con.timeout)

    def test_http_auth(self):
        con = Urllib3HttpConnection(http_auth='username:secret')
        self.assertEquals({'authorization': 'Basic dXNlcm5hbWU6c2VjcmV0'}, con.headers)

    def test_http_auth_tuple(self):
        con = Urllib3HttpConnection(http_auth=('username', 'secret'))
        self.assertEquals({'authorization': 'Basic dXNlcm5hbWU6c2VjcmV0'}, con.headers)

    def test_http_auth_list(self):
        con = Urllib3HttpConnection(http_auth=['username', 'secret'])
        self.assertEquals({'authorization': 'Basic dXNlcm5hbWU6c2VjcmV0'}, con.headers)

    def test_uses_https_if_specified(self):
        con = Urllib3HttpConnection(use_ssl=True)
        self.assertIsInstance(con.pool, urllib3.HTTPSConnectionPool)

    def test_doesnt_use_https_if_not_specified(self):
        con = Urllib3HttpConnection()
        self.assertIsInstance(con.pool, urllib3.HTTPConnectionPool)

    def test_content_length_gets_set(self):
        con = Urllib3HttpConnection()
        m = con.pool.urlopen = Mock()
        m.return_value.status = 200

        con.perform_request('PUT', '/', body='0123456789'.encode('utf-8'))
        m.assert_called_once_with('PUT', '/', '0123456789'.encode('utf-8'), headers={'content-length': '10'}, retries=False)

class TestRequestsConnection(TestCase):
    def _get_mock_connection(self, connection_params={}, status_code=200, response_body='{}'):
        con = RequestsHttpConnection(**connection_params)
        def _dummy_send(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = {}
            dummy_response.status_code = status_code
            dummy_response.text = response_body
            dummy_response.request = args[0]
            dummy_response.cookies = {}
            _dummy_send.call_args = (args, kwargs)
            return dummy_response
        con.session.send = _dummy_send
        return con

    def _get_request(self, connection, *args, **kwargs):
        if 'body' in kwargs:
            kwargs['body'] = kwargs['body'].encode('utf-8')

        status, headers, data = connection.perform_request(*args, **kwargs)
        self.assertEquals(200, status)
        self.assertEquals('{}', data)

        timeout = kwargs.pop('timeout', connection.timeout)
        args, kwargs = connection.session.send.call_args
        self.assertEquals(timeout, kwargs['timeout'])
        self.assertEquals(1, len(args))
        return args[0]

    def test_timeout_set(self):
        con = RequestsHttpConnection(timeout=42)
        self.assertEquals(42, con.timeout)

    def test_use_https_if_specified(self):
        con = self._get_mock_connection({'use_ssl': True, 'url_prefix': 'url'})
        request = self._get_request(con, 'GET', '/')

        self.assertEquals('https://localhost:9200/url/', request.url)
        self.assertEquals('GET', request.method)
        self.assertEquals(None, request.body)

    def test_http_auth(self):
        con = RequestsHttpConnection(http_auth='username:secret')
        self.assertEquals(('username', 'secret'), con.session.auth)

    def test_http_auth_tuple(self):
        con = RequestsHttpConnection(http_auth=('username', 'secret'))
        self.assertEquals(('username', 'secret'), con.session.auth)

    def test_http_auth_list(self):
        con = RequestsHttpConnection(http_auth=['username', 'secret'])
        self.assertEquals(('username', 'secret'), con.session.auth)

    def test_repr(self):
        con = self._get_mock_connection({"host": "elasticsearch.com", "port": 443})
        self.assertEquals('<RequestsHttpConnection: http://elasticsearch.com:443>', repr(con))

    def test_conflict_error_is_returned_on_409(self):
        con = self._get_mock_connection(status_code=409)
        self.assertRaises(ConflictError, con.perform_request, 'GET', '/', {}, '')

    def test_not_found_error_is_returned_on_404(self):
        con = self._get_mock_connection(status_code=404)
        self.assertRaises(NotFoundError, con.perform_request, 'GET', '/', {}, '')

    def test_request_error_is_returned_on_400(self):
        con = self._get_mock_connection(status_code=400)
        self.assertRaises(RequestError, con.perform_request, 'GET', '/', {}, '')

    @patch('elasticsearch.connection.base.tracer')
    @patch('elasticsearch.connection.base.logger')
    def test_failed_request_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(response_body='{"answer": 42}', status_code=500)
        self.assertRaises(TransportError, con.perform_request, 'GET', '/', {'param': 42}, '{}'.encode('utf-8'))

        # no trace request
        self.assertEquals(0, tracer.info.call_count)
        # no trace response
        self.assertEquals(0, tracer.debug.call_count)
        # log url and duration
        self.assertEquals(1, logger.warning.call_count)
        self.assertTrue(re.match(
            '^GET http://localhost:9200/\?param=42 \[status:500 request:0.[0-9]{3}s\]',
            logger.warning.call_args[0][0] % logger.warning.call_args[0][1:]
        ))

    @patch('elasticsearch.connection.base.tracer')
    @patch('elasticsearch.connection.base.logger')
    def test_success_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(response_body='''{"answer": "that's it!"}''')
        status, headers, data = con.perform_request('GET', '/', {'param': 42}, '''{"question": "what's that?"}'''.encode('utf-8'))

        # trace request
        self.assertEquals(1, tracer.info.call_count)
        self.assertEquals(
            """curl -XGET 'http://localhost:9200/?pretty&param=42' -d '{\n  "question": "what\\u0027s that?"\n}'""",
            tracer.info.call_args[0][0] % tracer.info.call_args[0][1:]
        )
        # trace response
        self.assertEquals(1, tracer.debug.call_count)
        self.assertTrue(re.match(
            '#\[200\] \(0.[0-9]{3}s\)\n#\{\n#  "answer": "that\\\\u0027s it!"\n#\}',
            tracer.debug.call_args[0][0] % tracer.debug.call_args[0][1:]
        ))

        # log url and duration
        self.assertEquals(1, logger.info.call_count)
        self.assertTrue(re.match(
            'GET http://localhost:9200/\?param=42 \[status:200 request:0.[0-9]{3}s\]',
            logger.info.call_args[0][0] % logger.info.call_args[0][1:]
        ))
        # log request body and response
        self.assertEquals(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list
        self.assertEquals(
            '> {"question": "what\'s that?"}',
            req[0][0] % req[0][1:]
        )
        self.assertEquals(
            '< {"answer": "that\'s it!"}',
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
        self.assertEquals('{"answer": 42}'.encode('utf-8'), request.body)

    def test_http_auth_attached(self):
        con = self._get_mock_connection({'http_auth': 'username:secret'})
        request = self._get_request(con, 'GET', '/')

        self.assertEquals(request.headers['authorization'], 'Basic dXNlcm5hbWU6c2VjcmV0')

    @patch('elasticsearch.connection.base.tracer')
    def test_url_prefix(self, tracer):
        con = self._get_mock_connection({"url_prefix": "/some-prefix/"})
        request = self._get_request(con, 'GET', '/_search', body='{"answer": 42}', timeout=0.1)

        self.assertEquals('http://localhost:9200/some-prefix/_search', request.url)
        self.assertEquals('GET', request.method)
        self.assertEquals('{"answer": 42}'.encode('utf-8'), request.body)

        # trace request
        self.assertEquals(1, tracer.info.call_count)
        self.assertEquals(
            "curl -XGET 'http://localhost:9200/_search?pretty' -d '{\n  \"answer\": 42\n}'",
            tracer.info.call_args[0][0] % tracer.info.call_args[0][1:]
        )

import re
import ssl
import gzip
import io
from mock import Mock, patch
import urllib3
import warnings
from requests.auth import AuthBase
from platform import python_version

from elasticsearch.exceptions import (
    TransportError,
    ConflictError,
    RequestError,
    NotFoundError,
)
from elasticsearch.connection import RequestsHttpConnection, Urllib3HttpConnection
from elasticsearch import __versionstr__
from .test_cases import TestCase, SkipTest


def gzip_decompress(data):
    buf = gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb")
    return buf.read()


class TestUrllib3Connection(TestCase):
    def _get_mock_connection(
        self, connection_params={}, response_body=b"{}"
    ):
        con = Urllib3HttpConnection(**connection_params)

        def _dummy_urlopen(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = {}
            dummy_response.status = 200
            dummy_response.data = response_body
            _dummy_urlopen.call_args = (args, kwargs)
            return dummy_response

        con.pool.urlopen = _dummy_urlopen
        return con

    def test_ssl_context(self):
        try:
            context = ssl.create_default_context()
        except AttributeError:
            # if create_default_context raises an AttributeError Exception
            # it means SSLContext is not available for that version of python
            # and we should skip this test.
            raise SkipTest(
                "Test test_ssl_context is skipped cause SSLContext is not available for this version of ptyhon"
            )

        con = Urllib3HttpConnection(use_ssl=True, ssl_context=context)
        self.assertEqual(len(con.pool.conn_kw.keys()), 1)
        self.assertIsInstance(con.pool.conn_kw["ssl_context"], ssl.SSLContext)
        self.assertTrue(con.use_ssl)

    def test_http_cloud_id(self):
        con = Urllib3HttpConnection(
            cloud_id="foobar:ZXhhbXBsZS5jbG91ZC5jb20kMGZkNTBmNjIzMjBlZDY1MzlmNmNiNDhlMWI2OCRhYzUzOTVhODgz\nNDU2NmM5ZjE1Y2Q4ZTQ5MGE=\n"
        )
        self.assertTrue(con.use_ssl)
        self.assertEquals(
            con.host, "https://0fd50f62320ed6539f6cb48e1b68.example.cloud.com:9243"
        )

    def test_api_key_auth(self):
        # test with tuple
        con = Urllib3HttpConnection(
            cloud_id="foobar:ZXhhbXBsZS5jbG91ZC5jb20kMGZkNTBmNjIzMjBlZDY1MzlmNmNiNDhlMWI2OCRhYzUzOTVhODgz\nNDU2NmM5ZjE1Y2Q4ZTQ5MGE=\n",
            api_key=("elastic", "changeme1"),
        )
        self.assertEquals(con.headers["authorization"], "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTE=")

        # test with base64 encoded string
        con = Urllib3HttpConnection(
            cloud_id="foobar:ZXhhbXBsZS5jbG91ZC5jb20kMGZkNTBmNjIzMjBlZDY1MzlmNmNiNDhlMWI2OCRhYzUzOTVhODgz\nNDU2NmM5ZjE1Y2Q4ZTQ5MGE=\n",
            api_key="ZWxhc3RpYzpjaGFuZ2VtZTI=",
        )
        self.assertEquals(con.headers["authorization"], "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTI=")

    def test_no_http_compression(self):
        con = self._get_mock_connection()
        self.assertFalse(con.http_compress)
        self.assertNotIn("accept-encoding", con.headers)

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertFalse(req_body)
        self.assertNotIn("accept-encoding", kwargs["headers"])
        self.assertNotIn("content-encoding", kwargs["headers"])

    def test_http_compression(self):
        con = self._get_mock_connection({"http_compress": True})
        self.assertTrue(con.http_compress)
        self.assertEqual(con.headers["accept-encoding"], "gzip,deflate")

        # 'content-encoding' shouldn't be set at a connection level.
        # Should be applied only if the request is sent with a body.
        self.assertNotIn("content-encoding", con.headers)

        con.perform_request("GET", "/", body=b"{}")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertEqual(gzip_decompress(req_body), b"{}")
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertEqual(kwargs["headers"]["content-encoding"], "gzip")

        con.perform_request("GET", "/")

        (_, _, req_body), kwargs = con.pool.urlopen.call_args

        self.assertFalse(req_body)
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertNotIn("content-encoding", kwargs["headers"])

    def test_default_user_agent(self):
        con = Urllib3HttpConnection()
        self.assertEquals(con._get_default_user_agent(), "elasticsearch-py/%s (Python %s)" % (__versionstr__, python_version()))

    def test_timeout_set(self):
        con = Urllib3HttpConnection(timeout=42)
        self.assertEquals(42, con.timeout)

    def test_keep_alive_is_on_by_default(self):
        con = Urllib3HttpConnection()
        self.assertEquals(
            {
                "connection": "keep-alive",
                "content-type": "application/json",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth(self):
        con = Urllib3HttpConnection(http_auth="username:secret")
        self.assertEquals(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "connection": "keep-alive",
                "content-type": "application/json",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth_tuple(self):
        con = Urllib3HttpConnection(http_auth=("username", "secret"))
        self.assertEquals(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "content-type": "application/json",
                "connection": "keep-alive",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth_list(self):
        con = Urllib3HttpConnection(http_auth=["username", "secret"])
        self.assertEquals(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "content-type": "application/json",
                "connection": "keep-alive",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(use_ssl=True, verify_certs=False)
            self.assertEquals(1, len(w))
            self.assertEquals(
                "Connecting to localhost using SSL with verify_certs=False is insecure.",
                str(w[0].message),
            )

        self.assertIsInstance(con.pool, urllib3.HTTPSConnectionPool)

    def nowarn_when_test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = Urllib3HttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            self.assertEquals(0, len(w))

        self.assertIsInstance(con.pool, urllib3.HTTPSConnectionPool)

    def test_doesnt_use_https_if_not_specified(self):
        con = Urllib3HttpConnection()
        self.assertIsInstance(con.pool, urllib3.HTTPConnectionPool)

    def test_no_warning_when_using_ssl_context(self):
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            Urllib3HttpConnection(ssl_context=ctx)
            self.assertEquals(0, len(w))

    def test_warns_if_using_non_default_ssl_kwargs_with_ssl_context(self):
        for kwargs in (
            {"ssl_show_warn": False},
            {"ssl_show_warn": True},
            {"verify_certs": True},
            {"verify_certs": False},
            {"ca_certs": "/path/to/certs"},
            {"ssl_show_warn": True, "ca_certs": "/path/to/certs"},
        ):
            kwargs["ssl_context"] = ssl.create_default_context()

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                Urllib3HttpConnection(**kwargs)

                self.assertEquals(1, len(w))
                self.assertEquals(
                    "When using `ssl_context`, all other SSL related kwargs are ignored",
                    str(w[0].message),
                )

    @patch("elasticsearch.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        con = self._get_mock_connection(connection_params={"http_compress": True})
        con.perform_request("GET", "/", body=b"{\"example\": \"body\"}")

        self.assertEquals(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list
        print(req, resp)
        self.assertEquals('> {"example": "body"}', req[0][0] % req[0][1:])
        self.assertEquals('< {}', resp[0][0] % resp[0][1:])


class TestRequestsConnection(TestCase):
    def _get_mock_connection(
        self, connection_params={}, status_code=200, response_body="{}"
    ):
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
        if "body" in kwargs:
            kwargs["body"] = kwargs["body"].encode("utf-8")

        status, headers, data = connection.perform_request(*args, **kwargs)
        self.assertEquals(200, status)
        self.assertEquals("{}", data)

        timeout = kwargs.pop("timeout", connection.timeout)
        args, kwargs = connection.session.send.call_args
        self.assertEquals(timeout, kwargs["timeout"])
        self.assertEquals(1, len(args))
        return args[0]

    def test_custom_http_auth_is_allowed(self):
        auth = AuthBase()
        c = RequestsHttpConnection(http_auth=auth)

        self.assertEquals(auth, c.session.auth)

    def test_timeout_set(self):
        con = RequestsHttpConnection(timeout=42)
        self.assertEquals(42, con.timeout)

    def test_http_cloud_id(self):
        con = RequestsHttpConnection(
            cloud_id="foobar:ZXhhbXBsZS5jbG91ZC5jb20kMGZkNTBmNjIzMjBlZDY1MzlmNmNiNDhlMWI2OCRhYzUzOTVhODgz\nNDU2NmM5ZjE1Y2Q4ZTQ5MGE=\n"
        )
        self.assertTrue(con.use_ssl)
        self.assertEquals(
            con.host, "https://0fd50f62320ed6539f6cb48e1b68.example.cloud.com:9243"
        )

    def test_api_key_auth(self):
        # test with tuple
        con = RequestsHttpConnection(
            cloud_id="foobar:ZXhhbXBsZS5jbG91ZC5jb20kMGZkNTBmNjIzMjBlZDY1MzlmNmNiNDhlMWI2OCRhYzUzOTVhODgz\nNDU2NmM5ZjE1Y2Q4ZTQ5MGE=\n",
            api_key=("elastic", "changeme1"),
        )
        self.assertEquals(con.session.headers["authorization"], "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTE=")

        # test with base64 encoded string
        con = RequestsHttpConnection(
            cloud_id="foobar:ZXhhbXBsZS5jbG91ZC5jb20kMGZkNTBmNjIzMjBlZDY1MzlmNmNiNDhlMWI2OCRhYzUzOTVhODgz\nNDU2NmM5ZjE1Y2Q4ZTQ5MGE=\n",
            api_key="ZWxhc3RpYzpjaGFuZ2VtZTI=",
        )
        self.assertEquals(con.session.headers["authorization"], "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTI=")

    def test_no_http_compression(self):
        con = self._get_mock_connection()

        self.assertFalse(con.http_compress)
        self.assertNotIn("content-encoding", con.session.headers)

        con.perform_request("GET", "/")

        req = con.session.send.call_args[0][0]
        self.assertNotIn("content-encoding", req.headers)
        self.assertNotIn("accept-encoding", req.headers)

    def test_http_compression(self):
        con = self._get_mock_connection(
            {"http_compress": True},
        )

        self.assertTrue(con.http_compress)

        # 'content-encoding' shouldn't be set at a session level.
        # Should be applied only if the request is sent with a body.
        self.assertNotIn("content-encoding", con.session.headers)

        con.perform_request("GET", "/", body=b"{}")

        req = con.session.send.call_args[0][0]
        self.assertEqual(req.headers["content-encoding"], "gzip")
        self.assertEqual(req.headers["accept-encoding"], "gzip,deflate")

        con.perform_request("GET", "/")

        req = con.session.send.call_args[0][0]
        self.assertNotIn("content-encoding", req.headers)
        self.assertEqual(req.headers["accept-encoding"], "gzip,deflate")

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = self._get_mock_connection(
                {"use_ssl": True, "url_prefix": "url", "verify_certs": False}
            )
            self.assertEquals(1, len(w))
            self.assertEquals(
                "Connecting to https://localhost:9200/url using SSL with verify_certs=False is insecure.",
                str(w[0].message),
            )

        request = self._get_request(con, "GET", "/")

        self.assertEquals("https://localhost:9200/url/", request.url)
        self.assertEquals("GET", request.method)
        self.assertEquals(None, request.body)

    def nowarn_when_test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = self._get_mock_connection(
                {
                    "use_ssl": True,
                    "url_prefix": "url",
                    "verify_certs": False,
                    "ssl_show_warn": False,
                }
            )
            self.assertEquals(0, len(w))

        request = self._get_request(con, "GET", "/")

        self.assertEquals("https://localhost:9200/url/", request.url)
        self.assertEquals("GET", request.method)
        self.assertEquals(None, request.body)

    def test_merge_headers(self):
        con = self._get_mock_connection(
            connection_params={"headers": {"h1": "v1", "h2": "v2"}}
        )
        req = self._get_request(con, "GET", "/", headers={"h2": "v2p", "h3": "v3"})
        self.assertEquals(req.headers["h1"], "v1")
        self.assertEquals(req.headers["h2"], "v2p")
        self.assertEquals(req.headers["h3"], "v3")

    def test_default_headers(self):
        con = self._get_mock_connection()
        req = self._get_request(con, "GET", "/")
        self.assertEquals(req.headers["content-type"], "application/json")
        self.assertEquals(req.headers["user-agent"], con._get_default_user_agent())

    def test_custom_headers(self):
        con = self._get_mock_connection()
        req = self._get_request(con, "GET", "/", headers={
            "content-type": "application/x-ndjson",
            "user-agent": "custom-agent/1.2.3",
        })
        self.assertEquals(req.headers["content-type"], "application/x-ndjson")
        self.assertEquals(req.headers["user-agent"], "custom-agent/1.2.3")

    def test_http_auth(self):
        con = RequestsHttpConnection(http_auth="username:secret")
        self.assertEquals(("username", "secret"), con.session.auth)

    def test_http_auth_tuple(self):
        con = RequestsHttpConnection(http_auth=("username", "secret"))
        self.assertEquals(("username", "secret"), con.session.auth)

    def test_http_auth_list(self):
        con = RequestsHttpConnection(http_auth=["username", "secret"])
        self.assertEquals(("username", "secret"), con.session.auth)

    def test_repr(self):
        con = self._get_mock_connection({"host": "elasticsearch.com", "port": 443})
        self.assertEquals(
            "<RequestsHttpConnection: http://elasticsearch.com:443>", repr(con)
        )

    def test_conflict_error_is_returned_on_409(self):
        con = self._get_mock_connection(status_code=409)
        self.assertRaises(ConflictError, con.perform_request, "GET", "/", {}, "")

    def test_not_found_error_is_returned_on_404(self):
        con = self._get_mock_connection(status_code=404)
        self.assertRaises(NotFoundError, con.perform_request, "GET", "/", {}, "")

    def test_request_error_is_returned_on_400(self):
        con = self._get_mock_connection(status_code=400)
        self.assertRaises(RequestError, con.perform_request, "GET", "/", {}, "")

    @patch("elasticsearch.connection.base.logger")
    def test_head_with_404_doesnt_get_logged(self, logger):
        con = self._get_mock_connection(status_code=404)
        self.assertRaises(NotFoundError, con.perform_request, "HEAD", "/", {}, "")
        self.assertEquals(0, logger.warning.call_count)

    @patch("elasticsearch.connection.base.tracer")
    @patch("elasticsearch.connection.base.logger")
    def test_failed_request_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(response_body='{"answer": 42}', status_code=500)
        self.assertRaises(
            TransportError,
            con.perform_request,
            "GET",
            "/",
            {"param": 42},
            "{}".encode("utf-8"),
        )

        # trace request
        self.assertEquals(1, tracer.info.call_count)
        # trace response
        self.assertEquals(1, tracer.debug.call_count)
        # log url and duration
        self.assertEquals(1, logger.warning.call_count)
        self.assertTrue(
            re.match(
                "^GET http://localhost:9200/\?param=42 \[status:500 request:0.[0-9]{3}s\]",
                logger.warning.call_args[0][0] % logger.warning.call_args[0][1:],
            )
        )

    @patch("elasticsearch.connection.base.tracer")
    @patch("elasticsearch.connection.base.logger")
    def test_success_logs_and_traces(self, logger, tracer):
        con = self._get_mock_connection(response_body="""{"answer": "that's it!"}""")
        status, headers, data = con.perform_request(
            "GET",
            "/",
            {"param": 42},
            """{"question": "what's that?"}""".encode("utf-8"),
        )

        # trace request
        self.assertEquals(1, tracer.info.call_count)
        self.assertEquals(
            """curl -H 'Content-Type: application/json' -XGET 'http://localhost:9200/?pretty&param=42' -d '{\n  "question": "what\\u0027s that?"\n}'""",
            tracer.info.call_args[0][0] % tracer.info.call_args[0][1:],
        )
        # trace response
        self.assertEquals(1, tracer.debug.call_count)
        self.assertTrue(
            re.match(
                '#\[200\] \(0.[0-9]{3}s\)\n#\{\n#  "answer": "that\\\\u0027s it!"\n#\}',
                tracer.debug.call_args[0][0] % tracer.debug.call_args[0][1:],
            )
        )

        # log url and duration
        self.assertEquals(1, logger.info.call_count)
        self.assertTrue(
            re.match(
                "GET http://localhost:9200/\?param=42 \[status:200 request:0.[0-9]{3}s\]",
                logger.info.call_args[0][0] % logger.info.call_args[0][1:],
            )
        )
        # log request body and response
        self.assertEquals(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list
        self.assertEquals('> {"question": "what\'s that?"}', req[0][0] % req[0][1:])
        self.assertEquals('< {"answer": "that\'s it!"}', resp[0][0] % resp[0][1:])

    @patch("elasticsearch.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        con = self._get_mock_connection(connection_params={"http_compress": True})
        con.perform_request("GET", "/", body=b"{\"example\": \"body\"}")

        self.assertEquals(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list
        self.assertEquals('> {"example": "body"}', req[0][0] % req[0][1:])
        self.assertEquals('< {}', resp[0][0] % resp[0][1:])

    def test_defaults(self):
        con = self._get_mock_connection()
        request = self._get_request(con, "GET", "/")

        self.assertEquals("http://localhost:9200/", request.url)
        self.assertEquals("GET", request.method)
        self.assertEquals(None, request.body)

    def test_params_properly_encoded(self):
        con = self._get_mock_connection()
        request = self._get_request(
            con, "GET", "/", params={"param": "value with spaces"}
        )

        self.assertEquals("http://localhost:9200/?param=value+with+spaces", request.url)
        self.assertEquals("GET", request.method)
        self.assertEquals(None, request.body)

    def test_body_attached(self):
        con = self._get_mock_connection()
        request = self._get_request(con, "GET", "/", body='{"answer": 42}')

        self.assertEquals("http://localhost:9200/", request.url)
        self.assertEquals("GET", request.method)
        self.assertEquals('{"answer": 42}'.encode("utf-8"), request.body)

    def test_http_auth_attached(self):
        con = self._get_mock_connection({"http_auth": "username:secret"})
        request = self._get_request(con, "GET", "/")

        self.assertEquals(
            request.headers["authorization"], "Basic dXNlcm5hbWU6c2VjcmV0"
        )

    @patch("elasticsearch.connection.base.tracer")
    def test_url_prefix(self, tracer):
        con = self._get_mock_connection({"url_prefix": "/some-prefix/"})
        request = self._get_request(
            con, "GET", "/_search", body='{"answer": 42}', timeout=0.1
        )

        self.assertEquals("http://localhost:9200/some-prefix/_search", request.url)
        self.assertEquals("GET", request.method)
        self.assertEquals('{"answer": 42}'.encode("utf-8"), request.body)

        # trace request
        self.assertEquals(1, tracer.info.call_count)
        self.assertEquals(
            "curl -H 'Content-Type: application/json' -XGET 'http://localhost:9200/_search?pretty' -d '{\n  \"answer\": 42\n}'",
            tracer.info.call_args[0][0] % tracer.info.call_args[0][1:],
        )

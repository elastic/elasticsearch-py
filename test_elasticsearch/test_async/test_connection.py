# -*- coding: utf-8 -*-
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import gzip
import io
import json
import ssl
import warnings
from platform import python_version

import aiohttp
import pytest
from mock import patch
from multidict import CIMultiDict

from elasticsearch import AIOHttpConnection, __versionstr__
from elasticsearch.compat import reraise_exceptions
from elasticsearch.exceptions import ConnectionError

pytestmark = pytest.mark.asyncio


def gzip_decompress(data):
    buf = gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb")
    return buf.read()


class TestAIOHttpConnection:
    async def _get_mock_connection(self, connection_params={}, response_body=b"{}"):
        con = AIOHttpConnection(**connection_params)
        await con._create_aiohttp_session()

        def _dummy_request(*args, **kwargs):
            class DummyResponse:
                async def __aenter__(self, *_, **__):
                    return self

                async def __aexit__(self, *_, **__):
                    pass

                async def text(self):
                    return response_body.decode("utf-8", "surrogatepass")

            dummy_response = DummyResponse()
            dummy_response.headers = CIMultiDict()
            dummy_response.status = 200
            _dummy_request.call_args = (args, kwargs)
            return dummy_response

        con.session.request = _dummy_request
        return con

    async def test_ssl_context(self):
        try:
            context = ssl.create_default_context()
        except AttributeError:
            # if create_default_context raises an AttributeError Exception
            # it means SSLContext is not available for that version of python
            # and we should skip this test.
            pytest.skip(
                "Test test_ssl_context is skipped cause SSLContext is not available for this version of Python"
            )

        con = AIOHttpConnection(use_ssl=True, ssl_context=context)
        await con._create_aiohttp_session()
        assert con.use_ssl
        assert con.session.connector._ssl == context

    def test_opaque_id(self):
        con = AIOHttpConnection(opaque_id="app-1")
        assert con.headers["x-opaque-id"] == "app-1"

    def test_http_cloud_id(self):
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng=="
        )
        assert con.use_ssl
        assert (
            con.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        assert con.port is None
        assert con.hostname == "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        assert con.http_compress

        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            port=9243,
        )
        assert (
            con.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io:9243"
        )
        assert con.port == 9243
        assert con.hostname == "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"

    def test_api_key_auth(self):
        # test with tuple
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key=("elastic", "changeme1"),
        )
        assert con.headers["authorization"] == "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTE="
        assert (
            con.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

        # test with base64 encoded string
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key="ZWxhc3RpYzpjaGFuZ2VtZTI=",
        )
        assert con.headers["authorization"] == "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTI="
        assert (
            con.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

    async def test_no_http_compression(self):
        con = await self._get_mock_connection()
        assert not con.http_compress
        assert "accept-encoding" not in con.headers

        await con.perform_request("GET", "/")

        _, kwargs = con.session.request.call_args

        assert not kwargs["data"]
        assert "accept-encoding" not in kwargs["headers"]
        assert "content-encoding" not in kwargs["headers"]

    async def test_http_compression(self):
        con = await self._get_mock_connection({"http_compress": True})
        assert con.http_compress
        assert con.headers["accept-encoding"] == "gzip,deflate"

        # 'content-encoding' shouldn't be set at a connection level.
        # Should be applied only if the request is sent with a body.
        assert "content-encoding" not in con.headers

        await con.perform_request("GET", "/", body=b"{}")

        _, kwargs = con.session.request.call_args

        assert gzip_decompress(kwargs["data"]) == b"{}"
        assert kwargs["headers"]["accept-encoding"] == "gzip,deflate"
        assert kwargs["headers"]["content-encoding"] == "gzip"

        await con.perform_request("GET", "/")

        _, kwargs = con.session.request.call_args

        assert not kwargs["data"]
        assert kwargs["headers"]["accept-encoding"] == "gzip,deflate"
        assert "content-encoding" not in kwargs["headers"]

    def test_cloud_id_http_compress_override(self):
        # 'http_compress' will be 'True' by default for connections with
        # 'cloud_id' set but should prioritize user-defined values.
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )
        assert con.http_compress is True

        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=False,
        )
        assert con.http_compress is False

        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=True,
        )
        assert con.http_compress is True

    async def test_url_prefix(self):
        con = await self._get_mock_connection(
            connection_params={"url_prefix": "/_search/"}
        )
        assert con.url_prefix == "/_search"

        await con.perform_request("GET", "/")

        # Need to convert the yarl URL to a string to compare.
        method, yarl_url = con.session.request.call_args[0]
        assert method == "GET" and str(yarl_url) == "http://localhost:9200/_search/"

    def test_default_user_agent(self):
        con = AIOHttpConnection()
        assert con._get_default_user_agent() == "elasticsearch-py/%s (Python %s)" % (
            __versionstr__,
            python_version(),
        )

    def test_timeout_set(self):
        con = AIOHttpConnection(timeout=42)
        assert 42 == con.timeout

    def test_keep_alive_is_on_by_default(self):
        con = AIOHttpConnection()
        assert {
            "connection": "keep-alive",
            "content-type": "application/json",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    def test_http_auth(self):
        con = AIOHttpConnection(http_auth="username:secret")
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "connection": "keep-alive",
            "content-type": "application/json",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    def test_http_auth_tuple(self):
        con = AIOHttpConnection(http_auth=("username", "secret"))
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "content-type": "application/json",
            "connection": "keep-alive",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    def test_http_auth_list(self):
        con = AIOHttpConnection(http_auth=["username", "secret"])
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "content-type": "application/json",
            "connection": "keep-alive",
            "user-agent": con._get_default_user_agent(),
        } == con.headers

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = AIOHttpConnection(use_ssl=True, verify_certs=False)
            assert 1 == len(w)
            assert (
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure."
                == str(w[0].message)
            )

        assert con.use_ssl
        assert con.scheme == "https"
        assert con.host == "https://localhost:9200"

    async def test_nowarn_when_test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = AIOHttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            await con._create_aiohttp_session()
            assert w == []

        assert isinstance(con.session, aiohttp.ClientSession)

    def test_doesnt_use_https_if_not_specified(self):
        con = AIOHttpConnection()
        assert not con.use_ssl

    def test_no_warning_when_using_ssl_context(self):
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            AIOHttpConnection(ssl_context=ctx)
            assert w == [], str([x.message for x in w])

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

                AIOHttpConnection(**kwargs)

                assert 1 == len(w)
                assert (
                    "When using `ssl_context`, all other SSL related kwargs are ignored"
                    == str(w[0].message)
                )

    @patch("elasticsearch.connection.base.logger")
    async def test_uncompressed_body_logged(self, logger):
        con = await self._get_mock_connection(connection_params={"http_compress": True})
        await con.perform_request("GET", "/", body=b'{"example": "body"}')

        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list

        assert '> {"example": "body"}' == req[0][0] % req[0][1:]
        assert "< {}" == resp[0][0] % resp[0][1:]

    async def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = await self._get_mock_connection(response_body=buf)
        status, headers, data = await con.perform_request("GET", "/")
        assert u"你好\uda6a" == data

    @pytest.mark.parametrize("exception_cls", reraise_exceptions)
    async def test_recursion_error_reraised(self, exception_cls):
        conn = AIOHttpConnection()

        def request_raise(*_, **__):
            raise exception_cls("Wasn't modified!")

        await conn._create_aiohttp_session()
        conn.session.request = request_raise

        with pytest.raises(exception_cls) as e:
            await conn.perform_request("GET", "/")
        assert str(e.value) == "Wasn't modified!"


class TestConnectionHttpbin:
    """Tests the HTTP connection implementations against a live server E2E"""

    async def httpbin_anything(self, conn, **kwargs):
        status, headers, data = await conn.perform_request("GET", "/anything", **kwargs)
        data = json.loads(data)
        data["headers"].pop(
            "X-Amzn-Trace-Id", None
        )  # Remove this header as it's put there by AWS.
        return (status, data)

    async def test_aiohttp_connection(self):
        # Defaults
        conn = AIOHttpConnection("httpbin.org", port=443, use_ssl=True)
        user_agent = conn._get_default_user_agent()
        status, data = await self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=False
        conn = AIOHttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=False
        )
        status, data = await self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=True
        conn = AIOHttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=True
        )
        status, data = await self.httpbin_anything(conn)
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # Headers
        conn = AIOHttpConnection(
            "httpbin.org",
            port=443,
            use_ssl=True,
            http_compress=True,
            headers={"header1": "value1"},
        )
        status, data = await self.httpbin_anything(
            conn, headers={"header2": "value2", "header1": "override!"}
        )
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "Header1": "override!",
            "Header2": "value2",
            "User-Agent": user_agent,
        }

    async def test_aiohttp_connection_error(self):
        conn = AIOHttpConnection("not.a.host.name")
        with pytest.raises(ConnectionError):
            await conn.perform_request("GET", "/")

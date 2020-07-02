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

import ssl
import gzip
import io
from mock import patch
import warnings
from platform import python_version
import aiohttp
import pytest

from elasticsearch import AIOHttpConnection
from elasticsearch import __versionstr__
from ..test_cases import TestCase, SkipTest

pytestmark = pytest.mark.asyncio


def gzip_decompress(data):
    buf = gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb")
    return buf.read()


class TestAIOHttpConnection(TestCase):
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
            dummy_response.headers = {}
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
            raise SkipTest(
                "Test test_ssl_context is skipped cause SSLContext is not available for this version of ptyhon"
            )

        con = AIOHttpConnection(use_ssl=True, ssl_context=context)
        await con._create_aiohttp_session()
        self.assertTrue(con.use_ssl)
        self.assertEqual(con.session.connector._ssl, context)

    def test_opaque_id(self):
        con = AIOHttpConnection(opaque_id="app-1")
        self.assertEqual(con.headers["x-opaque-id"], "app-1")

    def test_http_cloud_id(self):
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng=="
        )
        self.assertTrue(con.use_ssl)
        self.assertEqual(
            con.host, "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        self.assertEqual(con.port, None)
        self.assertEqual(
            con.hostname, "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        self.assertTrue(con.http_compress)

        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            port=9243,
        )
        self.assertEqual(
            con.host,
            "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io:9243",
        )
        self.assertEqual(con.port, 9243)
        self.assertEqual(
            con.hostname, "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

    def test_api_key_auth(self):
        # test with tuple
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key=("elastic", "changeme1"),
        )
        self.assertEqual(
            con.headers["authorization"], "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTE="
        )
        self.assertEqual(
            con.host, "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

        # test with base64 encoded string
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key="ZWxhc3RpYzpjaGFuZ2VtZTI=",
        )
        self.assertEqual(
            con.headers["authorization"], "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTI="
        )
        self.assertEqual(
            con.host, "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

    async def test_no_http_compression(self):
        con = await self._get_mock_connection()
        self.assertFalse(con.http_compress)
        self.assertNotIn("accept-encoding", con.headers)

        await con.perform_request("GET", "/")

        _, kwargs = con.session.request.call_args

        self.assertFalse(kwargs["data"])
        self.assertNotIn("accept-encoding", kwargs["headers"])
        self.assertNotIn("content-encoding", kwargs["headers"])

    async def test_http_compression(self):
        con = await self._get_mock_connection({"http_compress": True})
        self.assertTrue(con.http_compress)
        self.assertEqual(con.headers["accept-encoding"], "gzip,deflate")

        # 'content-encoding' shouldn't be set at a connection level.
        # Should be applied only if the request is sent with a body.
        self.assertNotIn("content-encoding", con.headers)

        await con.perform_request("GET", "/", body=b"{}")

        _, kwargs = con.session.request.call_args

        self.assertEqual(gzip_decompress(kwargs["data"]), b"{}")
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertEqual(kwargs["headers"]["content-encoding"], "gzip")

        await con.perform_request("GET", "/")

        _, kwargs = con.session.request.call_args

        self.assertFalse(kwargs["data"])
        self.assertEqual(kwargs["headers"]["accept-encoding"], "gzip,deflate")
        self.assertNotIn("content-encoding", kwargs["headers"])

    def test_cloud_id_http_compress_override(self):
        # 'http_compress' will be 'True' by default for connections with
        # 'cloud_id' set but should prioritize user-defined values.
        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )
        self.assertEqual(con.http_compress, True)

        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=False,
        )
        self.assertEqual(con.http_compress, False)

        con = AIOHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=True,
        )
        self.assertEqual(con.http_compress, True)

    def test_default_user_agent(self):
        con = AIOHttpConnection()
        self.assertEqual(
            con._get_default_user_agent(),
            "elasticsearch-py/%s (Python %s)" % (__versionstr__, python_version()),
        )

    def test_timeout_set(self):
        con = AIOHttpConnection(timeout=42)
        self.assertEqual(42, con.timeout)

    def test_keep_alive_is_on_by_default(self):
        con = AIOHttpConnection()
        self.assertEqual(
            {
                "connection": "keep-alive",
                "content-type": "application/json",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth(self):
        con = AIOHttpConnection(http_auth="username:secret")
        self.assertEqual(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "connection": "keep-alive",
                "content-type": "application/json",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth_tuple(self):
        con = AIOHttpConnection(http_auth=("username", "secret"))
        self.assertEqual(
            {
                "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
                "content-type": "application/json",
                "connection": "keep-alive",
                "user-agent": con._get_default_user_agent(),
            },
            con.headers,
        )

    def test_http_auth_list(self):
        con = AIOHttpConnection(http_auth=["username", "secret"])
        self.assertEqual(
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
            con = AIOHttpConnection(use_ssl=True, verify_certs=False)
            self.assertEqual(1, len(w))
            self.assertEqual(
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure.",
                str(w[0].message),
            )

        self.assertTrue(con.use_ssl)
        self.assertEqual(con.scheme, "https")
        self.assertEqual(con.host, "https://localhost:9200")

    async def test_nowarn_when_test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            con = AIOHttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            await con._create_aiohttp_session()
            self.assertEqual(0, len(w))

        self.assertIsInstance(con.session, aiohttp.ClientSession)

    def test_doesnt_use_https_if_not_specified(self):
        con = AIOHttpConnection()
        self.assertFalse(con.use_ssl)

    def test_no_warning_when_using_ssl_context(self):
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            AIOHttpConnection(ssl_context=ctx)
            self.assertEqual(0, len(w), str([x.message for x in w]))

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

                self.assertEqual(1, len(w))
                self.assertEqual(
                    "When using `ssl_context`, all other SSL related kwargs are ignored",
                    str(w[0].message),
                )

    @patch("elasticsearch.connection.base.logger")
    async def test_uncompressed_body_logged(self, logger):
        con = await self._get_mock_connection(connection_params={"http_compress": True})
        await con.perform_request("GET", "/", body=b'{"example": "body"}')

        self.assertEqual(2, logger.debug.call_count)
        req, resp = logger.debug.call_args_list

        self.assertEqual('> {"example": "body"}', req[0][0] % req[0][1:])
        self.assertEqual("< {}", resp[0][0] % resp[0][1:])

    async def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        con = await self._get_mock_connection(response_body=buf)
        status, headers, data = await con.perform_request("GET", "/")
        self.assertEqual(u"你好\uda6a", data)

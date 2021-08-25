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
import os
import re
import ssl
import warnings
from platform import python_version

import pytest
import urllib3
from mock import Mock, patch
from requests.auth import AuthBase
from urllib3._collections import HTTPHeaderDict

from elasticsearch import __versionstr__
from elasticsearch.compat import reraise_exceptions
from elasticsearch.connection import (
    Connection,
    RequestsHttpConnection,
    Urllib3HttpConnection,
)
from elasticsearch.exceptions import (
    ConflictError,
    ConnectionError,
    NotFoundError,
    RequestError,
    TransportError,
)

CLOUD_ID_PORT_443 = "cluster:d2VzdGV1cm9wZS5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo0NDMkZTdkZTlmMTM0NWU0NDkwMjgzZDkwM2JlNWI2ZjkxOWUk"
CLOUD_ID_KIBANA = "cluster:d2VzdGV1cm9wZS5henVyZS5lbGFzdGljLWNsb3VkLmNvbSQ4YWY3ZWUzNTQyMGY0NThlOTAzMDI2YjQwNjQwODFmMiQyMDA2MTU1NmM1NDA0OTg2YmZmOTU3ZDg0YTZlYjUxZg=="
CLOUD_ID_PORT_AND_KIBANA = "cluster:d2VzdGV1cm9wZS5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo5MjQzJGM2NjM3ZjMxMmM1MjQzY2RhN2RlZDZlOTllM2QyYzE5JA=="
CLOUD_ID_NO_PORT_OR_KIBANA = "cluster:d2VzdGV1cm9wZS5henVyZS5lbGFzdGljLWNsb3VkLmNvbSRlN2RlOWYxMzQ1ZTQ0OTAyODNkOTAzYmU1YjZmOTE5ZSQ="


def gzip_decompress(data):
    buf = gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb")
    return buf.read()


class TestBaseConnection:
    def test_parse_cloud_id(self):
        # Embedded port in cloud_id
        conn = Connection(cloud_id=CLOUD_ID_PORT_AND_KIBANA)
        assert (
            conn.host
            == "https://c6637f312c5243cda7ded6e99e3d2c19.westeurope.azure.elastic-cloud.com:9243"
        )
        assert conn.port == 9243
        assert (
            conn.hostname
            == "c6637f312c5243cda7ded6e99e3d2c19.westeurope.azure.elastic-cloud.com"
        )
        conn = Connection(
            cloud_id=CLOUD_ID_PORT_AND_KIBANA,
            port=443,
        )
        assert (
            conn.host
            == "https://c6637f312c5243cda7ded6e99e3d2c19.westeurope.azure.elastic-cloud.com:443"
        )
        assert conn.port == 443
        assert (
            conn.hostname
            == "c6637f312c5243cda7ded6e99e3d2c19.westeurope.azure.elastic-cloud.com"
        )
        conn = Connection(cloud_id=CLOUD_ID_PORT_443)
        assert (
            conn.host
            == "https://e7de9f1345e4490283d903be5b6f919e.westeurope.azure.elastic-cloud.com"
        )
        assert conn.port is None
        assert (
            conn.hostname
            == "e7de9f1345e4490283d903be5b6f919e.westeurope.azure.elastic-cloud.com"
        )
        conn = Connection(cloud_id=CLOUD_ID_KIBANA)
        assert (
            conn.host
            == "https://8af7ee35420f458e903026b4064081f2.westeurope.azure.elastic-cloud.com"
        )
        assert conn.port is None
        assert (
            conn.hostname
            == "8af7ee35420f458e903026b4064081f2.westeurope.azure.elastic-cloud.com"
        )

    def test_empty_warnings(self):
        conn = Connection()
        with warnings.catch_warnings(record=True) as w:
            conn._raise_warnings(())
            conn._raise_warnings([])

            assert w == []

    def test_raises_warnings(self):
        conn = Connection()
        with warnings.catch_warnings(record=True) as warn:
            conn._raise_warnings(['299 Elasticsearch-7.6.1-aa751 "this is deprecated"'])

        assert [str(w.message) for w in warn] == ["this is deprecated"]
        with warnings.catch_warnings(record=True) as warn:
            conn._raise_warnings(
                [
                    '299 Elasticsearch-7.6.1-aa751 "this is also deprecated"',
                    '299 Elasticsearch-7.6.1-aa751 "this is also deprecated"',
                    '299 Elasticsearch-7.6.1-aa751 "guess what? deprecated"',
                ]
            )

        assert [str(w.message) for w in warn] == [
            "this is also deprecated",
            "guess what? deprecated",
        ]

    def test_raises_warnings_when_folded(self):
        conn = Connection()
        with warnings.catch_warnings(record=True) as warn:
            conn._raise_warnings(
                [
                    '299 Elasticsearch-7.6.1-aa751 "warning",'
                    '299 Elasticsearch-7.6.1-aa751 "folded"',
                ]
            )

        assert [str(w.message) for w in warn] == ["warning", "folded"]

    def test_ipv6_host_and_port(self):
        for kwargs, expected_host in [
            ({"host": "::1"}, "http://[::1]:9200"),
            ({"host": "::1", "port": 443}, "http://[::1]:443"),
            ({"host": "::1", "use_ssl": True}, "https://[::1]:9200"),
            ({"host": "127.0.0.1", "port": 1234}, "http://127.0.0.1:1234"),
            ({"host": "localhost", "use_ssl": True}, "https://localhost:9200"),
        ]:
            conn = Connection(**kwargs)
            assert conn.host == expected_host

    def test_meta_header(self):
        conn = Connection(meta_header=True)
        assert conn.meta_header is True
        conn = Connection(meta_header=False)
        assert conn.meta_header is False
        with pytest.raises(TypeError) as e:
            Connection(meta_header=1)
        assert str(e.value) == "meta_header must be of type bool"

    def test_compatibility_accept_header(self):
        try:
            conn = Connection()
            assert "accept" not in conn.headers
            os.environ["ELASTIC_CLIENT_APIVERSIONING"] = "0"
            conn = Connection()
            assert "accept" not in conn.headers
            os.environ["ELASTIC_CLIENT_APIVERSIONING"] = "1"
            conn = Connection()
            assert (
                conn.headers["accept"]
                == "application/vnd.elasticsearch+json;compatible-with=8"
            )
        finally:
            os.environ.pop("ELASTIC_CLIENT_APIVERSIONING")


class TestUrllib3Connection:
    def get_mock_urllib3_connection(self, connection_params={}, response_body=b"{}"):
        conn = Urllib3HttpConnection(**connection_params)

        def _dummy_urlopen(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = HTTPHeaderDict({})
            dummy_response.status = 200
            dummy_response.data = response_body
            _dummy_urlopen.call_args = (args, kwargs)
            return dummy_response

        conn.pool.urlopen = _dummy_urlopen
        return conn

    def test_ssl_context(self):
        try:
            context = ssl.create_default_context()
        except AttributeError:
            # if create_default_context raises an AttributeError exception
            # it means SSLContext is not available for that version of python
            # and we should skip this test.
            pytest.skip(
                "test_ssl_context is skipped cause SSLContext is not available for this version of python"
            )

        conn = Urllib3HttpConnection(use_ssl=True, ssl_context=context)
        assert len(conn.pool.conn_kw.keys()) == 1
        assert isinstance(conn.pool.conn_kw["ssl_context"], ssl.SSLContext)
        assert conn.use_ssl

    def test_opaque_id(self):
        conn = Urllib3HttpConnection(opaque_id="app-1")
        assert conn.headers["x-opaque-id"] == "app-1"

    def test_http_cloud_id(self):
        conn = Urllib3HttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng=="
        )
        assert conn.use_ssl
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        assert conn.port is None
        assert (
            conn.hostname == "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        assert conn.http_compress
        conn = Urllib3HttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            port=9243,
        )
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io:9243"
        )
        assert conn.port == 9243
        assert (
            conn.hostname == "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

    def test_api_key_auth(self):
        # test with tuple
        conn = Urllib3HttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key=("elastic", "changeme1"),
        )
        assert conn.headers["authorization"] == "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTE="
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        conn = Urllib3HttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key="ZWxhc3RpYzpjaGFuZ2VtZTI=",
        )
        assert conn.headers["authorization"] == "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTI="
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

    def test_no_http_compression(self):
        conn = self.get_mock_urllib3_connection()
        assert not conn.http_compress
        assert "accept-encoding" not in conn.headers
        conn.perform_request("GET", "/")
        (_, _, req_body), kwargs = conn.pool.urlopen.call_args
        assert not req_body
        assert "accept-encoding" not in kwargs["headers"]
        assert "content-encoding" not in kwargs["headers"]

    def test_http_compression(self):
        conn = self.get_mock_urllib3_connection({"http_compress": True})
        assert conn.http_compress
        assert conn.headers["accept-encoding"] == "gzip,deflate"
        assert "content-encoding" not in conn.headers
        conn.perform_request("GET", "/", body=b"{}")
        (_, _, req_body), kwargs = conn.pool.urlopen.call_args
        assert gzip_decompress(req_body) == b"{}"
        assert kwargs["headers"]["accept-encoding"] == "gzip,deflate"
        assert kwargs["headers"]["content-encoding"] == "gzip"
        conn.perform_request("GET", "/")
        (_, _, req_body), kwargs = conn.pool.urlopen.call_args
        assert not req_body
        assert kwargs["headers"]["accept-encoding"] == "gzip,deflate"
        assert "content-encoding" not in kwargs["headers"]

    def test_cloud_id_http_compress_override(self):
        # 'http_compress' will be 'True' by default for connections with
        # 'cloud_id' set but should prioritize user-defined values.
        conn = Urllib3HttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )
        assert conn.http_compress is True
        conn = Urllib3HttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=False,
        )
        assert conn.http_compress is False
        conn = Urllib3HttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=True,
        )
        assert conn.http_compress is True

    def test_default_user_agent(self):
        conn = Urllib3HttpConnection()
        assert conn._get_default_user_agent() == "elasticsearch-py/%s (Python %s)" % (
            __versionstr__,
            python_version(),
        )

    def test_timeout_set(self):
        conn = Urllib3HttpConnection(timeout=42)
        assert 42 == conn.timeout

    def test_keep_alive_is_on_by_default(self):
        conn = Urllib3HttpConnection()
        assert {
            "connection": "keep-alive",
            "content-type": "application/json",
            "user-agent": conn._get_default_user_agent(),
        } == conn.headers

    def test_http_auth(self):
        conn = Urllib3HttpConnection(http_auth="username:secret")
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "connection": "keep-alive",
            "content-type": "application/json",
            "user-agent": conn._get_default_user_agent(),
        } == conn.headers

    def test_http_auth_tuple(self):
        conn = Urllib3HttpConnection(http_auth=("username", "secret"))
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "content-type": "application/json",
            "connection": "keep-alive",
            "user-agent": conn._get_default_user_agent(),
        } == conn.headers

    def test_http_auth_list(self):
        conn = Urllib3HttpConnection(http_auth=["username", "secret"])
        assert {
            "authorization": "Basic dXNlcm5hbWU6c2VjcmV0",
            "content-type": "application/json",
            "connection": "keep-alive",
            "user-agent": conn._get_default_user_agent(),
        } == conn.headers

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            conn = Urllib3HttpConnection(use_ssl=True, verify_certs=False)
            assert 1 == len(w)
            assert (
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure."
                == str(w[0].message)
            )

            assert isinstance(conn.pool, urllib3.HTTPSConnectionPool)

    def test_nowarn_when_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            conn = Urllib3HttpConnection(
                use_ssl=True, verify_certs=False, ssl_show_warn=False
            )
            assert 0 == len(w)

            assert isinstance(conn.pool, urllib3.HTTPSConnectionPool)

    def test_doesnt_use_https_if_not_specified(self):
        conn = Urllib3HttpConnection()
        assert isinstance(conn.pool, urllib3.HTTPConnectionPool)

    def test_no_warning_when_using_ssl_context(self):
        ctx = ssl.create_default_context()
        with warnings.catch_warnings(record=True) as w:
            Urllib3HttpConnection(ssl_context=ctx)
            assert 0 == len(w)

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
            assert 1 == len(w)
            assert (
                "When using `ssl_context`, all other SSL related kwargs are ignored"
                == str(w[0].message)
            )

    @patch("elasticsearch.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        conn = self.get_mock_urllib3_connection(
            connection_params={"http_compress": True}
        )
        conn.perform_request("GET", "/", body=b'{"example": "body"}')
        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list
        assert '> {"example": "body"}' == req[0][0] % req[0][1:]
        assert "< {}" == resp[0][0] % resp[0][1:]

    def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        conn = self.get_mock_urllib3_connection(response_body=buf)
        status, headers, data = conn.perform_request("GET", "/")
        assert u"你好\uda6a" == data

    @pytest.mark.skipif(
        not reraise_exceptions, reason="RecursionError isn't defined in Python <3.5"
    )
    def test_recursion_error_reraised(self):
        conn = Urllib3HttpConnection()

        def urlopen_raise(*_, **__):
            raise RecursionError("Wasn't modified!")

        conn.pool.urlopen = urlopen_raise
        with pytest.raises(RecursionError) as e:
            conn.perform_request("GET", "/")
        assert str(e.value) == "Wasn't modified!"


class TestRequestsConnection:
    def get_mock_requests_connection(
        self, connection_params={}, status_code=200, response_body=b"{}"
    ):
        conn = RequestsHttpConnection(**connection_params)

        def _dummy_send(*args, **kwargs):
            dummy_response = Mock()
            dummy_response.headers = {}
            dummy_response.status_code = status_code
            dummy_response.content = response_body
            dummy_response.request = args[0]
            dummy_response.cookies = {}
            _dummy_send.call_args = (args, kwargs)
            return dummy_response

        conn.session.send = _dummy_send
        return conn

    def _get_request(self, connection, *args, **kwargs):
        if "body" in kwargs:
            kwargs["body"] = kwargs["body"].encode("utf-8")

        status, headers, data = connection.perform_request(*args, **kwargs)
        assert 200 == status
        assert "{}" == data
        timeout = kwargs.pop("timeout", connection.timeout)
        args, kwargs = connection.session.send.call_args
        assert timeout == kwargs["timeout"]
        assert 1 == len(args)
        return args[0]

    def test_custom_http_auth_is_allowed(self):
        auth = AuthBase()
        c = RequestsHttpConnection(http_auth=auth)
        assert auth == c.session.auth

    def test_timeout_set(self):
        conn = RequestsHttpConnection(timeout=42)
        assert 42 == conn.timeout

    def test_opaque_id(self):
        conn = RequestsHttpConnection(opaque_id="app-1")
        assert conn.headers["x-opaque-id"] == "app-1"

    def test_http_cloud_id(self):
        conn = RequestsHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng=="
        )
        assert conn.use_ssl
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        assert conn.port is None
        assert (
            conn.hostname == "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        assert conn.http_compress
        conn = RequestsHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            port=9243,
        )
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io:9243"
        )
        assert conn.port == 9243
        assert (
            conn.hostname == "4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

    def test_api_key_auth(self):
        # test with tuple
        conn = RequestsHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key=("elastic", "changeme1"),
        )
        assert (
            conn.session.headers["authorization"] == "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTE="
        )
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )
        conn = RequestsHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            api_key="ZWxhc3RpYzpjaGFuZ2VtZTI=",
        )
        assert (
            conn.session.headers["authorization"] == "ApiKey ZWxhc3RpYzpjaGFuZ2VtZTI="
        )
        assert (
            conn.host
            == "https://4fa8821e75634032bed1cf22110e2f97.us-east-1.aws.found.io"
        )

    def test_no_http_compression(self):
        conn = self.get_mock_requests_connection()
        assert not conn.http_compress
        assert "content-encoding" not in conn.session.headers
        conn.perform_request("GET", "/")

        req = conn.session.send.call_args[0][0]
        assert "content-encoding" not in req.headers
        assert "accept-encoding" not in req.headers

    def test_http_compression(self):
        conn = self.get_mock_requests_connection(
            {"http_compress": True},
        )
        assert conn.http_compress
        assert "content-encoding" not in conn.session.headers
        conn.perform_request("GET", "/", body=b"{}")

        req = conn.session.send.call_args[0][0]
        assert req.headers["content-encoding"] == "gzip"
        assert req.headers["accept-encoding"] == "gzip,deflate"
        conn.perform_request("GET", "/")

        req = conn.session.send.call_args[0][0]
        assert "content-encoding" not in req.headers
        assert req.headers["accept-encoding"] == "gzip,deflate"

    def test_cloud_id_http_compress_override(self):
        # 'http_compress' will be 'True' by default for connections with
        # 'cloud_id' set but should prioritize user-defined values.
        conn = RequestsHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )
        assert conn.http_compress is True
        conn = RequestsHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=False,
        )
        assert conn.http_compress is False
        conn = RequestsHttpConnection(
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
            http_compress=True,
        )
        assert conn.http_compress is True

    def test_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            conn = self.get_mock_requests_connection(
                {"use_ssl": True, "url_prefix": "url", "verify_certs": False}
            )
            assert 1 == len(w)
            assert (
                "Connecting to https://localhost:9200 using SSL with verify_certs=False is insecure."
                == str(w[0].message)
            )

            request = self._get_request(conn, "GET", "/")
        assert "https://localhost:9200/url/" == request.url
        assert "GET" == request.method
        assert request.body is None

    def test_nowarn_when_uses_https_if_verify_certs_is_off(self):
        with warnings.catch_warnings(record=True) as w:
            conn = self.get_mock_requests_connection(
                {
                    "use_ssl": True,
                    "url_prefix": "url",
                    "verify_certs": False,
                    "ssl_show_warn": False,
                }
            )
            assert 0 == len(w)

            request = self._get_request(conn, "GET", "/")
        assert "https://localhost:9200/url/" == request.url
        assert "GET" == request.method
        assert request.body is None

    def test_merge_headers(self):
        conn = self.get_mock_requests_connection(
            connection_params={"headers": {"h1": "v1", "h2": "v2"}}
        )
        req = self._get_request(conn, "GET", "/", headers={"h2": "v2p", "h3": "v3"})
        assert req.headers["h1"] == "v1"
        assert req.headers["h2"] == "v2p"
        assert req.headers["h3"] == "v3"

    def test_default_headers(self):
        conn = self.get_mock_requests_connection()
        req = self._get_request(conn, "GET", "/")
        assert req.headers["content-type"] == "application/json"
        assert req.headers["user-agent"] == conn._get_default_user_agent()

    def test_custom_headers(self):
        conn = self.get_mock_requests_connection()
        req = self._get_request(
            conn,
            "GET",
            "/",
            headers={
                "content-type": "application/x-ndjson",
                "user-agent": "custom-agent/1.2.3",
            },
        )
        assert req.headers["content-type"] == "application/x-ndjson"
        assert req.headers["user-agent"] == "custom-agent/1.2.3"

    def test_http_auth(self):
        conn = RequestsHttpConnection(http_auth="username:secret")
        assert ("username", "secret") == conn.session.auth

    def test_http_auth_tuple(self):
        conn = RequestsHttpConnection(http_auth=("username", "secret"))
        assert ("username", "secret") == conn.session.auth

    def test_http_auth_list(self):
        conn = RequestsHttpConnection(http_auth=["username", "secret"])
        assert ("username", "secret") == conn.session.auth

    def test_repr(self):
        conn = self.get_mock_requests_connection(
            {"host": "elasticsearch.com", "port": 443}
        )
        assert "<RequestsHttpConnection: http://elasticsearch.com:443>" == repr(conn)

    def test_conflict_error_is_returned_on_409(self):
        conn = self.get_mock_requests_connection(status_code=409)
        with pytest.raises(ConflictError):
            conn.perform_request("GET", "/", {}, "")

    def test_not_found_error_is_returned_on_404(self):
        conn = self.get_mock_requests_connection(status_code=404)
        with pytest.raises(NotFoundError):
            conn.perform_request("GET", "/", {}, "")

    def test_request_error_is_returned_on_400(self):
        conn = self.get_mock_requests_connection(status_code=400)
        with pytest.raises(RequestError):
            conn.perform_request("GET", "/", {}, "")

    @patch("elasticsearch.connection.base.logger")
    def test_head_with_404_doesnt_get_logged(self, logger):
        conn = self.get_mock_requests_connection(status_code=404)
        with pytest.raises(NotFoundError):
            conn.perform_request("HEAD", "/", {}, "")
        assert 0 == logger.warning.call_count

    @patch("elasticsearch.connection.base.tracer")
    @patch("elasticsearch.connection.base.logger")
    def test_failed_request_logs_and_traces(self, logger, tracer):
        conn = self.get_mock_requests_connection(
            response_body=b'{"answer": 42}', status_code=500
        )
        with pytest.raises(TransportError):
            conn.perform_request(
                "GET",
                "/",
                {"param": 42},
                "{}".encode("utf-8"),
            )
        assert 1 == tracer.info.call_count
        assert 1 == tracer.debug.call_count
        assert 1 == logger.warning.call_count
        assert re.match(
            r"^GET http://localhost:9200/\?param=42 \[status:500 request:0.[0-9]{3}s\]",
            logger.warning.call_args[0][0] % logger.warning.call_args[0][1:],
        )

    @patch("elasticsearch.connection.base.tracer")
    @patch("elasticsearch.connection.base.logger")
    def test_success_logs_and_traces(self, logger, tracer):
        conn = self.get_mock_requests_connection(
            response_body=b"""{"answer": "that's it!"}"""
        )
        status, headers, data = conn.perform_request(
            "GET",
            "/",
            {"param": 42},
            """{"question": "what's that?"}""".encode("utf-8"),
        )
        assert 1 == tracer.info.call_count
        assert (
            """curl -H 'Content-Type: application/json' -XGET 'http://localhost:9200/?pretty&param=42' -d '{\n  "question": "what\\u0027s that?"\n}'"""
            == tracer.info.call_args[0][0] % tracer.info.call_args[0][1:]
        )
        assert 1 == tracer.debug.call_count
        assert re.match(
            r'#\[200\] \(0.[0-9]{3}s\)\n#{\n#  "answer": "that\\u0027s it!"\n#}',
            tracer.debug.call_args[0][0] % tracer.debug.call_args[0][1:],
        )
        assert 1 == logger.info.call_count
        assert re.match(
            r"GET http://localhost:9200/\?param=42 \[status:200 request:0.[0-9]{3}s\]",
            logger.info.call_args[0][0] % logger.info.call_args[0][1:],
        )
        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list
        assert '> {"question": "what\'s that?"}' == req[0][0] % req[0][1:]
        assert '< {"answer": "that\'s it!"}' == resp[0][0] % resp[0][1:]

    @patch("elasticsearch.connection.base.logger")
    def test_uncompressed_body_logged(self, logger):
        conn = self.get_mock_requests_connection(
            connection_params={"http_compress": True}
        )
        conn.perform_request("GET", "/", body=b'{"example": "body"}')
        assert 2 == logger.debug.call_count
        req, resp = logger.debug.call_args_list
        assert '> {"example": "body"}' == req[0][0] % req[0][1:]
        assert "< {}" == resp[0][0] % resp[0][1:]
        conn = self.get_mock_requests_connection(
            connection_params={"http_compress": True},
            status_code=500,
            response_body=b'{"hello":"world"}',
        )
        with pytest.raises(TransportError):
            conn.perform_request("GET", "/", body=b'{"example": "body2"}')

        assert 4 == logger.debug.call_count
        _, _, req, resp = logger.debug.call_args_list
        assert '> {"example": "body2"}' == req[0][0] % req[0][1:]
        assert '< {"hello":"world"}' == resp[0][0] % resp[0][1:]

    def test_defaults(self):
        conn = self.get_mock_requests_connection()
        request = self._get_request(conn, "GET", "/")
        assert "http://localhost:9200/" == request.url
        assert "GET" == request.method
        assert request.body is None

    def test_params_properly_encoded(self):
        conn = self.get_mock_requests_connection()
        request = self._get_request(
            conn, "GET", "/", params={"param": "value with spaces"}
        )
        assert "http://localhost:9200/?param=value+with+spaces" == request.url
        assert "GET" == request.method
        assert request.body is None

    def test_body_attached(self):
        conn = self.get_mock_requests_connection()
        request = self._get_request(conn, "GET", "/", body='{"answer": 42}')
        assert "http://localhost:9200/" == request.url
        assert "GET" == request.method
        assert '{"answer": 42}'.encode("utf-8") == request.body

    def test_http_auth_attached(self):
        conn = self.get_mock_requests_connection({"http_auth": "username:secret"})
        request = self._get_request(conn, "GET", "/")
        assert request.headers["authorization"] == "Basic dXNlcm5hbWU6c2VjcmV0"

    @patch("elasticsearch.connection.base.tracer")
    def test_url_prefix(self, tracer):
        conn = self.get_mock_requests_connection({"url_prefix": "/some-prefix/"})
        request = self._get_request(
            conn, "GET", "/_search", body='{"answer": 42}', timeout=0.1
        )
        assert "http://localhost:9200/some-prefix/_search" == request.url
        assert "GET" == request.method
        assert '{"answer": 42}'.encode("utf-8") == request.body
        assert 1 == tracer.info.call_count
        assert (
            "curl -H 'Content-Type: application/json' -XGET 'http://localhost:9200/_search?pretty' -d '{\n  \"answer\": 42\n}'"
            == tracer.info.call_args[0][0] % tracer.info.call_args[0][1:]
        )

    def test_surrogatepass_into_bytes(self):
        buf = b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"
        conn = self.get_mock_requests_connection(response_body=buf)
        status, headers, data = conn.perform_request("GET", "/")
        assert u"你好\uda6a" == data

    @pytest.mark.skipif(
        not reraise_exceptions, reason="RecursionError isn't defined in Python <3.5"
    )
    def test_recursion_error_reraised(self):
        conn = RequestsHttpConnection()

        def send_raise(*_, **__):
            raise RecursionError("Wasn't modified!")

        conn.session.send = send_raise

        with pytest.raises(RecursionError) as e:
            conn.perform_request("GET", "/")
        assert str(e.value) == "Wasn't modified!"


class TestConnectionHttpbin:
    """Tests the HTTP connection implementations against a live server E2E"""

    def httpbin_anything(self, conn, **kwargs):
        status, headers, data = conn.perform_request("GET", "/anything", **kwargs)
        data = json.loads(data)
        data["headers"].pop(
            "X-Amzn-Trace-Id", None
        )  # Remove this header as it's put there by AWS.
        return (status, data)

    def test_urllib3_connection(self):
        # Defaults
        conn = Urllib3HttpConnection("httpbin.org", port=443, use_ssl=True)
        user_agent = conn._get_default_user_agent()
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=False
        conn = Urllib3HttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=False
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=True
        conn = Urllib3HttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=True
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # Headers
        conn = Urllib3HttpConnection(
            "httpbin.org",
            port=443,
            use_ssl=True,
            http_compress=True,
            headers={"header1": "value1"},
        )
        status, data = self.httpbin_anything(
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

    def test_urllib3_connection_error(self):
        conn = Urllib3HttpConnection("not.a.host.name")
        with pytest.raises(ConnectionError):
            conn.perform_request("GET", "/")

    def test_requests_connection(self):
        # Defaults
        conn = RequestsHttpConnection("httpbin.org", port=443, use_ssl=True)
        user_agent = conn._get_default_user_agent()
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=False
        conn = RequestsHttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=False
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["method"] == "GET"
        assert data["headers"] == {
            "Accept-Encoding": "identity",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # http_compress=True
        conn = RequestsHttpConnection(
            "httpbin.org", port=443, use_ssl=True, http_compress=True
        )
        status, data = self.httpbin_anything(conn)
        assert status == 200
        assert data["headers"] == {
            "Accept-Encoding": "gzip,deflate",
            "Content-Type": "application/json",
            "Host": "httpbin.org",
            "User-Agent": user_agent,
        }

        # Headers
        conn = RequestsHttpConnection(
            "httpbin.org",
            port=443,
            use_ssl=True,
            http_compress=True,
            headers={"header1": "value1"},
        )
        status, data = self.httpbin_anything(
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

    def test_requests_connection_error(self):
        conn = RequestsHttpConnection("not.a.host.name")
        with pytest.raises(ConnectionError):
            conn.perform_request("GET", "/")

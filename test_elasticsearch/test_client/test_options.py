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

import pytest
from elastic_transport import OpenTelemetrySpan
from elastic_transport.client_utils import DEFAULT

from elasticsearch import AsyncElasticsearch, Elasticsearch
from elasticsearch._sync.client.utils import USER_AGENT
from test_elasticsearch.test_cases import (
    DummyAsyncTransport,
    DummyTransport,
    DummyTransportTestCase,
)


class TestOptions(DummyTransportTestCase):
    def assert_called_with_headers(self, client, method, target, headers):
        calls = client.transport.calls
        assert (method, target) in calls
        called_headers = calls[(method, target)][-1]["headers"].copy()
        for header in (
            "accept",
            "content-type",
        ):  # Common HTTP headers that we're not testing.
            called_headers.pop(header, None)
        assert headers == called_headers

    @pytest.mark.parametrize(
        ["options", "headers"],
        [
            (
                {"headers": {"authorization": "custom method"}},
                {"Authorization": "custom method"},
            ),
            ({"api_key": "key"}, {"Authorization": "ApiKey key"}),
            ({"api_key": ("id", "value")}, {"Authorization": "ApiKey aWQ6dmFsdWU="}),
            (
                {"basic_auth": ("username", "password")},
                {"Authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ="},
            ),
            ({"basic_auth": "encoded"}, {"Authorization": "Basic encoded"}),
            ({"bearer_auth": "bear"}, {"Authorization": "Bearer bear"}),
            (
                {"opaque_id": "test-id"},
                {"X-Opaque-Id": "test-id"},
            ),
            (
                {
                    "opaque_id": "opaq-id",
                    "headers": {"custom": "key"},
                    "api_key": ("id", "val"),
                },
                {
                    "custom": "key",
                    "authorization": "ApiKey aWQ6dmFs",
                    "x-opaque-id": "opaq-id",
                },
            ),
        ],
    )
    def test_options_to_headers(self, options, headers):
        # Tests that authentication works identically from the constructor
        # or from the client.options() API.
        client = self.client.options(**options)
        client.indices.exists(index="test")
        self.assert_called_with_headers(client, "HEAD", "/test", headers=headers)

        client = Elasticsearch(
            "http://localhost:9200", transport_class=DummyTransport, **options
        )
        client.indices.exists(index="test")
        self.assert_called_with_headers(client, "HEAD", "/test", headers=headers)

        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            headers={"Authorization": "not it"},
        )
        client = self.client.options(**options)
        client.indices.exists(index="test")
        self.assert_called_with_headers(client, "HEAD", "/test", headers=headers)

    @pytest.mark.parametrize("api_key", [None, "api-key", ("api", "key")])
    @pytest.mark.parametrize("bearer_auth", [None, "bearer"])
    @pytest.mark.parametrize("basic_auth", [None, "user:pass", ("user", "pass")])
    @pytest.mark.parametrize(
        "headers", [None, {"Authorization": "value"}, {"authorization": "value"}]
    )
    def test_options_auth_conflicts(self, api_key, bearer_auth, basic_auth, headers):
        if sum(x is not None for x in (api_key, bearer_auth, basic_auth, headers)) < 2:
            pytest.skip("Skip the cases where 1 or fewer options are unset")
        kwargs = {
            k: v
            for k, v in {
                "api_key": api_key,
                "bearer_auth": bearer_auth,
                "basic_auth": basic_auth,
                "headers": headers,
            }.items()
            if v is not None
        }

        with pytest.raises(ValueError) as e:
            self.client.options(**kwargs)
        assert str(e.value) in (
            "Can only set one of 'api_key', 'basic_auth', and 'bearer_auth'",
            "Can't set 'Authorization' HTTP header with other authentication options",
        )

    def test_options_passed_to_perform_request(self):
        # Default transport options are 'DEFAULT' to rely on 'elastic_transport' defaults.
        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
        )
        client.indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("request_timeout") is DEFAULT
        assert call.pop("max_retries") is DEFAULT
        assert call.pop("retry_on_timeout") is DEFAULT
        assert call.pop("retry_on_status") is DEFAULT
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
        }

        # Can be overwritten with .options()
        client.options(
            request_timeout=1,
            max_retries=2,
            retry_on_timeout=False,
            retry_on_status=(404,),
        ).indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][1]
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
            "request_timeout": 1,
            "max_retries": 2,
            "retry_on_status": (404,),
            "retry_on_timeout": False,
        }

        # Can be overwritten on constructor
        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            request_timeout=1,
            max_retries=2,
            retry_on_timeout=False,
            retry_on_status=(404,),
        )
        client.indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
            "request_timeout": 1,
            "max_retries": 2,
            "retry_on_status": (404,),
            "retry_on_timeout": False,
        }

    @pytest.mark.asyncio
    async def test_options_passed_to_async_perform_request(self):
        # Default transport options are 'DEFAULT' to rely on 'elastic_transport' defaults.
        client = AsyncElasticsearch(
            "http://localhost:9200",
            transport_class=DummyAsyncTransport,
        )
        await client.indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("request_timeout") is DEFAULT
        assert call.pop("max_retries") is DEFAULT
        assert call.pop("retry_on_timeout") is DEFAULT
        assert call.pop("retry_on_status") is DEFAULT
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
        }

        # Can be overwritten with .options()
        await client.options(
            request_timeout=1,
            max_retries=2,
            retry_on_timeout=False,
            retry_on_status=(404,),
        ).indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][1]
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
            "request_timeout": 1,
            "max_retries": 2,
            "retry_on_status": (404,),
            "retry_on_timeout": False,
        }

        # Can be overwritten on constructor
        client = AsyncElasticsearch(
            "http://localhost:9200",
            transport_class=DummyAsyncTransport,
            request_timeout=1,
            max_retries=2,
            retry_on_timeout=False,
            retry_on_status=(404,),
        )
        await client.indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
            "request_timeout": 1,
            "max_retries": 2,
            "retry_on_status": (404,),
            "retry_on_timeout": False,
        }

    def test_default_node_configs(self):
        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            headers={"key": "val"},
            basic_auth=("username", "password"),
        )
        assert client._headers == {
            "key": "val",
            "authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ=",
        }

        assert len(client.transport.hosts) == 1
        node_config = client.transport.hosts[0]
        assert node_config.scheme == "http"
        assert node_config.host == "localhost"
        assert node_config.port == 9200
        assert node_config.path_prefix == ""
        assert node_config.headers == {"user-agent": USER_AGENT}

    def test_http_headers_overrides(self):
        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            headers={"key": "val"},
        )
        calls = client.transport.calls

        client.indices.get(index="1")
        call = calls[("GET", "/1")][0]

        assert call["headers"] == {
            "key": "val",
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        client.options(headers={"key1": "val"}).indices.get(index="2")
        call = calls[("GET", "/2")][0]

        assert call["headers"] == {
            "key": "val",
            "key1": "val",
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        client.options(headers={"key": "val2"}).indices.get(index="3")
        call = calls[("GET", "/3")][0]

        assert call["headers"] == {
            "key": "val2",
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        client = Elasticsearch(
            "http://username:password@localhost:9200",
            transport_class=DummyTransport,
            headers={"key": "val"},
        )
        calls = client.transport.calls
        node_config = client.transport.hosts[0]
        assert node_config.headers == {
            "authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ=",
            "user-agent": USER_AGENT,
        }
        assert client._headers == {"key": "val"}

    def test_user_agent_override(self):
        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
        )
        calls = client.transport.calls

        client.options(headers={"user-agent": "custom1"}).indices.get(index="1")
        call = calls[("GET", "/1")][0]
        assert call["headers"] == {
            "user-agent": "custom1",
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        client.indices.get(index="2", headers={"user-agent": "custom2"})
        call = calls[("GET", "/2")][0]
        assert call["headers"] == {
            "user-agent": "custom2",
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            headers={"User-Agent": "custom3"},
        )
        calls = client.transport.calls

        client.indices.get(index="1")
        call = calls[("GET", "/1")][0]
        assert call["headers"] == {
            "user-agent": "custom3",
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        client.indices.get(index="2", headers={"user-agent": "custom4"})
        call = calls[("GET", "/2")][0]
        assert call["headers"] == {
            "user-agent": "custom4",
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

    def test_options_timeout_parameters(self):
        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            request_timeout=1,
            max_retries=2,
            retry_on_status=(404,),
            retry_on_timeout=True,
        )

        # timeout parameters are preserved with .options()
        client.options().indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
            "request_timeout": 1,
            "max_retries": 2,
            "retry_on_status": (404,),
            "retry_on_timeout": True,
        }

        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            request_timeout=1,
            max_retries=2,
            retry_on_status=(404,),
            retry_on_timeout=True,
        )
        client.options(
            request_timeout=2,
            max_retries=3,
            retry_on_status=(400,),
            retry_on_timeout=False,
        ).indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
            "request_timeout": 2,
            "max_retries": 3,
            "retry_on_status": (400,),
            "retry_on_timeout": False,
        }

        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
        )
        client.options().indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("request_timeout") is DEFAULT
        assert call.pop("max_retries") is DEFAULT
        assert call.pop("retry_on_timeout") is DEFAULT
        assert call.pop("retry_on_status") is DEFAULT
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
        }

        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
        )
        client.options(
            request_timeout=1,
            max_retries=2,
            retry_on_status=(404,),
            retry_on_timeout=True,
        ).indices.get(index="test")

        calls = client.transport.calls
        call = calls[("GET", "/test")][0]
        assert call.pop("client_meta") is DEFAULT
        assert isinstance(call.pop("otel_span"), OpenTelemetrySpan)
        assert call == {
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "body": None,
            "request_timeout": 1,
            "max_retries": 2,
            "retry_on_status": (404,),
            "retry_on_timeout": True,
        }

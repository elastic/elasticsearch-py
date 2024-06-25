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


import asyncio
import re
import warnings
from typing import Any, Dict, Optional, Union

import pytest
from elastic_transport import (
    ApiResponseMeta,
    BaseAsyncNode,
    HttpHeaders,
    NodeConfig,
    NodePool,
)
from elastic_transport._node import NodeApiResponse
from elastic_transport.client_utils import DEFAULT

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import (
    ApiError,
    ConnectionError,
    ElasticsearchWarning,
    UnsupportedProductError,
)

pytestmark = pytest.mark.asyncio


class DummyNode(BaseAsyncNode):
    def __init__(self, config: NodeConfig):
        self.resp_status = config._extras.pop("status", 200)
        self.resp_error = config._extras.pop("exception", None)
        self.resp_data = config._extras.pop("data", b"{}")
        self.resp_headers = config._extras.pop(
            "headers", {"X-elastic-product": "Elasticsearch"}
        )
        self.calls = []
        self.closed = False

        super().__init__(config)

    async def perform_request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.resp_error:
            raise self.resp_error
        return NodeApiResponse(
            ApiResponseMeta(
                status=self.resp_status,
                headers=HttpHeaders(self.resp_headers),
                http_version="1.1",
                duration=0.0,
                node=self.config,
            ),
            self.resp_data,
        )

    async def close(self):
        if self.closed:
            raise RuntimeError("This connection is already closed")
        self.closed = True


class NoTimeoutConnectionPool(NodePool):
    def mark_dead(self, connection):
        pass

    def mark_live(self, connection):
        pass


CLUSTER_NODES = """{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "elasticsearch",
  "nodes" : {
    "SRZpKFZdQguhhvifmN6UVA" : {
      "name" : "SRZpKFZ",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1",
      "version" : "5.0.0",
      "build_hash" : "253032b",
      "roles" : [ "master", "data", "ingest" ],
      "http" : {
        "bound_address" : [ "[fe80::1]:9200", "[::1]:9200", "127.0.0.1:9200" ],
        "publish_address" : "1.1.1.1:123",
        "max_content_length_in_bytes" : 104857600
      }
    }
  }
}"""

CLUSTER_NODES_7x_PUBLISH_HOST = """{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "elasticsearch",
  "nodes" : {
    "SRZpKFZdQguhhvifmN6UVA" : {
      "name" : "SRZpKFZ",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1",
      "version" : "5.0.0",
      "build_hash" : "253032b",
      "roles" : [ "master", "data", "ingest" ],
      "http" : {
        "bound_address" : [ "[fe80::1]:9200", "[::1]:9200", "127.0.0.1:9200" ],
        "publish_address" : "somehost.tld/1.1.1.1:123",
        "max_content_length_in_bytes" : 104857600
      }
    }
  }
}"""

CLUSTER_NODES_MASTER_ONLY = """{
  "_nodes" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  },
  "cluster_name" : "elasticsearch",
  "nodes" : {
    "SRZpKFZdQguhhvifmN6UVA" : {
      "name" : "SRZpKFZa",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1",
      "version" : "5.0.0",
      "build_hash" : "253032b",
      "roles" : ["master"],
      "http" : {
        "bound_address" : [ "[fe80::1]:9200", "[::1]:9200", "127.0.0.1:9200" ],
        "publish_address" : "somehost.tld/1.1.1.1:123",
        "max_content_length_in_bytes" : 104857600
      }
    },
    "SRZpKFZdQguhhvifmN6UVB" : {
      "name" : "SRZpKFZb",
      "transport_address" : "127.0.0.1:9300",
      "host" : "127.0.0.1",
      "ip" : "127.0.0.1",
      "version" : "5.0.0",
      "build_hash" : "253032b",
      "roles" : [ "master", "data", "ingest" ],
      "http" : {
        "bound_address" : [ "[fe80::1]:9200", "[::1]:9200", "127.0.0.1:9200" ],
        "publish_address" : "somehost.tld/1.1.1.1:124",
        "max_content_length_in_bytes" : 104857600
      }
    }
  }
}"""


class TestTransport:
    async def test_request_timeout_extracted_from_params_and_passed(self):
        client = AsyncElasticsearch(
            "http://localhost:9200", meta_header=False, node_class=DummyNode
        )

        await client.info(params={"request_timeout": 42})
        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][0] == ("GET", "/")
        assert calls[0][1]["request_timeout"] == 42

    async def test_opaque_id(self):
        client = AsyncElasticsearch(
            "http://localhost:9200",
            meta_header=False,
            node_class=DummyNode,
            opaque_id="app-1",
        )

        await client.info()
        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][0] == ("GET", "/")
        assert calls[0][1]["headers"]["x-opaque-id"] == "app-1"

        # Now try with an 'x-opaque-id' set on perform_request().
        await client.info(opaque_id="request-2")
        calls = client.transport.node_pool.get().calls
        assert 2 == len(calls)
        assert calls[1][0] == ("GET", "/")
        assert calls[1][1]["headers"]["x-opaque-id"] == "request-2"

    async def test_request_with_custom_user_agent_header(self):
        client = AsyncElasticsearch(
            "http://localhost:9200", meta_header=False, node_class=DummyNode
        )

        await client.info(headers={"User-Agent": "my-custom-value/1.2.3"})
        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][0] == ("GET", "/")
        assert calls[0][1]["headers"]["user-agent"] == "my-custom-value/1.2.3"

    async def test_client_meta_header(self):
        client = AsyncElasticsearch("http://localhost:9200", node_class=DummyNode)
        await client.info()

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        headers = calls[0][1]["headers"]
        assert re.search(
            r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?$", headers["x-elastic-client-meta"]
        )

        class DummyNodeWithMeta(DummyNode):
            _CLIENT_META_HTTP_CLIENT = ("dm", "1.2.3")

        client = AsyncElasticsearch(
            "http://localhost:9200", node_class=DummyNodeWithMeta
        )
        await client.info(headers={"CustoM": "header"})

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        headers = calls[0][1]["headers"]
        assert re.search(
            r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?,dm=1.2.3$",
            headers["x-elastic-client-meta"],
        )
        assert headers["Custom"] == "header"

    async def test_client_meta_header_not_sent(self):
        client = AsyncElasticsearch(
            "http://localhost:9200", meta_header=False, node_class=DummyNode
        )
        await client.info()

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][1]["headers"] == {
            "accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

    async def test_body_surrogates_replaced_encoded_into_bytes(self):
        client = AsyncElasticsearch("http://localhost:9200", node_class=DummyNode)

        await client.search(query={"match": "你好\uda6a"})

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert (
            calls[0][1]["body"]
            == b'{"query":{"match":"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"}}'
        )

    def test_kwargs_passed_on_to_node_pool(self):
        dt = object()
        client = AsyncElasticsearch(
            "http://localhost:9200", dead_node_backoff_factor=dt
        )
        assert dt is client.transport.node_pool.dead_node_backoff_factor

        class MyConnection:
            def __init__(self, *_, **__):
                pass

            async def perform_request(*_, **__):
                pass

        client = AsyncElasticsearch("http://localhost:9200", node_class=MyConnection)
        assert 1 == len(client.transport.node_pool)
        assert isinstance(client.transport.node_pool.all()[0], MyConnection)

    async def test_request_will_fail_after_x_retries(self):
        client = AsyncElasticsearch(
            [
                NodeConfig(
                    "http",
                    "localhost",
                    9200,
                    _extras={"exception": ConnectionError("abandon ship!")},
                )
            ],
            node_class=DummyNode,
        )

        with pytest.raises(ConnectionError) as e:
            await client.info()
        calls = client.transport.node_pool.get().calls
        assert 4 == len(calls)
        assert len(e.value.errors) == 3
        del calls[:]

        with pytest.raises(ConnectionError):
            await client.options(max_retries=5).info()
        calls = client.transport.node_pool.get().calls
        assert 6 == len(calls)

    async def test_failed_connection_will_be_marked_as_dead(self):
        client = AsyncElasticsearch(
            [
                NodeConfig(
                    "http",
                    "localhost",
                    9200,
                    _extras={"exception": ConnectionError("abandon ship!")},
                ),
                NodeConfig(
                    "http",
                    "localhost",
                    9201,
                    _extras={"exception": ConnectionError("abandon ship!")},
                ),
            ],
            node_class=DummyNode,
        )

        with pytest.raises(ConnectionError):
            await client.info()
        assert 0 == len(client.transport.node_pool._alive_nodes)

    async def test_resurrected_connection_will_be_marked_as_live_on_success(self):
        client = AsyncElasticsearch(
            [
                NodeConfig("http", "localhost", 9200),
                NodeConfig("http", "localhost", 9201),
            ],
            node_class=DummyNode,
        )
        node1 = client.transport.node_pool.get()
        node2 = client.transport.node_pool.get()
        assert node1 is not node2
        client.transport.node_pool.mark_dead(node1)
        client.transport.node_pool.mark_dead(node2)
        assert len(client.transport.node_pool._alive_nodes) == 0

        await client.info()

        assert len(client.transport.node_pool._alive_nodes) == 1
        assert len(client.transport.node_pool._dead_consecutive_failures) == 1

    async def test_override_mark_dead_mark_live(self):
        client = AsyncElasticsearch(
            [
                NodeConfig("http", "localhost", 9200),
                NodeConfig("http", "localhost", 9201),
            ],
            node_class=DummyNode,
            node_pool_class=NoTimeoutConnectionPool,
        )
        node1 = client.transport.node_pool.get()
        node2 = client.transport.node_pool.get()
        assert node1 is not node2
        client.transport.node_pool.mark_dead(node1)
        client.transport.node_pool.mark_dead(node2)
        assert len(client.transport.node_pool._alive_nodes) == 2

        await client.info()

        assert len(client.transport.node_pool._alive_nodes) == 2
        assert len(client.transport.node_pool._dead_consecutive_failures) == 0

    @pytest.mark.parametrize(
        ["nodes_info_response", "node_host"],
        [(CLUSTER_NODES, "1.1.1.1"), (CLUSTER_NODES_7x_PUBLISH_HOST, "somehost.tld")],
    )
    async def test_sniff_will_use_seed_connections(
        self, nodes_info_response, node_host
    ):
        client = AsyncElasticsearch(
            [
                NodeConfig(
                    "http", "localhost", 9200, _extras={"data": nodes_info_response}
                )
            ],
            node_class=DummyNode,
            sniff_on_start=True,
        )

        # Async sniffing happens in the background.
        await client.transport._async_call()
        assert client.transport._sniffing_task is not None
        await client.transport._sniffing_task

        node_configs = [node.config for node in client.transport.node_pool.all()]
        assert len(node_configs) == 2
        assert NodeConfig("http", node_host, 123) in node_configs

    async def test_sniff_on_start_ignores_sniff_timeout(self):
        client = AsyncElasticsearch(
            [NodeConfig("http", "localhost", 9200, _extras={"data": CLUSTER_NODES})],
            node_class=DummyNode,
            sniff_on_start=True,
            sniff_timeout=12,
            meta_header=False,
        )

        # Async sniffing happens in the background.
        await client.transport._async_call()
        assert client.transport._sniffing_task is not None
        await client.transport._sniffing_task

        calls = client.transport.node_pool.all()[0].calls

        assert len(calls) == 1
        assert calls[0] == (
            ("GET", "/_nodes/_all/http"),
            {
                "body": None,
                "headers": {
                    "accept": "application/vnd.elasticsearch+json; compatible-with=8"
                },
                "request_timeout": None,  # <-- Should be None instead of 12
            },
        )

    async def test_sniff_uses_sniff_timeout(self):
        client = AsyncElasticsearch(
            [NodeConfig("http", "localhost", 9200, _extras={"data": CLUSTER_NODES})],
            node_class=DummyNode,
            sniff_before_requests=True,
            sniff_timeout=12,
            meta_header=False,
        )
        await client.info()

        # Async sniffing happens in the background.
        assert client.transport._sniffing_task is not None
        await client.transport._sniffing_task

        calls = client.transport.node_pool.all()[0].calls

        assert len(calls) == 2
        assert calls[0] == (
            ("GET", "/"),
            {
                "body": None,
                "headers": {
                    "accept": "application/vnd.elasticsearch+json; compatible-with=8",
                },
                "request_timeout": DEFAULT,
            },
        )
        assert calls[1] == (
            ("GET", "/_nodes/_all/http"),
            {
                "body": None,
                "headers": {
                    "accept": "application/vnd.elasticsearch+json; compatible-with=8"
                },
                "request_timeout": 12,
            },
        )

    async def test_sniff_on_start_awaits_before_request(self):
        client = AsyncElasticsearch(
            [NodeConfig("http", "localhost", 9200, _extras={"data": CLUSTER_NODES})],
            node_class=DummyNode,
            sniff_on_start=True,
            sniff_timeout=12,
            meta_header=False,
        )

        await client.info()

        calls = client.transport.node_pool.all()[0].calls

        assert len(calls) == 2
        # The sniff request happens first.
        assert calls[0][0] == ("GET", "/_nodes/_all/http")
        assert calls[1][0] == ("GET", "/")

    async def test_sniff_reuses_node_instances(self):
        client = AsyncElasticsearch(
            [NodeConfig("http", "1.1.1.1", 123, _extras={"data": CLUSTER_NODES})],
            node_class=DummyNode,
            sniff_on_start=True,
        )

        assert len(client.transport.node_pool) == 1
        await client.info()
        assert len(client.transport.node_pool) == 1

    @pytest.mark.parametrize(
        ["extra_key", "extra_value"],
        [("exception", ConnectionError("Abandon ship!")), ("status", 500)],
    )
    async def test_sniff_on_node_failure_triggers(self, extra_key, extra_value):
        client = AsyncElasticsearch(
            [
                NodeConfig("http", "localhost", 9200, _extras={extra_key: extra_value}),
                NodeConfig("http", "localhost", 9201, _extras={"data": CLUSTER_NODES}),
            ],
            node_class=DummyNode,
            sniff_on_node_failure=True,
            randomize_nodes_in_pool=False,
            max_retries=0,
        )

        request_failed_in_error = False
        try:
            await client.info()
        except (ConnectionError, ApiError):
            request_failed_in_error = True

        assert client.transport._sniffing_task is not None
        await client.transport._sniffing_task

        assert request_failed_in_error
        assert len(client.transport.node_pool) == 3

    async def test_sniff_after_n_seconds(self, event_loop):
        client = AsyncElasticsearch(  # noqa: F821
            [NodeConfig("http", "localhost", 9200, _extras={"data": CLUSTER_NODES})],
            node_class=DummyNode,
            min_delay_between_sniffing=5,
        )
        client.transport._last_sniffed_at = event_loop.time()

        await client.info()

        for _ in range(4):
            await client.info()
            await asyncio.sleep(0)

        assert 1 == len(client.transport.node_pool)

        client.transport._last_sniffed_at = event_loop.time() - 5.1

        await client.info()
        await client.transport._sniffing_task  # Need to wait for the sniffing task to complete

        assert 2 == len(client.transport.node_pool)
        assert "http://1.1.1.1:123" in (
            node.base_url for node in client.transport.node_pool.all()
        )
        assert (
            event_loop.time() - 1
            < client.transport._last_sniffed_at
            < event_loop.time() + 0.01
        )

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"sniff_on_start": True},
            {"sniff_on_connection_fail": True},
            {"sniff_on_node_failure": True},
            {"sniff_before_requests": True},
            {"sniffer_timeout": 1},
            {"sniff_timeout": 1},
        ],
    )
    async def test_sniffing_disabled_on_elastic_cloud(self, kwargs):
        with pytest.raises(ValueError) as e:
            AsyncElasticsearch(
                cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
                **kwargs,
            )

        assert (
            str(e.value)
            == "Sniffing should not be enabled when connecting to Elastic Cloud"
        )

    async def test_sniff_on_start_close_unlocks_async_calls(self, event_loop):
        client = AsyncElasticsearch(  # noqa: F821
            [
                NodeConfig(
                    "http",
                    "localhost",
                    9200,
                    _extras={"delay": 10, "data": CLUSTER_NODES},
                ),
            ],
            node_class=DummyNode,
            sniff_on_start=True,
        )

        # Start making _async_calls() before we cancel
        tasks = []
        start_time = event_loop.time()
        for _ in range(3):
            tasks.append(event_loop.create_task(client.info()))
            await asyncio.sleep(0)

        # Close the transport while the sniffing task is active! :(
        await client.transport.close()

        # Now we start waiting on all those _async_calls()
        await asyncio.gather(*tasks)
        end_time = event_loop.time()
        duration = end_time - start_time

        # A lot quicker than 10 seconds defined in 'delay'
        assert duration < 1

    async def test_sniffing_master_only_filtered_by_default(self):
        client = AsyncElasticsearch(  # noqa: F821
            [
                NodeConfig(
                    "http",
                    "localhost",
                    9200,
                    _extras={"data": CLUSTER_NODES_MASTER_ONLY},
                )
            ],
            node_class=DummyNode,
            sniff_on_start=True,
        )
        await client.transport._async_call()

        assert len(client.transport.node_pool) == 2

    async def test_sniff_node_callback(self):
        def sniffed_node_callback(
            node_info: Dict[str, Any], node_config: NodeConfig
        ) -> Optional[NodeConfig]:
            return (
                node_config
                if node_info["http"]["publish_address"].endswith(":124")
                else None
            )

        client = AsyncElasticsearch(  # noqa: F821
            [
                NodeConfig(
                    "http",
                    "localhost",
                    9200,
                    _extras={"data": CLUSTER_NODES_MASTER_ONLY},
                )
            ],
            node_class=DummyNode,
            sniff_on_start=True,
            sniffed_node_callback=sniffed_node_callback,
        )
        await client.transport._async_call()

        assert len(client.transport.node_pool) == 2

        ports = {node.config.port for node in client.transport.node_pool.all()}
        assert ports == {9200, 124}

    async def test_sniffing_deprecated_host_info_callback(self):
        def host_info_callback(
            node_info: Dict[str, Any], host: Dict[str, Union[int, str]]
        ) -> Dict[str, Any]:
            return (
                host if node_info["http"]["publish_address"].endswith(":124") else None
            )

        with warnings.catch_warnings(record=True) as w:
            client = AsyncElasticsearch(  # noqa: F821
                [
                    NodeConfig(
                        "http",
                        "localhost",
                        9200,
                        _extras={"data": CLUSTER_NODES_MASTER_ONLY},
                    )
                ],
                node_class=DummyNode,
                sniff_on_start=True,
                host_info_callback=host_info_callback,
            )
            await client.transport._async_call()

        assert len(w) == 1
        assert w[0].category == DeprecationWarning
        assert (
            str(w[0].message)
            == "The 'host_info_callback' parameter is deprecated in favor of 'sniffed_node_callback'"
        )

        assert len(client.transport.node_pool) == 2

        ports = {node.config.port for node in client.transport.node_pool.all()}
        assert ports == {9200, 124}


@pytest.mark.parametrize("headers", [{}, {"X-elastic-product": "BAD HEADER"}])
async def test_unsupported_product_error(headers):
    client = AsyncElasticsearch(
        [NodeConfig("http", "localhost", 9200, _extras={"headers": headers})],
        meta_header=False,
        node_class=DummyNode,
    )

    with pytest.raises(UnsupportedProductError) as e:
        await client.info()
    assert str(e.value) == (
        "The client noticed that the server is not Elasticsearch "
        "and we do not support this unknown product"
    )

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1
    assert calls[0] == (
        ("GET", "/"),
        {
            "body": None,
            "headers": {
                "accept": "application/vnd.elasticsearch+json; compatible-with=8",
            },
            "request_timeout": DEFAULT,
        },
    )


@pytest.mark.parametrize("status", [401, 403, 413, 500])
async def test_unsupported_product_error_not_raised_on_non_2xx(status):
    client = AsyncElasticsearch(
        [
            NodeConfig(
                "http", "localhost", 9200, _extras={"headers": {}, "status": status}
            )
        ],
        meta_header=False,
        node_class=DummyNode,
    )
    try:
        await client.info()
    except UnsupportedProductError:
        assert False, "Raised UnsupportedProductError"
    except ApiError as e:
        assert e.meta.status == status


@pytest.mark.parametrize("status", [404, 500])
async def test_api_error_raised_before_product_error(status):
    client = AsyncElasticsearch(
        [
            NodeConfig(
                "http",
                "localhost",
                9200,
                _extras={
                    "headers": {"X-elastic-product": "BAD HEADER"},
                    "status": status,
                },
            )
        ],
        meta_header=False,
        node_class=DummyNode,
    )

    with pytest.raises(ApiError) as e:
        await client.info()
    assert e.value.status_code == status
    assert not isinstance(e.value, UnsupportedProductError)

    calls = client.transport.node_pool.get().calls
    assert len(calls) == 1
    assert calls[0][0] == ("GET", "/")


@pytest.mark.parametrize(
    "headers",
    [
        {
            "Warning": '299 Elasticsearch-8.0.0-SNAPSHOT-ad975cacd240b3329e160673c432e768dcd7899a "[xpack.monitoring.history.duration] setting was deprecated in Elasticsearch and will be removed in a future release! See the breaking changes documentation for the next major version."',
            "X-elastic-product": "Elasticsearch",
        },
        {
            "Warning": '299 Elasticsearch-8.0.0-SNAPSHOT-ad975cacd240b3329e160673c432e768dcd7899a "[xpack.monitoring.history.duration] setting was deprecated in Elasticsearch and will be removed in a future release! See the breaking changes documentation for the next major version.", 299 Elasticsearch-8.0.0-SNAPSHOT-ad975cacd240b3329e160673c432e768dcd7899a "[xpack.monitoring.history.duration2] setting was deprecated in Elasticsearch and will be removed in a future release! See the breaking changes documentation for the next major version."',
            "X-elastic-product": "Elasticsearch",
        },
    ],
)
async def test_warning_header(headers):
    client = AsyncElasticsearch(
        [NodeConfig("http", "localhost", 9200, _extras={"headers": headers})],
        meta_header=False,
        node_class=DummyNode,
    )

    with warnings.catch_warnings(record=True) as w:
        await client.info()

    assert len(w) == headers["Warning"].count("299")
    assert w[0].category == ElasticsearchWarning
    assert (
        str(w[0].message)
        == "[xpack.monitoring.history.duration] setting was deprecated in Elasticsearch and will be removed in a future release! See the breaking changes documentation for the next major version."
    )

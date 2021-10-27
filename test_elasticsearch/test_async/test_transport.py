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

from __future__ import unicode_literals

import asyncio
import json
import re
import warnings

import pytest
from elastic_transport import ApiResponseMeta, BaseAsyncNode, HttpHeaders, NodeConfig
from elastic_transport.client_utils import DEFAULT
from mock import patch

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import (
    ConnectionError,
    ElasticsearchWarning,
    TransportError,
    UnsupportedProductError,
)

pytestmark = pytest.mark.asyncio


sniffing_xfail = pytest.mark.xfail(strict=True)


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
        return (
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
        assert calls[0][1]["headers"] == {"content-type": "application/json"}

    async def test_body_surrogates_replaced_encoded_into_bytes(self):
        client = AsyncElasticsearch("http://localhost:9200", node_class=DummyNode)

        await client.search(body="你好\uda6a")

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][1]["body"] == b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"

    def test_kwargs_passed_on_to_node_pool(self):
        dt = object()
        client = AsyncElasticsearch(
            "http://localhost:9200", dead_node_backoff_factor=dt
        )
        assert dt is client.transport.node_pool.dead_node_backoff_factor

        class MyConnection(object):
            def __init__(self, *_, **__):
                pass

        client = AsyncElasticsearch("http://localhost:9200", node_class=MyConnection)
        assert 1 == len(client.transport.node_pool.all_nodes)
        assert isinstance(
            client.transport.node_pool.all_nodes.popitem()[1], MyConnection
        )

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
        assert 0 == len(client.transport.node_pool.alive_nodes)

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
        assert len(client.transport.node_pool.alive_nodes) == 0

        await client.info()

        assert len(client.transport.node_pool.alive_nodes) == 1
        assert len(client.transport.node_pool.dead_consecutive_failures) == 1

    @sniffing_xfail
    async def test_sniff_will_use_seed_connections(self):
        t = AsyncTransport(  # noqa: F821
            [{"data": CLUSTER_NODES}], connection_class=DummyNode
        )
        await t._async_call()
        t.set_connections([{"data": "invalid"}])

        await t.sniff_hosts()
        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    @sniffing_xfail
    async def test_sniff_on_start_fetches_and_uses_nodes_list(self):
        t = AsyncTransport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_start=True,
        )
        await t._async_call()
        await t.sniffing_task  # Need to wait for the sniffing task to complete

        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    @sniffing_xfail
    async def test_sniff_on_start_ignores_sniff_timeout(self):
        t = AsyncTransport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_start=True,
            sniff_timeout=12,
        )
        await t._async_call()
        await t.sniffing_task  # Need to wait for the sniffing task to complete

        assert (("GET", "/_nodes/_all/http"), {"timeout": None}) == t.seed_connections[
            0
        ].calls[0]

    @sniffing_xfail
    async def test_sniff_uses_sniff_timeout(self):
        t = AsyncTransport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_timeout=42,
        )
        await t._async_call()
        await t.sniff_hosts()

        assert (("GET", "/_nodes/_all/http"), {"timeout": 42}) == t.seed_connections[
            0
        ].calls[0]

    @sniffing_xfail
    async def test_sniff_reuses_connection_instances_if_possible(self):
        t = AsyncTransport(  # noqa: F821
            [{"data": CLUSTER_NODES}, {"host": "1.1.1.1", "port": 123}],
            connection_class=DummyNode,
            randomize_hosts=False,
        )
        await t._async_call()
        connection = t.connection_pool.connections[1]
        connection.delay = 3.0  # Add this delay to make the sniffing deterministic.

        await t.sniff_hosts()
        assert 1 == len(t.connection_pool.connections)
        assert connection is t.get_connection()

    @sniffing_xfail
    async def test_sniff_on_fail_triggers_sniffing_on_fail(self):
        t = AsyncTransport(  # noqa: F821
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_connection_fail=True,
            max_retries=0,
            randomize_hosts=False,
        )
        await t._async_call()

        connection_error = False
        try:
            await t.perform_request("GET", "/")
        except ConnectionError:
            connection_error = True

        await t.sniffing_task  # Need to wait for the sniffing task to complete

        assert connection_error
        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    @sniffing_xfail
    @patch("elasticsearch._async.transport.AsyncTransport.sniff_hosts")
    async def test_sniff_on_fail_failing_does_not_prevent_retires(self, sniff_hosts):
        sniff_hosts.side_effect = [TransportError("sniff failed")]
        t = AsyncTransport(  # noqa: F821
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_connection_fail=True,
            max_retries=3,
            randomize_hosts=False,
        )
        await t._async_init()

        conn_err, conn_data = t.connection_pool.connections
        response = await t.perform_request("GET", "/")
        assert json.loads(CLUSTER_NODES) == response
        assert 1 == sniff_hosts.call_count
        assert 1 == len(conn_err.calls)
        assert 1 == len(conn_data.calls)

    @sniffing_xfail
    async def test_sniff_after_n_seconds(self, event_loop):
        t = AsyncTransport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniffer_timeout=5,
        )
        await t._async_call()

        for _ in range(4):
            await t.perform_request("GET", "/")
        assert 1 == len(t.connection_pool.connections)
        assert isinstance(t.get_connection(), DummyNode)
        t.last_sniff = event_loop.time() - 5.1

        await t.perform_request("GET", "/")
        await t.sniffing_task  # Need to wait for the sniffing task to complete

        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host
        assert event_loop.time() - 1 < t.last_sniff < event_loop.time() + 0.01

    @sniffing_xfail
    async def test_sniff_7x_publish_host(self):
        # Test the response shaped when a 7.x node has publish_host set
        # and the returend data is shaped in the fqdn/ip:port format.
        t = AsyncTransport(  # noqa: F821
            [{"data": CLUSTER_NODES_7x_PUBLISH_HOST}],
            connection_class=DummyNode,
            sniff_timeout=42,
        )
        await t._async_call()
        await t.sniff_hosts()
        # Ensure we parsed out the fqdn and port from the fqdn/ip:port string.
        assert t.connection_pool.connection_opts[0][1] == {
            "host": "somehost.tld",
            "port": 123,
        }

    @sniffing_xfail
    @patch("elasticsearch._async.transport.AsyncTransport.sniff_hosts")
    async def test_sniffing_disabled_on_cloud_instances(self, sniff_hosts):
        t = AsyncTransport(  # noqa: F821
            [{}],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            connection_class=DummyNode,
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )
        await t._async_call()

        assert not t.sniff_on_connection_fail
        assert sniff_hosts.call_args is None  # Assert not called.
        await t.perform_request("GET", "/", body={})
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", None, b"{}") == t.get_connection().calls[0][0]

    @sniffing_xfail
    async def test_transport_close_closes_all_pool_connections(self):
        t = AsyncTransport([{}], connection_class=DummyNode)  # noqa: F821
        await t._async_call()

        assert not any([conn.closed for conn in t.connection_pool.connections])
        await t.close()
        assert all([conn.closed for conn in t.connection_pool.connections])

        t = AsyncTransport([{}, {}], connection_class=DummyNode)  # noqa: F821
        await t._async_call()

        assert not any([conn.closed for conn in t.connection_pool.connections])
        await t.close()
        assert all([conn.closed for conn in t.connection_pool.connections])

    @sniffing_xfail
    async def test_sniff_on_start_no_viable_hosts(self, event_loop):
        t = AsyncTransport(  # noqa: F821
            [
                {"data": ""},
                {"data": ""},
                {"data": ""},
            ],
            connection_class=DummyNode,
            sniff_on_start=True,
        )

        # If our initial sniffing attempt comes back
        # empty then we raise an error.
        with pytest.raises(TransportError) as e:
            await t._async_call()
        assert str(e.value) == "TransportError(N/A, 'Unable to sniff hosts.')"

    @sniffing_xfail
    async def test_sniff_on_start_waits_for_sniff_to_complete(self, event_loop):
        t = AsyncTransport(  # noqa: F821
            [
                {"delay": 1, "data": ""},
                {"delay": 1, "data": ""},
                {"delay": 1, "data": CLUSTER_NODES},
            ],
            connection_class=DummyNode,
            sniff_on_start=True,
        )

        # Start the timer right before the first task
        # and have a bunch of tasks come in immediately.
        tasks = []
        start_time = event_loop.time()
        for _ in range(5):
            tasks.append(event_loop.create_task(t._async_call()))
            await asyncio.sleep(0)  # Yield to the loop

        assert t.sniffing_task is not None

        # Tasks streaming in later.
        for _ in range(5):
            tasks.append(event_loop.create_task(t._async_call()))
            await asyncio.sleep(0.1)

        # Now that all the API calls have come in we wait for
        # them all to resolve before
        await asyncio.gather(*tasks)
        end_time = event_loop.time()
        duration = end_time - start_time

        # All the tasks blocked on the sniff of each node
        # and then resolved immediately after.
        assert 1 <= duration < 2

    @sniffing_xfail
    async def test_sniff_on_start_close_unlocks_async_calls(self, event_loop):
        t = AsyncTransport(  # noqa: F821
            [
                {"delay": 10, "data": CLUSTER_NODES},
            ],
            connection_class=DummyNode,
            sniff_on_start=True,
        )

        # Start making _async_calls() before we cancel
        tasks = []
        start_time = event_loop.time()
        for _ in range(3):
            tasks.append(event_loop.create_task(t._async_call()))
            await asyncio.sleep(0)

        # Close the transport while the sniffing task is active! :(
        await t.close()

        # Now we start waiting on all those _async_calls()
        await asyncio.gather(*tasks)
        end_time = event_loop.time()
        duration = end_time - start_time

        # A lot quicker than 10 seconds defined in 'delay'
        assert duration < 1


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
            "headers": {"content-type": "application/json"},
            "request_timeout": DEFAULT,
        },
    )


@pytest.mark.parametrize("status", [404, 500])
async def test_transport_error_raised_before_product_error(status):
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

    with pytest.raises(TransportError) as e:
        await client.info()
    assert e.value.status_code == status

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

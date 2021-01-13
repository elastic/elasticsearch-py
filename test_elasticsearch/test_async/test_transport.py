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

import pytest
from mock import patch

from elasticsearch import AsyncTransport
from elasticsearch.connection import Connection
from elasticsearch.connection_pool import DummyConnectionPool
from elasticsearch.exceptions import ConnectionError, TransportError

pytestmark = pytest.mark.asyncio


class DummyConnection(Connection):
    def __init__(self, **kwargs):
        self.exception = kwargs.pop("exception", None)
        self.status, self.data = kwargs.pop("status", 200), kwargs.pop("data", "{}")
        self.headers = kwargs.pop("headers", {})
        self.delay = kwargs.pop("delay", 0)
        self.calls = []
        self.closed = False
        super(DummyConnection, self).__init__(**kwargs)

    async def perform_request(self, *args, **kwargs):
        if self.closed:
            raise RuntimeError("This connection is closed")
        if self.delay:
            await asyncio.sleep(self.delay)
        self.calls.append((args, kwargs))
        if self.exception:
            raise self.exception
        return self.status, self.headers, self.data

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
    async def test_single_connection_uses_dummy_connection_pool(self):
        t = AsyncTransport([{}])
        await t._async_call()
        assert isinstance(t.connection_pool, DummyConnectionPool)
        t = AsyncTransport([{"host": "localhost"}])
        await t._async_call()
        assert isinstance(t.connection_pool, DummyConnectionPool)

    async def test_request_timeout_extracted_from_params_and_passed(self):
        t = AsyncTransport([{}], connection_class=DummyConnection, meta_header=False)

        await t.perform_request("GET", "/", params={"request_timeout": 42})
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", {}, None) == t.get_connection().calls[0][0]
        assert {
            "timeout": 42,
            "ignore": (),
            "headers": None,
        } == t.get_connection().calls[0][1]

    async def test_opaque_id(self):
        t = AsyncTransport(
            [{}], opaque_id="app-1", connection_class=DummyConnection, meta_header=False
        )

        await t.perform_request("GET", "/")
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", None, None) == t.get_connection().calls[0][0]
        assert {
            "timeout": None,
            "ignore": (),
            "headers": None,
        } == t.get_connection().calls[0][1]

        # Now try with an 'x-opaque-id' set on perform_request().
        await t.perform_request("GET", "/", headers={"x-opaque-id": "request-1"})
        assert 2 == len(t.get_connection().calls)
        assert ("GET", "/", None, None) == t.get_connection().calls[1][0]
        assert {
            "timeout": None,
            "ignore": (),
            "headers": {"x-opaque-id": "request-1"},
        } == t.get_connection().calls[1][1]

    async def test_request_with_custom_user_agent_header(self):
        t = AsyncTransport([{}], connection_class=DummyConnection, meta_header=False)

        await t.perform_request(
            "GET", "/", headers={"user-agent": "my-custom-value/1.2.3"}
        )
        assert 1 == len(t.get_connection().calls)
        assert {
            "timeout": None,
            "ignore": (),
            "headers": {"user-agent": "my-custom-value/1.2.3"},
        } == t.get_connection().calls[0][1]

    async def test_send_get_body_as_source(self):
        t = AsyncTransport(
            [{}], send_get_body_as="source", connection_class=DummyConnection
        )

        await t.perform_request("GET", "/", body={})
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", {"source": "{}"}, None) == t.get_connection().calls[0][0]

    async def test_send_get_body_as_post(self):
        t = AsyncTransport(
            [{}], send_get_body_as="POST", connection_class=DummyConnection
        )

        await t.perform_request("GET", "/", body={})
        assert 1 == len(t.get_connection().calls)
        assert ("POST", "/", None, b"{}") == t.get_connection().calls[0][0]

    async def test_client_meta_header(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)

        await t.perform_request("GET", "/", body={})
        assert len(t.get_connection().calls) == 1
        headers = t.get_connection().calls[0][1]["headers"]
        assert re.match(
            r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?$",
            headers["x-elastic-client-meta"],
        )

        class DummyConnectionWithMeta(DummyConnection):
            HTTP_CLIENT_META = ("dm", "1.2.3")

        t = AsyncTransport([{}], connection_class=DummyConnectionWithMeta)

        await t.perform_request("GET", "/", body={}, headers={"Custom": "header"})
        assert len(t.get_connection().calls) == 1
        headers = t.get_connection().calls[0][1]["headers"]
        assert re.match(
            r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?,dm=1.2.3$",
            headers["x-elastic-client-meta"],
        )
        assert headers["Custom"] == "header"

    async def test_client_meta_header_not_sent(self):
        t = AsyncTransport([{}], meta_header=False, connection_class=DummyConnection)

        await t.perform_request("GET", "/", body={})
        assert len(t.get_connection().calls) == 1
        headers = t.get_connection().calls[0][1]["headers"]
        assert headers is None

    async def test_body_gets_encoded_into_bytes(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)

        await t.perform_request("GET", "/", body="你好")
        assert 1 == len(t.get_connection().calls)
        assert (
            "GET",
            "/",
            None,
            b"\xe4\xbd\xa0\xe5\xa5\xbd",
        ) == t.get_connection().calls[0][0]

    async def test_body_bytes_get_passed_untouched(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)

        body = b"\xe4\xbd\xa0\xe5\xa5\xbd"
        await t.perform_request("GET", "/", body=body)
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", None, body) == t.get_connection().calls[0][0]

    async def test_body_surrogates_replaced_encoded_into_bytes(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)

        await t.perform_request("GET", "/", body="你好\uda6a")
        assert 1 == len(t.get_connection().calls)
        assert (
            "GET",
            "/",
            None,
            b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa",
        ) == t.get_connection().calls[0][0]

    async def test_kwargs_passed_on_to_connections(self):
        t = AsyncTransport([{"host": "google.com"}], port=123)
        await t._async_call()
        assert 1 == len(t.connection_pool.connections)
        assert "http://google.com:123" == t.connection_pool.connections[0].host

    async def test_kwargs_passed_on_to_connection_pool(self):
        dt = object()
        t = AsyncTransport([{}, {}], dead_timeout=dt)
        await t._async_call()
        assert dt is t.connection_pool.dead_timeout

    async def test_custom_connection_class(self):
        class MyConnection(object):
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        t = AsyncTransport([{}], connection_class=MyConnection)
        await t._async_call()
        assert 1 == len(t.connection_pool.connections)
        assert isinstance(t.connection_pool.connections[0], MyConnection)

    def test_add_connection(self):
        t = AsyncTransport([{}], randomize_hosts=False)
        t.add_connection({"host": "google.com", "port": 1234})

        assert 2 == len(t.connection_pool.connections)
        assert "http://google.com:1234" == t.connection_pool.connections[1].host

    async def test_request_will_fail_after_X_retries(self):
        t = AsyncTransport(
            [{"exception": ConnectionError("abandon ship")}],
            connection_class=DummyConnection,
        )

        connection_error = False
        try:
            await t.perform_request("GET", "/")
        except ConnectionError:
            connection_error = True

        assert connection_error
        assert 4 == len(t.get_connection().calls)

    async def test_failed_connection_will_be_marked_as_dead(self):
        t = AsyncTransport(
            [{"exception": ConnectionError("abandon ship")}] * 2,
            connection_class=DummyConnection,
        )

        connection_error = False
        try:
            await t.perform_request("GET", "/")
        except ConnectionError:
            connection_error = True

        assert connection_error
        assert 0 == len(t.connection_pool.connections)

    async def test_resurrected_connection_will_be_marked_as_live_on_success(self):
        for method in ("GET", "HEAD"):
            t = AsyncTransport([{}, {}], connection_class=DummyConnection)
            await t._async_call()
            con1 = t.connection_pool.get_connection()
            con2 = t.connection_pool.get_connection()
            t.connection_pool.mark_dead(con1)
            t.connection_pool.mark_dead(con2)

            await t.perform_request(method, "/")
            assert 1 == len(t.connection_pool.connections)
            assert 1 == len(t.connection_pool.dead_count)

    async def test_sniff_will_use_seed_connections(self):
        t = AsyncTransport([{"data": CLUSTER_NODES}], connection_class=DummyConnection)
        await t._async_call()
        t.set_connections([{"data": "invalid"}])

        await t.sniff_hosts()
        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    async def test_sniff_on_start_fetches_and_uses_nodes_list(self):
        t = AsyncTransport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
        )
        await t._async_call()
        await t.sniffing_task  # Need to wait for the sniffing task to complete

        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    async def test_sniff_on_start_ignores_sniff_timeout(self):
        t = AsyncTransport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
            sniff_timeout=12,
        )
        await t._async_call()
        await t.sniffing_task  # Need to wait for the sniffing task to complete

        assert (("GET", "/_nodes/_all/http"), {"timeout": None}) == t.seed_connections[
            0
        ].calls[0]

    async def test_sniff_uses_sniff_timeout(self):
        t = AsyncTransport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        await t._async_call()
        await t.sniff_hosts()

        assert (("GET", "/_nodes/_all/http"), {"timeout": 42}) == t.seed_connections[
            0
        ].calls[0]

    async def test_sniff_reuses_connection_instances_if_possible(self):
        t = AsyncTransport(
            [{"data": CLUSTER_NODES}, {"host": "1.1.1.1", "port": 123}],
            connection_class=DummyConnection,
            randomize_hosts=False,
        )
        await t._async_call()
        connection = t.connection_pool.connections[1]
        connection.delay = 3.0  # Add this delay to make the sniffing deterministic.

        await t.sniff_hosts()
        assert 1 == len(t.connection_pool.connections)
        assert connection is t.get_connection()

    async def test_sniff_on_fail_triggers_sniffing_on_fail(self):
        t = AsyncTransport(
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
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

    @patch("elasticsearch._async.transport.AsyncTransport.sniff_hosts")
    async def test_sniff_on_fail_failing_does_not_prevent_retires(self, sniff_hosts):
        sniff_hosts.side_effect = [TransportError("sniff failed")]
        t = AsyncTransport(
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
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

    async def test_sniff_after_n_seconds(self, event_loop):
        t = AsyncTransport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniffer_timeout=5,
        )
        await t._async_call()

        for _ in range(4):
            await t.perform_request("GET", "/")
        assert 1 == len(t.connection_pool.connections)
        assert isinstance(t.get_connection(), DummyConnection)
        t.last_sniff = event_loop.time() - 5.1

        await t.perform_request("GET", "/")
        await t.sniffing_task  # Need to wait for the sniffing task to complete

        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host
        assert event_loop.time() - 1 < t.last_sniff < event_loop.time() + 0.01

    async def test_sniff_7x_publish_host(self):
        # Test the response shaped when a 7.x node has publish_host set
        # and the returend data is shaped in the fqdn/ip:port format.
        t = AsyncTransport(
            [{"data": CLUSTER_NODES_7x_PUBLISH_HOST}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        await t._async_call()
        await t.sniff_hosts()
        # Ensure we parsed out the fqdn and port from the fqdn/ip:port string.
        assert t.connection_pool.connection_opts[0][1] == {
            "host": "somehost.tld",
            "port": 123,
        }

    @patch("elasticsearch._async.transport.AsyncTransport.sniff_hosts")
    async def test_sniffing_disabled_on_cloud_instances(self, sniff_hosts):
        t = AsyncTransport(
            [{}],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            connection_class=DummyConnection,
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )
        await t._async_call()

        assert not t.sniff_on_connection_fail
        assert sniff_hosts.call_args is None  # Assert not called.
        await t.perform_request("GET", "/", body={})
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", None, b"{}") == t.get_connection().calls[0][0]

    async def test_transport_close_closes_all_pool_connections(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)
        await t._async_call()

        assert not any([conn.closed for conn in t.connection_pool.connections])
        await t.close()
        assert all([conn.closed for conn in t.connection_pool.connections])

        t = AsyncTransport([{}, {}], connection_class=DummyConnection)
        await t._async_call()

        assert not any([conn.closed for conn in t.connection_pool.connections])
        await t.close()
        assert all([conn.closed for conn in t.connection_pool.connections])

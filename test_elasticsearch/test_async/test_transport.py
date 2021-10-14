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
from mock import patch

from elasticsearch import AsyncTransport
from elasticsearch.connection import Connection
from elasticsearch.connection_pool import DummyConnectionPool
from elasticsearch.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConnectionError,
    ElasticsearchWarning,
    NotFoundError,
    TransportError,
    UnsupportedProductError,
)
from elasticsearch.transport import _ProductChecker

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
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

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
        with warnings.catch_warnings(record=True) as w:
            t = AsyncTransport(
                [{}], send_get_body_as="source", connection_class=DummyConnection
            )
        assert len(w) == 1
        assert str(w[0].message) == (
            "The 'send_get_body_as' parameter is no longer necessary and will be removed in 8.0"
        )
        t._verified_elasticsearch = True

        await t.perform_request("GET", "/", body={})
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", {"source": "{}"}, None) == t.get_connection().calls[0][0]

    async def test_send_get_body_as_post(self):
        with warnings.catch_warnings(record=True) as w:
            t = AsyncTransport(
                [{}], send_get_body_as="POST", connection_class=DummyConnection
            )
        assert len(w) == 1
        assert str(w[0].message) == (
            "The 'send_get_body_as' parameter is no longer necessary and will be removed in 8.0"
        )
        t._verified_elasticsearch = True

        await t.perform_request("GET", "/", body={})
        assert 1 == len(t.get_connection().calls)
        assert ("POST", "/", None, b"{}") == t.get_connection().calls[0][0]

    async def test_client_meta_header(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

        await t.perform_request("GET", "/", body={})
        assert len(t.get_connection().calls) == 1
        headers = t.get_connection().calls[0][1]["headers"]
        assert headers is None

    async def test_body_gets_encoded_into_bytes(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

        body = b"\xe4\xbd\xa0\xe5\xa5\xbd"
        await t.perform_request("GET", "/", body=body)
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", None, body) == t.get_connection().calls[0][0]

    async def test_body_surrogates_replaced_encoded_into_bytes(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

        await t._async_call()
        assert 1 == len(t.connection_pool.connections)
        assert "http://google.com:123" == t.connection_pool.connections[0].host

    async def test_kwargs_passed_on_to_connection_pool(self):
        dt = object()
        t = AsyncTransport([{}, {}], dead_timeout=dt)
        t._verified_elasticsearch = True

        await t._async_call()
        assert dt is t.connection_pool.dead_timeout

    async def test_custom_connection_class(self):
        class MyConnection(object):
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        t = AsyncTransport([{}], connection_class=MyConnection)
        t._verified_elasticsearch = True

        await t._async_call()
        assert 1 == len(t.connection_pool.connections)
        assert isinstance(t.connection_pool.connections[0], MyConnection)

    def test_add_connection(self):
        t = AsyncTransport([{}], randomize_hosts=False)
        t._verified_elasticsearch = True
        t.add_connection({"host": "google.com", "port": 1234})

        assert 2 == len(t.connection_pool.connections)
        assert "http://google.com:1234" == t.connection_pool.connections[1].host

    async def test_request_will_fail_after_X_retries(self):
        t = AsyncTransport(
            [{"exception": ConnectionError("abandon ship")}],
            connection_class=DummyConnection,
        )
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

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
            t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True

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
        t._verified_elasticsearch = True
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
        t._verified_elasticsearch = True
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
        t._verified_elasticsearch = True
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
        t._verified_elasticsearch = True
        await t._async_call()

        assert not t.sniff_on_connection_fail
        assert sniff_hosts.call_args is None  # Assert not called.
        await t.perform_request("GET", "/", body={})
        assert 1 == len(t.get_connection().calls)
        assert ("GET", "/", None, b"{}") == t.get_connection().calls[0][0]

    async def test_transport_close_closes_all_pool_connections(self):
        t = AsyncTransport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True
        await t._async_call()

        assert not any([conn.closed for conn in t.connection_pool.connections])
        await t.close()
        assert all([conn.closed for conn in t.connection_pool.connections])

        t = AsyncTransport([{}, {}], connection_class=DummyConnection)
        t._verified_elasticsearch = True
        await t._async_call()

        assert not any([conn.closed for conn in t.connection_pool.connections])
        await t.close()
        assert all([conn.closed for conn in t.connection_pool.connections])

    async def test_sniff_on_start_error_if_no_sniffed_hosts(self, event_loop):
        t = AsyncTransport(
            [
                {"data": ""},
                {"data": ""},
                {"data": ""},
            ],
            connection_class=DummyConnection,
            sniff_on_start=True,
        )
        t._verified_elasticsearch = True

        # If our initial sniffing attempt comes back
        # empty then we raise an error.
        with pytest.raises(TransportError) as e:
            await t._async_call()
        assert str(e.value) == "TransportError(N/A, 'Unable to sniff hosts.')"

    async def test_sniff_on_start_waits_for_sniff_to_complete(self, event_loop):
        t = AsyncTransport(
            [
                {"delay": 1, "data": ""},
                {"delay": 1, "data": ""},
                {"delay": 1, "data": CLUSTER_NODES},
            ],
            connection_class=DummyConnection,
            sniff_on_start=True,
        )
        t._verified_elasticsearch = True

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

    async def test_sniff_on_start_close_unlocks_async_calls(self, event_loop):
        t = AsyncTransport(
            [
                {"delay": 10, "data": CLUSTER_NODES},
            ],
            connection_class=DummyConnection,
            sniff_on_start=True,
        )
        t._verified_elasticsearch = True

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

    @pytest.mark.parametrize(
        ["headers", "data"],
        [
            (
                {},
                '{"version":{"number":"6.99.0"},"tagline":"You Know, for Search"}',
            ),
            (
                {},
                '{"version":{"number":"7.13.0","build_flavor":"default"},"tagline":"You Know, for Search"}',
            ),
            (
                {"X-elastic-product": "Elasticsearch"},
                '{"version":{"number":"7.14.0","build_flavor":"default"},"tagline":"You Know, for Search"}',
            ),
        ],
    )
    async def test_verify_elasticsearch(self, headers, data):
        t = AsyncTransport(
            [{"data": data, "headers": headers}], connection_class=DummyConnection
        )
        await t.perform_request("GET", "/_search")
        assert t._verified_elasticsearch is True

        calls = t.connection_pool.connections[0].calls
        _ = [call[1]["headers"].pop("x-elastic-client-meta") for call in calls]

        assert calls == [
            (
                ("GET", "/"),
                {
                    "headers": {
                        "accept": "application/json",
                    },
                    "timeout": None,
                },
            ),
            (
                ("GET", "/_search", None, None),
                {
                    "headers": {},
                    "ignore": (),
                    "timeout": None,
                },
            ),
        ]

    @pytest.mark.parametrize(
        "exception_cls", [AuthorizationException, AuthenticationException]
    )
    async def test_verify_elasticsearch_skips_on_auth_errors(self, exception_cls):
        t = AsyncTransport(
            [{"exception": exception_cls(exception_cls.status_code)}],
            connection_class=DummyConnection,
        )

        with pytest.warns(ElasticsearchWarning) as warns:
            with pytest.raises(exception_cls):
                await t.perform_request(
                    "GET", "/_search", headers={"Authorization": "testme"}
                )

        # Assert that a warning was raised due to security privileges
        assert [str(w.message) for w in warns] == [
            "The client is unable to verify that the server is "
            "Elasticsearch due security privileges on the server side"
        ]

        # Assert that the cluster is "verified"
        assert t._verified_elasticsearch is True

        # See that the headers were passed along to the "info" request made
        calls = t.connection_pool.connections[0].calls
        _ = [call[1]["headers"].pop("x-elastic-client-meta") for call in calls]

        assert calls == [
            (
                ("GET", "/"),
                {
                    "headers": {
                        "accept": "application/json",
                        "authorization": "testme",
                    },
                    "timeout": None,
                },
            ),
            (
                ("GET", "/_search", None, None),
                {
                    "headers": {
                        "Authorization": "testme",
                    },
                    "ignore": (),
                    "timeout": None,
                },
            ),
        ]

    async def test_multiple_requests_verify_elasticsearch_success(self, event_loop):
        t = AsyncTransport(
            [
                {
                    "data": '{"version":{"number":"7.13.0","build_flavor":"default"},"tagline":"You Know, for Search"}',
                    "delay": 1,
                }
            ],
            connection_class=DummyConnection,
        )

        results = []
        completed_at = []

        async def request_task():
            try:
                results.append(await t.perform_request("GET", "/_search"))
            except Exception as e:
                results.append(e)
            completed_at.append(event_loop.time())

        # Execute a bunch of requests concurrently.
        tasks = []
        start_time = event_loop.time()
        for _ in range(10):
            tasks.append(event_loop.create_task(request_task()))
        await asyncio.gather(*tasks)
        end_time = event_loop.time()

        # Exactly 10 results completed
        assert len(results) == 10

        # No errors in the results
        assert all(isinstance(result, dict) for result in results)

        # Assert that this took longer than 2 seconds but less than 2.1 seconds
        duration = end_time - start_time
        assert 2 <= duration <= 2.1

        # Assert that every result came after ~2 seconds, no fast completions.
        assert all(
            2 <= completed_time - start_time <= 2.1 for completed_time in completed_at
        )

        # Assert that the cluster is "verified"
        assert t._verified_elasticsearch is True

        # See that the first request is always 'GET /' for ES check
        calls = t.connection_pool.connections[0].calls
        assert calls[0][0] == ("GET", "/")

        # The rest of the requests are 'GET /_search' afterwards
        assert all(call[0][:2] == ("GET", "/_search") for call in calls[1:])

    @pytest.mark.parametrize(
        ["build_flavor", "tagline", "product_error", "error_message"],
        [
            (
                "default",
                "BAD TAGLINE",
                _ProductChecker.UNSUPPORTED_PRODUCT,
                "The client noticed that the server is not Elasticsearch and we do not support this unknown product",
            ),
            (
                "BAD BUILD FLAVOR",
                "BAD TAGLINE",
                _ProductChecker.UNSUPPORTED_PRODUCT,
                "The client noticed that the server is not Elasticsearch and we do not support this unknown product",
            ),
            (
                "BAD BUILD FLAVOR",
                "You Know, for Search",
                _ProductChecker.UNSUPPORTED_DISTRIBUTION,
                "The client noticed that the server is not a supported distribution of Elasticsearch",
            ),
        ],
    )
    async def test_multiple_requests_verify_elasticsearch_product_error(
        self, event_loop, build_flavor, tagline, product_error, error_message
    ):
        t = AsyncTransport(
            [
                {
                    "data": '{"version":{"number":"7.13.0","build_flavor":"%s"},"tagline":"%s"}'
                    % (build_flavor, tagline),
                    "delay": 1,
                }
            ],
            connection_class=DummyConnection,
        )

        results = []
        completed_at = []

        async def request_task():
            try:
                results.append(await t.perform_request("GET", "/_search"))
            except Exception as e:
                results.append(e)
            completed_at.append(event_loop.time())

        # Execute a bunch of requests concurrently.
        tasks = []
        start_time = event_loop.time()
        for _ in range(10):
            tasks.append(event_loop.create_task(request_task()))
        await asyncio.gather(*tasks)
        end_time = event_loop.time()

        # Exactly 10 results completed
        assert len(results) == 10

        # All results were errors
        assert all(isinstance(result, UnsupportedProductError) for result in results)
        assert all(str(result) == error_message for result in results)

        # Assert that one request was made but not 2 requests.
        duration = end_time - start_time
        assert 1 <= duration <= 1.1

        # Assert that every result came after ~1 seconds, no fast completions.
        assert all(
            1 <= completed_time - start_time <= 1.1 for completed_time in completed_at
        )

        # Assert that the cluster is definitely not Elasticsearch
        assert t._verified_elasticsearch == product_error

        # See that the first request is always 'GET /' for ES check
        calls = t.connection_pool.connections[0].calls
        assert calls[0][0] == ("GET", "/")

        # The rest of the requests are 'GET /_search' afterwards
        assert all(call[0][:2] == ("GET", "/_search") for call in calls[1:])

    @pytest.mark.parametrize("error_cls", [ConnectionError, NotFoundError])
    async def test_multiple_requests_verify_elasticsearch_retry_on_errors(
        self, event_loop, error_cls
    ):
        t = AsyncTransport(
            [
                {
                    "exception": error_cls(),
                    "delay": 0.1,
                }
            ],
            connection_class=DummyConnection,
        )

        results = []
        completed_at = []

        async def request_task():
            try:
                results.append(await t.perform_request("GET", "/_search"))
            except Exception as e:
                results.append(e)
            completed_at.append(event_loop.time())

        # Execute a bunch of requests concurrently.
        tasks = []
        start_time = event_loop.time()
        for _ in range(5):
            tasks.append(event_loop.create_task(request_task()))
        await asyncio.gather(*tasks)
        end_time = event_loop.time()

        # Exactly 5 results completed
        assert len(results) == 5

        # All results were errors and not wrapped in 'NotElasticsearchError'
        assert all(isinstance(result, error_cls) for result in results)

        # Assert that 5 requests were made in total (5 transport requests per x 0.1s/conn request)
        duration = end_time - start_time
        assert 0.5 <= duration <= 0.6

        # Assert that the cluster is still in the unknown/unverified stage.
        assert t._verified_elasticsearch is None

        # See that the API isn't hit, instead it's the index requests that are failing.
        calls = t.connection_pool.connections[0].calls
        assert len(calls) == 5
        assert all(call[0] == ("GET", "/") for call in calls)

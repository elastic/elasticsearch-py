# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time

from elasticsearch.transport import Transport, get_host_info
from elasticsearch.connection import Connection
from elasticsearch.connection_pool import DummyConnectionPool
from elasticsearch.exceptions import ConnectionError

from .test_cases import TestCase


class DummyConnection(Connection):
    def __init__(self, **kwargs):
        self.exception = kwargs.pop("exception", None)
        self.status, self.data = kwargs.pop("status", 200), kwargs.pop("data", "{}")
        self.headers = kwargs.pop("headers", {})
        self.calls = []
        super(DummyConnection, self).__init__(**kwargs)

    def perform_request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.exception:
            raise self.exception
        return self.status, self.headers, self.data


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


class TestHostsInfoCallback(TestCase):
    def test_master_only_nodes_are_ignored(self):
        nodes = [
            {"roles": ["master"]},
            {"roles": ["master", "data", "ingest"]},
            {"roles": ["data", "ingest"]},
            {"roles": []},
            {},
        ]
        chosen = [
            i
            for i, node_info in enumerate(nodes)
            if get_host_info(node_info, i) is not None
        ]
        self.assertEquals([1, 2, 3, 4], chosen)


class TestTransport(TestCase):
    def test_single_connection_uses_dummy_connection_pool(self):
        t = Transport([{}])
        self.assertIsInstance(t.connection_pool, DummyConnectionPool)
        t = Transport([{"host": "localhost"}])
        self.assertIsInstance(t.connection_pool, DummyConnectionPool)

    def test_request_timeout_extracted_from_params_and_passed(self):
        t = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", params={"request_timeout": 42})
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(("GET", "/", {}, None), t.get_connection().calls[0][0])
        self.assertEquals(
            {"timeout": 42, "ignore": (), "headers": None},
            t.get_connection().calls[0][1],
        )

    def test_opaque_id(self):
        t = Transport([{}], opaque_id="app-1", connection_class=DummyConnection)

        t.perform_request("GET", "/")
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(("GET", "/", None, None), t.get_connection().calls[0][0])
        self.assertEquals(
            {"timeout": None, "ignore": (), "headers": None},
            t.get_connection().calls[0][1],
        )

        # Now try with an 'x-opaque-id' set on perform_request().
        t.perform_request("GET", "/", headers={"x-opaque-id": "request-1"})
        self.assertEquals(2, len(t.get_connection().calls))
        self.assertEquals(("GET", "/", None, None), t.get_connection().calls[1][0])
        self.assertEquals(
            {"timeout": None, "ignore": (), "headers": {"x-opaque-id": "request-1"}},
            t.get_connection().calls[1][1],
        )

    def test_request_with_custom_user_agent_header(self):
        t = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", headers={"user-agent": "my-custom-value/1.2.3"})
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(
            {
                "timeout": None,
                "ignore": (),
                "headers": {"user-agent": "my-custom-value/1.2.3"},
            },
            t.get_connection().calls[0][1],
        )

    def test_send_get_body_as_source(self):
        t = Transport([{}], send_get_body_as="source", connection_class=DummyConnection)

        t.perform_request("GET", "/", body={})
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(
            ("GET", "/", {"source": "{}"}, None), t.get_connection().calls[0][0]
        )

    def test_send_get_body_as_post(self):
        t = Transport([{}], send_get_body_as="POST", connection_class=DummyConnection)

        t.perform_request("GET", "/", body={})
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(("POST", "/", None, b"{}"), t.get_connection().calls[0][0])

    def test_body_gets_encoded_into_bytes(self):
        t = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", body="你好")
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(
            ("GET", "/", None, b"\xe4\xbd\xa0\xe5\xa5\xbd"),
            t.get_connection().calls[0][0],
        )

    def test_body_bytes_get_passed_untouched(self):
        t = Transport([{}], connection_class=DummyConnection)

        body = b"\xe4\xbd\xa0\xe5\xa5\xbd"
        t.perform_request("GET", "/", body=body)
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(("GET", "/", None, body), t.get_connection().calls[0][0])

    def test_body_surrogates_replaced_encoded_into_bytes(self):
        t = Transport([{}], connection_class=DummyConnection)

        t.perform_request("GET", "/", body="你好\uda6a")
        self.assertEquals(1, len(t.get_connection().calls))
        self.assertEquals(
            ("GET", "/", None, b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"),
            t.get_connection().calls[0][0],
        )

    def test_kwargs_passed_on_to_connections(self):
        t = Transport([{"host": "google.com"}], port=123)
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertEquals(
            "http://google.com:123", t.connection_pool.connections[0].host
        )

    def test_kwargs_passed_on_to_connection_pool(self):
        dt = object()
        t = Transport([{}, {}], dead_timeout=dt)
        self.assertIs(dt, t.connection_pool.dead_timeout)

    def test_custom_connection_class(self):
        class MyConnection(object):
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        t = Transport([{}], connection_class=MyConnection)
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertIsInstance(t.connection_pool.connections[0], MyConnection)

    def test_add_connection(self):
        t = Transport([{}], randomize_hosts=False)
        t.add_connection({"host": "google.com", "port": 1234})

        self.assertEquals(2, len(t.connection_pool.connections))
        self.assertEquals(
            "http://google.com:1234", t.connection_pool.connections[1].host
        )

    def test_request_will_fail_after_X_retries(self):
        t = Transport(
            [{"exception": ConnectionError("abandon ship")}],
            connection_class=DummyConnection,
        )

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEquals(4, len(t.get_connection().calls))

    def test_failed_connection_will_be_marked_as_dead(self):
        t = Transport(
            [{"exception": ConnectionError("abandon ship")}] * 2,
            connection_class=DummyConnection,
        )

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEquals(0, len(t.connection_pool.connections))

    def test_resurrected_connection_will_be_marked_as_live_on_success(self):
        t = Transport([{}, {}], connection_class=DummyConnection)
        con1 = t.connection_pool.get_connection()
        con2 = t.connection_pool.get_connection()
        t.connection_pool.mark_dead(con1)
        t.connection_pool.mark_dead(con2)

        t.perform_request("GET", "/")
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertEquals(1, len(t.connection_pool.dead_count))

    def test_sniff_will_use_seed_connections(self):
        t = Transport([{"data": CLUSTER_NODES}], connection_class=DummyConnection)
        t.set_connections([{"data": "invalid"}])

        t.sniff_hosts()
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertEquals("http://1.1.1.1:123", t.get_connection().host)

    def test_sniff_on_start_fetches_and_uses_nodes_list(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
        )
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertEquals("http://1.1.1.1:123", t.get_connection().host)

    def test_sniff_on_start_ignores_sniff_timeout(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
            sniff_timeout=12,
        )
        self.assertEquals(
            (("GET", "/_nodes/_all/http"), {"timeout": None}),
            t.seed_connections[0].calls[0],
        )

    def test_sniff_uses_sniff_timeout(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        t.sniff_hosts()
        self.assertEquals(
            (("GET", "/_nodes/_all/http"), {"timeout": 42}),
            t.seed_connections[0].calls[0],
        )

    def test_sniff_reuses_connection_instances_if_possible(self):
        t = Transport(
            [{"data": CLUSTER_NODES}, {"host": "1.1.1.1", "port": 123}],
            connection_class=DummyConnection,
            randomize_hosts=False,
        )
        connection = t.connection_pool.connections[1]

        t.sniff_hosts()
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertIs(connection, t.get_connection())

    def test_sniff_on_fail_triggers_sniffing_on_fail(self):
        t = Transport(
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_connection_fail=True,
            max_retries=0,
            randomize_hosts=False,
        )

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertEquals("http://1.1.1.1:123", t.get_connection().host)

    def test_sniff_after_n_seconds(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniffer_timeout=5,
        )

        for _ in range(4):
            t.perform_request("GET", "/")
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertIsInstance(t.get_connection(), DummyConnection)
        t.last_sniff = time.time() - 5.1

        t.perform_request("GET", "/")
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertEquals("http://1.1.1.1:123", t.get_connection().host)
        self.assertTrue(time.time() - 1 < t.last_sniff < time.time() + 0.01)

    def test_sniff_7x_publish_host(self):
        # Test the response shaped when a 7.x node has publish_host set
        # and the returend data is shaped in the fqdn/ip:port format.
        t = Transport(
            [{"data": CLUSTER_NODES_7x_PUBLISH_HOST}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        t.sniff_hosts()
        # Ensure we parsed out the fqdn and port from the fqdn/ip:port string.
        self.assertEqual(
            t.connection_pool.connection_opts[0][1],
            {"host": "somehost.tld", "port": 123},
        )

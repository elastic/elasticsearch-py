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

import json
import time
import warnings

import pytest
from mock import patch

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
from elasticsearch.transport import Transport, _ProductChecker, get_host_info

from .test_cases import TestCase


class DummyConnection(Connection):
    def __init__(self, **kwargs):
        self.exception = kwargs.pop("exception", None)
        self.status, self.data = kwargs.pop("status", 200), kwargs.pop("data", "{}")
        self.headers = kwargs.pop("headers", {})
        self.delay = kwargs.pop("delay", None)
        self.calls = []
        super(DummyConnection, self).__init__(**kwargs)

    def perform_request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.delay is not None:
            time.sleep(self.delay)
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
        self.assertEqual([1, 2, 3, 4], chosen)


class TestTransport(TestCase):
    def test_single_connection_uses_dummy_connection_pool(self):
        t = Transport([{}])
        t._verified_elasticsearch = True
        self.assertIsInstance(t.connection_pool, DummyConnectionPool)

        t = Transport([{"host": "localhost"}])
        t._verified_elasticsearch = True
        self.assertIsInstance(t.connection_pool, DummyConnectionPool)

    def test_request_timeout_extracted_from_params_and_passed(self):
        t = Transport([{}], meta_header=False, connection_class=DummyConnection)
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", params={"request_timeout": 42})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", {}, None), t.get_connection().calls[0][0])
        self.assertEqual(
            {"timeout": 42, "ignore": (), "headers": None},
            t.get_connection().calls[0][1],
        )

    def test_opaque_id(self):
        t = Transport(
            [{}], opaque_id="app-1", meta_header=False, connection_class=DummyConnection
        )
        t._verified_elasticsearch = True

        t.perform_request("GET", "/")
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", None, None), t.get_connection().calls[0][0])
        self.assertEqual(
            {"timeout": None, "ignore": (), "headers": None},
            t.get_connection().calls[0][1],
        )

        # Now try with an 'x-opaque-id' set on perform_request().
        t.perform_request("GET", "/", headers={"x-opaque-id": "request-1"})
        self.assertEqual(2, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", None, None), t.get_connection().calls[1][0])
        self.assertEqual(
            {"timeout": None, "ignore": (), "headers": {"x-opaque-id": "request-1"}},
            t.get_connection().calls[1][1],
        )

    def test_request_with_custom_user_agent_header(self):
        t = Transport([{}], meta_header=False, connection_class=DummyConnection)
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", headers={"user-agent": "my-custom-value/1.2.3"})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            {
                "timeout": None,
                "ignore": (),
                "headers": {"user-agent": "my-custom-value/1.2.3"},
            },
            t.get_connection().calls[0][1],
        )

    def test_send_get_body_as_source(self):
        with warnings.catch_warnings(record=True) as w:
            t = Transport(
                [{}], send_get_body_as="source", connection_class=DummyConnection
            )
        assert len(w) == 1
        assert str(w[0].message) == (
            "The 'send_get_body_as' parameter is no longer necessary and will be removed in 8.0"
        )
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", body={})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            ("GET", "/", {"source": "{}"}, None), t.get_connection().calls[0][0]
        )

    def test_send_get_body_as_post(self):
        with warnings.catch_warnings(record=True) as w:
            t = Transport(
                [{}], send_get_body_as="POST", connection_class=DummyConnection
            )
        assert len(w) == 1
        assert str(w[0].message) == (
            "The 'send_get_body_as' parameter is no longer necessary and will be removed in 8.0"
        )
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", body={})
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("POST", "/", None, b"{}"), t.get_connection().calls[0][0])

    def test_client_meta_header(self):
        t = Transport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", body={})
        self.assertEqual(1, len(t.get_connection().calls))
        headers = t.get_connection().calls[0][1]["headers"]
        self.assertRegexpMatches(
            headers["x-elastic-client-meta"], r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?$"
        )

        class DummyConnectionWithMeta(DummyConnection):
            HTTP_CLIENT_META = ("dm", "1.2.3")

        t = Transport([{}], connection_class=DummyConnectionWithMeta)
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", body={}, headers={"Custom": "header"})
        self.assertEqual(1, len(t.get_connection().calls))
        headers = t.get_connection().calls[0][1]["headers"]
        self.assertRegexpMatches(
            headers["x-elastic-client-meta"],
            r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?,dm=1.2.3$",
        )
        self.assertEqual(headers["Custom"], "header")

    def test_client_meta_header_not_sent(self):
        t = Transport([{}], meta_header=False, connection_class=DummyConnection)
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", body={})
        self.assertEqual(1, len(t.get_connection().calls))
        headers = t.get_connection().calls[0][1]["headers"]
        self.assertIs(headers, None)

    def test_meta_header_type_error(self):
        with pytest.raises(TypeError) as e:
            Transport([{}], meta_header=1)
        assert str(e.value) == "meta_header must be of type bool"

    def test_body_gets_encoded_into_bytes(self):
        t = Transport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", body="你好")
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            ("GET", "/", None, b"\xe4\xbd\xa0\xe5\xa5\xbd"),
            t.get_connection().calls[0][0],
        )

    def test_body_bytes_get_passed_untouched(self):
        t = Transport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True

        body = b"\xe4\xbd\xa0\xe5\xa5\xbd"
        t.perform_request("GET", "/", body=body)
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(("GET", "/", None, body), t.get_connection().calls[0][0])

    def test_body_surrogates_replaced_encoded_into_bytes(self):
        t = Transport([{}], connection_class=DummyConnection)
        t._verified_elasticsearch = True

        t.perform_request("GET", "/", body="你好\uda6a")
        self.assertEqual(1, len(t.get_connection().calls))
        self.assertEqual(
            ("GET", "/", None, b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"),
            t.get_connection().calls[0][0],
        )

    def test_kwargs_passed_on_to_connections(self):
        t = Transport([{"host": "google.com"}], port=123)
        t._verified_elasticsearch = True
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://google.com:123", t.connection_pool.connections[0].host)

    def test_kwargs_passed_on_to_connection_pool(self):
        dt = object()
        t = Transport([{}, {}], dead_timeout=dt)
        t._verified_elasticsearch = True
        self.assertIs(dt, t.connection_pool.dead_timeout)

    def test_custom_connection_class(self):
        class MyConnection(object):
            def __init__(self, **kwargs):
                self.kwargs = kwargs

        t = Transport([{}], connection_class=MyConnection)
        t._verified_elasticsearch = True
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertIsInstance(t.connection_pool.connections[0], MyConnection)

    def test_add_connection(self):
        t = Transport([{}], randomize_hosts=False)
        t._verified_elasticsearch = True
        t.add_connection({"host": "google.com", "port": 1234})

        self.assertEqual(2, len(t.connection_pool.connections))
        self.assertEqual(
            "http://google.com:1234", t.connection_pool.connections[1].host
        )

    def test_request_will_fail_after_X_retries(self):
        t = Transport(
            [{"exception": ConnectionError("abandon ship")}],
            connection_class=DummyConnection,
        )
        t._verified_elasticsearch = True

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEqual(4, len(t.get_connection().calls))

    def test_failed_connection_will_be_marked_as_dead(self):
        t = Transport(
            [{"exception": ConnectionError("abandon ship")}] * 2,
            connection_class=DummyConnection,
        )
        t._verified_elasticsearch = True

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEqual(0, len(t.connection_pool.connections))

    def test_resurrected_connection_will_be_marked_as_live_on_success(self):
        for method in ("GET", "HEAD"):
            t = Transport([{}, {}], connection_class=DummyConnection)
            t._verified_elasticsearch = True
            con1 = t.connection_pool.get_connection()
            con2 = t.connection_pool.get_connection()
            t.connection_pool.mark_dead(con1)
            t.connection_pool.mark_dead(con2)

            t.perform_request(method, "/")
            self.assertEqual(1, len(t.connection_pool.connections))
            self.assertEqual(1, len(t.connection_pool.dead_count))

    def test_sniff_will_use_seed_connections(self):
        t = Transport([{"data": CLUSTER_NODES}], connection_class=DummyConnection)
        t._verified_elasticsearch = True
        t.set_connections([{"data": "invalid"}])

        t.sniff_hosts()
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)

    def test_sniff_on_start_fetches_and_uses_nodes_list(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
        )
        t._verified_elasticsearch = True
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)

    def test_sniff_on_start_ignores_sniff_timeout(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_start=True,
            sniff_timeout=12,
        )
        t._verified_elasticsearch = True
        self.assertEqual(
            (("GET", "/_nodes/_all/http"), {"timeout": None}),
            t.seed_connections[0].calls[0],
        )

    def test_sniff_uses_sniff_timeout(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        t._verified_elasticsearch = True
        t.sniff_hosts()
        self.assertEqual(
            (("GET", "/_nodes/_all/http"), {"timeout": 42}),
            t.seed_connections[0].calls[0],
        )

    def test_sniff_reuses_connection_instances_if_possible(self):
        t = Transport(
            [{"data": CLUSTER_NODES}, {"host": "1.1.1.1", "port": 123}],
            connection_class=DummyConnection,
            randomize_hosts=False,
        )
        t._verified_elasticsearch = True
        connection = t.connection_pool.connections[1]

        t.sniff_hosts()
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertIs(connection, t.get_connection())

    def test_sniff_on_fail_triggers_sniffing_on_fail(self):
        t = Transport(
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_connection_fail=True,
            max_retries=0,
            randomize_hosts=False,
        )
        t._verified_elasticsearch = True

        self.assertRaises(ConnectionError, t.perform_request, "GET", "/")
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)

    @patch("elasticsearch.transport.Transport.sniff_hosts")
    def test_sniff_on_fail_failing_does_not_prevent_retires(self, sniff_hosts):
        sniff_hosts.side_effect = [TransportError("sniff failed")]
        t = Transport(
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniff_on_connection_fail=True,
            max_retries=3,
            randomize_hosts=False,
        )
        t._verified_elasticsearch = True

        conn_err, conn_data = t.connection_pool.connections
        response = t.perform_request("GET", "/")
        self.assertEqual(json.loads(CLUSTER_NODES), response)
        self.assertEqual(1, sniff_hosts.call_count)
        self.assertEqual(1, len(conn_err.calls))
        self.assertEqual(1, len(conn_data.calls))

    def test_sniff_after_n_seconds(self):
        t = Transport(
            [{"data": CLUSTER_NODES}],
            connection_class=DummyConnection,
            sniffer_timeout=5,
        )
        t._verified_elasticsearch = True

        for _ in range(4):
            t.perform_request("GET", "/")
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertIsInstance(t.get_connection(), DummyConnection)
        t.last_sniff = time.time() - 5.1

        t.perform_request("GET", "/")
        self.assertEqual(1, len(t.connection_pool.connections))
        self.assertEqual("http://1.1.1.1:123", t.get_connection().host)
        self.assertTrue(time.time() - 1 < t.last_sniff < time.time() + 0.01)

    def test_sniff_7x_publish_host(self):
        # Test the response shaped when a 7.x node has publish_host set
        # and the returend data is shaped in the fqdn/ip:port format.
        t = Transport(
            [{"data": CLUSTER_NODES_7x_PUBLISH_HOST}],
            connection_class=DummyConnection,
            sniff_timeout=42,
        )
        t._verified_elasticsearch = True
        t.sniff_hosts()
        # Ensure we parsed out the fqdn and port from the fqdn/ip:port string.
        self.assertEqual(
            t.connection_pool.connection_opts[0][1],
            {"host": "somehost.tld", "port": 123},
        )

    @patch("elasticsearch.transport.Transport.sniff_hosts")
    def test_sniffing_disabled_on_cloud_instances(self, sniff_hosts):
        t = Transport(
            [{}],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )
        t._verified_elasticsearch = True

        self.assertFalse(t.sniff_on_connection_fail)
        self.assertIs(sniff_hosts.call_args, None)  # Assert not called.


TAGLINE = "You Know, for Search"


@pytest.mark.parametrize(
    ["headers", "response", "product_error"],
    [
        # All empty.
        ({}, {}, _ProductChecker.UNSUPPORTED_PRODUCT),
        # Don't check the product header immediately, need to check version first.
        (
            {"x-elastic-product": "Elasticsearch"},
            {},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
        # Version not there.
        ({}, {"tagline": TAGLINE}, _ProductChecker.UNSUPPORTED_PRODUCT),
        # Version is nonsense
        (
            {},
            {"version": "1.0.0", "tagline": TAGLINE},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
        # Version number not there
        ({}, {"version": {}, "tagline": TAGLINE}, _ProductChecker.UNSUPPORTED_PRODUCT),
        # Version number is nonsense
        (
            {},
            {"version": {"number": "nonsense"}, "tagline": TAGLINE},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
        # Version number way in the past
        (
            {},
            {"version": {"number": "1.0.0"}, "tagline": TAGLINE},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
        # Version number way in the future
        (
            {},
            {"version": {"number": "999.0.0"}, "tagline": TAGLINE},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
        # Build flavor not supposed to be missing
        (
            {},
            {"version": {"number": "7.13.0"}, "tagline": TAGLINE},
            _ProductChecker.UNSUPPORTED_DISTRIBUTION,
        ),
        # Build flavor is 'oss'
        (
            {},
            {
                "version": {"number": "7.10.0", "build_flavor": "oss"},
                "tagline": TAGLINE,
            },
            _ProductChecker.UNSUPPORTED_DISTRIBUTION,
        ),
        # Build flavor is nonsense
        (
            {},
            {
                "version": {"number": "7.13.0", "build_flavor": "nonsense"},
                "tagline": TAGLINE,
            },
            _ProductChecker.UNSUPPORTED_DISTRIBUTION,
        ),
        # Tagline is nonsense
        (
            {},
            {"version": {"number": "7.1.0-SNAPSHOT"}, "tagline": "nonsense"},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
        # Product header is not supposed to be missing
        (
            {},
            {"version": {"number": "7.14.0"}, "tagline": "You Know, for Search"},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
        # Product header is nonsense
        (
            {"x-elastic-product": "nonsense"},
            {"version": {"number": "7.15.0"}, "tagline": TAGLINE},
            _ProductChecker.UNSUPPORTED_PRODUCT,
        ),
    ],
)
def test_verify_elasticsearch_errors(headers, response, product_error):
    assert _ProductChecker.check_product(headers, response) == product_error


@pytest.mark.parametrize(
    ["headers", "response"],
    [
        ({}, {"version": {"number": "6.0.0"}, "tagline": TAGLINE}),
        ({}, {"version": {"number": "6.99.99"}, "tagline": TAGLINE}),
        (
            {},
            {
                "version": {"number": "7.0.0", "build_flavor": "default"},
                "tagline": TAGLINE,
            },
        ),
        (
            {},
            {
                "version": {"number": "7.13.99", "build_flavor": "default"},
                "tagline": TAGLINE,
            },
        ),
        (
            {"x-elastic-product": "Elasticsearch"},
            {
                "version": {"number": "7.14.0", "build_flavor": "default"},
                "tagline": TAGLINE,
            },
        ),
        (
            {"x-elastic-product": "Elasticsearch"},
            {
                "version": {"number": "7.99.99", "build_flavor": "default"},
                "tagline": TAGLINE,
            },
        ),
        (
            {"x-elastic-product": "Elasticsearch"},
            {
                "version": {"number": "8.0.0"},
            },
        ),
    ],
)
def test_verify_elasticsearch_passes(headers, response):
    result = _ProductChecker.check_product(headers, response)
    assert result == _ProductChecker.SUCCESS
    assert result is True


@pytest.mark.parametrize(
    ["headers", "data"],
    [
        (
            {},
            '{"version":{"number":"6.99.0"},"tagline":"You Know, for Search"}',
        ),
        (
            {},
            """{
  "name" : "io",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "HaMHUswUSGGnzla8B17Iqw",
  "version" : {
    "number" : "7.6.0",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "7f634e9f44834fbc12724506cc1da681b0c3b1e3",
    "build_date" : "2020-02-06T00:09:00.449973Z",
    "build_snapshot" : false,
    "lucene_version" : "8.4.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}""",
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
def test_verify_elasticsearch(headers, data):
    t = Transport(
        [{"data": data, "headers": headers}], connection_class=DummyConnection
    )
    t.perform_request("GET", "/_search")
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
def test_verify_elasticsearch_skips_on_auth_errors(exception_cls):
    t = Transport(
        [{"exception": exception_cls(exception_cls.status_code)}],
        connection_class=DummyConnection,
    )

    with pytest.warns(ElasticsearchWarning) as warns:
        with pytest.raises(exception_cls):
            t.perform_request(
                "GET",
                "/_search",
                headers={"Authorization": "testme"},
                params={"request_timeout": 3},
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
                "timeout": 3,
            },
        ),
        (
            ("GET", "/_search", {}, None),
            {
                "headers": {
                    "Authorization": "testme",
                },
                "ignore": (),
                "timeout": 3,
            },
        ),
    ]


def test_multiple_requests_verify_elasticsearch_success():
    try:
        import threading
    except ImportError:
        return pytest.skip("Requires the 'threading' module")

    t = Transport(
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

    class RequestThread(threading.Thread):
        def run(self):
            try:
                results.append(t.perform_request("GET", "/_search"))
            except Exception as e:
                results.append(e)
            completed_at.append(time.time())

    # Execute a bunch of requests concurrently.
    threads = []
    start_time = time.time()
    for _ in range(10):
        thread = RequestThread()
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end_time = time.time()

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
def test_multiple_requests_verify_elasticsearch_product_error(
    build_flavor, tagline, product_error, error_message
):
    try:
        import threading
    except ImportError:
        return pytest.skip("Requires the 'threading' module")

    t = Transport(
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

    class RequestThread(threading.Thread):
        def run(self):
            try:
                results.append(t.perform_request("GET", "/_search"))
            except Exception as e:
                results.append(e)
            completed_at.append(time.time())

    # Execute a bunch of requests concurrently.
    threads = []
    start_time = time.time()
    for _ in range(10):
        thread = RequestThread()
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end_time = time.time()

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
def test_multiple_requests_verify_elasticsearch_retry_on_errors(error_cls):
    try:
        import threading
    except ImportError:
        return pytest.skip("Requires the 'threading' module")

    t = Transport(
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

    class RequestThread(threading.Thread):
        def run(self):
            try:
                results.append(t.perform_request("GET", "/_search"))
            except Exception as e:
                results.append(e)
            completed_at.append(time.time())

    # Execute a bunch of requests concurrently.
    threads = []
    start_time = time.time()
    for _ in range(5):
        thread = RequestThread()
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    end_time = time.time()

    # Exactly 5 results completed
    assert len(results) == 5

    # All results were errors and not wrapped in 'UnsupportedProductError'
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

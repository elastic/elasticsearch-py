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
import re
import time
import warnings

import pytest
from elastic_transport import ApiResponseMeta, BaseNode, HttpHeaders, NodeConfig
from elastic_transport.client_utils import DEFAULT
from mock import patch

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import (
    ConnectionError,
    ElasticsearchWarning,
    TransportError,
    UnsupportedProductError,
)
from elasticsearch.transport import get_host_info

sniffing_xfail = pytest.mark.xfail(strict=True)


class DummyNode(BaseNode):
    def __init__(self, config: NodeConfig):
        self.resp_status = config._extras.pop("status", 200)
        self.resp_error = config._extras.pop("exception", None)
        self.resp_data = config._extras.pop("data", b"{}")
        self.resp_headers = config._extras.pop(
            "headers", {"X-elastic-product": "Elasticsearch"}
        )
        self.calls = []

        super().__init__(config)

    def perform_request(self, *args, **kwargs):
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


class TestHostsInfoCallback:
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
        assert [1, 2, 3, 4] == chosen


class TestTransport:
    def test_request_timeout_extracted_from_params_and_passed(self):
        client = Elasticsearch(
            "http://localhost:9200", meta_header=False, node_class=DummyNode
        )

        client.info(params={"request_timeout": 42})
        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][0] == ("GET", "/")
        assert calls[0][1]["request_timeout"] == 42

    def test_opaque_id(self):
        client = Elasticsearch(
            "http://localhost:9200",
            meta_header=False,
            node_class=DummyNode,
            opaque_id="app-1",
        )

        client.info()
        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][0] == ("GET", "/")
        assert calls[0][1]["headers"]["x-opaque-id"] == "app-1"

        # Now try with an 'x-opaque-id' set on perform_request().
        client.info(opaque_id="request-2")
        calls = client.transport.node_pool.get().calls
        assert 2 == len(calls)
        assert calls[1][0] == ("GET", "/")
        assert calls[1][1]["headers"]["x-opaque-id"] == "request-2"

    def test_request_with_custom_user_agent_header(self):
        client = Elasticsearch(
            "http://localhost:9200", meta_header=False, node_class=DummyNode
        )

        client.info(headers={"User-Agent": "my-custom-value/1.2.3"})
        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][0] == ("GET", "/")
        assert calls[0][1]["headers"]["user-agent"] == "my-custom-value/1.2.3"

    def test_client_meta_header(self):
        client = Elasticsearch("http://localhost:9200", node_class=DummyNode)
        client.info()

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        headers = calls[0][1]["headers"]
        assert re.search(
            r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?$", headers["x-elastic-client-meta"]
        )

        class DummyNodeWithMeta(DummyNode):
            _CLIENT_META_HTTP_CLIENT = ("dm", "1.2.3")

        client = Elasticsearch("http://localhost:9200", node_class=DummyNodeWithMeta)
        client.info(headers={"CustoM": "header"})

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        headers = calls[0][1]["headers"]
        assert re.search(
            r"^es=[0-9.]+p?,py=[0-9.]+p?,t=[0-9.]+p?,dm=1.2.3$",
            headers["x-elastic-client-meta"],
        )
        assert headers["Custom"] == "header"

    def test_client_meta_header_not_sent(self):
        client = Elasticsearch(
            "http://localhost:9200", meta_header=False, node_class=DummyNode
        )
        client.info()

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][1]["headers"] == {"content-type": "application/json"}

    def test_meta_header_type_error(self):
        with pytest.raises(TypeError) as e:
            Elasticsearch("https://localhost:9200", meta_header=1)
        assert str(e.value) == "'meta_header' must be of type bool"

    def test_body_surrogates_replaced_encoded_into_bytes(self):
        client = Elasticsearch("http://localhost:9200", node_class=DummyNode)
        client.search(body="你好\uda6a")

        calls = client.transport.node_pool.get().calls
        assert 1 == len(calls)
        assert calls[0][1]["body"] == b"\xe4\xbd\xa0\xe5\xa5\xbd\xed\xa9\xaa"

    def test_kwargs_passed_on_to_node_pool(self):
        dt = object()
        client = Elasticsearch("http://localhost:9200", dead_node_backoff_factor=dt)
        assert dt is client.transport.node_pool.dead_node_backoff_factor

    def test_custom_node_class(self):
        class MyConnection(object):
            def __init__(self, *_, **__):
                pass

        client = Elasticsearch("http://localhost:9200", node_class=MyConnection)
        assert 1 == len(client.transport.node_pool.all_nodes)
        assert isinstance(
            client.transport.node_pool.all_nodes.popitem()[1], MyConnection
        )

    def test_request_will_fail_after_x_retries(self):
        client = Elasticsearch(
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
            client.info()
        calls = client.transport.node_pool.get().calls
        assert 4 == len(calls)
        assert len(e.value.errors) == 3
        del calls[:]

        with pytest.raises(ConnectionError):
            client.options(max_retries=5).info()
        calls = client.transport.node_pool.get().calls
        assert 6 == len(calls)

    def test_failed_connection_will_be_marked_as_dead(self):
        client = Elasticsearch(
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
            client.info()
        assert 0 == len(client.transport.node_pool.alive_nodes)

    def test_resurrected_connection_will_be_marked_as_live_on_success(self):
        client = Elasticsearch(
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

        client.info()

        assert len(client.transport.node_pool.alive_nodes) == 1
        assert len(client.transport.node_pool.dead_consecutive_failures) == 1

    @sniffing_xfail
    def test_sniff_will_use_seed_connections(self):
        t = Transport(  # noqa: F821
            [{"data": CLUSTER_NODES}], connection_class=DummyNode
        )
        t.set_connections([{"data": "invalid"}])

        t.sniff_hosts()
        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    @sniffing_xfail
    def test_sniff_on_start_fetches_and_uses_nodes_list(self):
        t = Transport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_start=True,
        )
        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    @sniffing_xfail
    def test_sniff_on_start_ignores_sniff_timeout(self):
        t = Transport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_start=True,
            sniff_timeout=12,
        )
        assert (("GET", "/_nodes/_all/http"), {"timeout": None}) == t.seed_connections[
            0
        ].calls[0]

    @sniffing_xfail
    def test_sniff_uses_sniff_timeout(self):
        t = Transport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_timeout=42,
        )
        t.sniff_hosts()
        assert (("GET", "/_nodes/_all/http"), {"timeout": 42}) == t.seed_connections[
            0
        ].calls[0]

    @sniffing_xfail
    def test_sniff_reuses_connection_instances_if_possible(self):
        t = Transport(  # noqa: F821
            [{"data": CLUSTER_NODES}, {"host": "1.1.1.1", "port": 123}],
            connection_class=DummyNode,
            randomize_hosts=False,
        )
        connection = t.connection_pool.connections[1]

        t.sniff_hosts()
        assert 1 == len(t.connection_pool.connections)
        assert connection is t.get_connection()

    @sniffing_xfail
    def test_sniff_on_fail_triggers_sniffing_on_fail(self):
        t = Transport(  # noqa: F821
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_connection_fail=True,
            max_retries=0,
            randomize_hosts=False,
        )

        with pytest.raises(ConnectionError):
            t.perform_request("GET", "/")
        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host

    @sniffing_xfail
    @patch("elasticsearch.transport.Transport.sniff_hosts")
    def test_sniff_on_fail_failing_does_not_prevent_retires(self, sniff_hosts):
        sniff_hosts.side_effect = [TransportError("sniff failed")]
        t = Transport(  # noqa: F821
            [{"exception": ConnectionError("abandon ship")}, {"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniff_on_connection_fail=True,
            max_retries=3,
            randomize_hosts=False,
        )

        conn_err, conn_data = t.connection_pool.connections
        response = t.perform_request("GET", "/")
        assert json.loads(CLUSTER_NODES) == response
        assert 1 == sniff_hosts.call_count
        assert 1 == len(conn_err.calls)
        assert 1 == len(conn_data.calls)

    @sniffing_xfail
    def test_sniff_after_n_seconds(self):
        t = Transport(  # noqa: F821
            [{"data": CLUSTER_NODES}],
            connection_class=DummyNode,
            sniffer_timeout=5,
        )

        for _ in range(4):
            t.perform_request("GET", "/")
        assert 1 == len(t.connection_pool.connections)
        assert isinstance(t.get_connection(), DummyNode)
        t.last_sniff = time.time() - 5.1

        t.perform_request("GET", "/")
        assert 1 == len(t.connection_pool.connections)
        assert "http://1.1.1.1:123" == t.get_connection().host
        assert time.time() - 1 < t.last_sniff < time.time() + 0.01

    @sniffing_xfail
    def test_sniff_7x_publish_host(self):
        # Test the response shaped when a 7.x node has publish_host set
        # and the returend data is shaped in the fqdn/ip:port format.
        t = Transport(  # noqa: F821
            [{"data": CLUSTER_NODES_7x_PUBLISH_HOST}],
            connection_class=DummyNode,
            sniff_timeout=42,
        )
        t.sniff_hosts()
        # Ensure we parsed out the fqdn and port from the fqdn/ip:port string.
        assert t.connection_pool.connection_opts[0][1] == {
            "host": "somehost.tld",
            "port": 123,
        }

    @sniffing_xfail
    @patch("elasticsearch.transport.Transport.sniff_hosts")
    def test_sniffing_disabled_on_cloud_instances(self, sniff_hosts):
        t = Transport(  # noqa: F821
            [{}],
            sniff_on_start=True,
            sniff_on_connection_fail=True,
            cloud_id="cluster:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5NyQ0ZmE4ODIxZTc1NjM0MDMyYmVkMWNmMjIxMTBlMmY5Ng==",
        )

        assert not t.sniff_on_connection_fail
        assert sniff_hosts.call_args is None  # Assert not called.


@pytest.mark.parametrize("headers", [{}, {"X-elastic-product": "BAD HEADER"}])
def test_unsupported_product_error(headers):
    client = Elasticsearch(
        [NodeConfig("http", "localhost", 9200, _extras={"headers": headers})],
        meta_header=False,
        node_class=DummyNode,
    )

    with pytest.raises(UnsupportedProductError) as e:
        client.info()
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
def test_transport_error_raised_before_product_error(status):
    client = Elasticsearch(
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
        client.info()
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
def test_warning_header(headers):
    client = Elasticsearch(
        [NodeConfig("http", "localhost", 9200, _extras={"headers": headers})],
        meta_header=False,
        node_class=DummyNode,
    )

    with warnings.catch_warnings(record=True) as w:
        client.info()

    assert len(w) == headers["Warning"].count("299")
    assert w[0].category == ElasticsearchWarning
    assert (
        str(w[0].message)
        == "[xpack.monitoring.history.duration] setting was deprecated in Elasticsearch and will be removed in a future release! See the breaking changes documentation for the next major version."
    )

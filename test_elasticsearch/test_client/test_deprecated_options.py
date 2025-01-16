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

import warnings

import pytest

from elasticsearch import Elasticsearch, JsonSerializer

EXPECTED_SERIALIZERS = {
    "application/vnd.mapbox-vector-tile",
    "application/x-ndjson",
    "application/json",
    "text/*",
    "application/vnd.elasticsearch+json",
    "application/vnd.elasticsearch+x-ndjson",
}


try:
    import pyarrow as pa

    EXPECTED_SERIALIZERS.add("application/vnd.apache.arrow.stream")
except ImportError:
    pa = None


def test_sniff_on_connection_fail():
    with warnings.catch_warnings(record=True) as w:
        client = Elasticsearch("http://localhost:9200", sniff_on_connection_fail=True)
    assert client.transport._sniff_on_node_failure is True
    assert len(w) == 1
    assert w[0].category == DeprecationWarning
    assert str(w[0].message) == (
        "The 'sniff_on_connection_fail' parameter is deprecated in favor of 'sniff_on_node_failure'"
    )

    with pytest.raises(ValueError) as e:
        Elasticsearch(
            "http://localhost:9200",
            sniff_on_connection_fail=True,
            sniff_on_node_failure=True,
        )
    assert (
        str(e.value)
        == "Can't specify both 'sniff_on_connection_fail' and 'sniff_on_node_failure', instead only specify 'sniff_on_node_failure'"
    )


def test_sniffer_timeout():
    with warnings.catch_warnings(record=True) as w:
        client = Elasticsearch("http://localhost:9200", sniffer_timeout=1)
    assert client.transport._min_delay_between_sniffing == 1
    assert len(w) == 1
    assert w[0].category == DeprecationWarning
    assert str(w[0].message) == (
        "The 'sniffer_timeout' parameter is deprecated in favor of 'min_delay_between_sniffing'"
    )

    with pytest.raises(ValueError) as e:
        Elasticsearch(
            "http://localhost:9200", sniffer_timeout=1, min_delay_between_sniffing=1
        )
    assert (
        str(e.value)
        == "Can't specify both 'sniffer_timeout' and 'min_delay_between_sniffing', instead only specify 'min_delay_between_sniffing'"
    )


def test_randomize_hosts():
    with warnings.catch_warnings(record=True) as w:
        Elasticsearch("http://localhost:9200", randomize_hosts=True)
    assert len(w) == 1
    assert w[0].category == DeprecationWarning
    assert str(w[0].message) == (
        "The 'randomize_hosts' parameter is deprecated in favor of 'randomize_nodes_in_pool'"
    )

    with pytest.raises(ValueError) as e:
        Elasticsearch(
            "http://localhost:9200", randomize_hosts=True, randomize_nodes_in_pool=True
        )
    assert (
        str(e.value)
        == "Can't specify both 'randomize_hosts' and 'randomize_nodes_in_pool', instead only specify 'randomize_nodes_in_pool'"
    )


def test_http_auth():
    with warnings.catch_warnings(record=True) as w:
        client = Elasticsearch(
            "http://localhost:9200", http_auth=("username", "password")
        )

    assert len(w) == 1
    assert w[0].category == DeprecationWarning
    assert (
        str(w[0].message)
        == "The 'http_auth' parameter is deprecated. Use 'basic_auth' or 'bearer_auth' parameters instead"
    )
    assert client._headers["Authorization"] == "Basic dXNlcm5hbWU6cGFzc3dvcmQ="

    with pytest.raises(ValueError) as e:
        Elasticsearch(
            "http://localhost:9200",
            http_auth=("username", "password"),
            basic_auth=("username", "password"),
        )
    assert (
        str(e.value)
        == "Can't specify both 'http_auth' and 'basic_auth', instead only specify 'basic_auth'"
    )


def test_serializer_and_serializers():
    with pytest.raises(ValueError) as e:
        Elasticsearch(
            "http://localhost:9200",
            serializer=JsonSerializer(),
            serializers={"application/json": JsonSerializer()},
        )
    assert str(e.value) == (
        "Can't specify both 'serializer' and 'serializers' parameters together. "
        "Instead only specify one of the other."
    )

    class CustomSerializer(JsonSerializer):
        pass

    client = Elasticsearch("http://localhost:9200", serializer=CustomSerializer())
    assert isinstance(
        client.transport.serializers.get_serializer("application/json"),
        CustomSerializer,
    )
    assert set(client.transport.serializers.serializers.keys()) == EXPECTED_SERIALIZERS

    client = Elasticsearch(
        "http://localhost:9200",
        serializers={
            "application/json": CustomSerializer(),
            "application/cbor": CustomSerializer(),
        },
    )
    assert isinstance(
        client.transport.serializers.get_serializer("application/json"),
        CustomSerializer,
    )
    expected = EXPECTED_SERIALIZERS | {"application/cbor"}
    assert set(client.transport.serializers.serializers.keys()) == expected

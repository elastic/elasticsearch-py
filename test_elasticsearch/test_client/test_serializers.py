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

from elasticsearch import Elasticsearch
from test_elasticsearch.test_cases import DummyTransportTestCase

EXPECTED_SERIALIZERS = {
    "application/json",
    "text/*",
    "application/x-ndjson",
    "application/vnd.mapbox-vector-tile",
    "application/vnd.elasticsearch+json",
    "application/vnd.elasticsearch+x-ndjson",
}


try:
    import pyarrow as pa

    EXPECTED_SERIALIZERS.add("application/vnd.apache.arrow.stream")
except ImportError:
    pa = None


class TestSerializers(DummyTransportTestCase):
    def test_compat_mode_on_by_default(self):
        calls = self.client.transport.calls

        # Get, never uses a body
        self.client.get(index="test0", id="1")
        assert len(calls) == 1
        assert calls[("GET", "/test0/_doc/1")][0]["headers"] == {
            "Accept": "application/vnd.elasticsearch+json; compatible-with=8"
        }

        # Search with body
        self.client.search(index="test1", query={"match_all": {}})
        assert len(calls) == 2
        assert calls[("POST", "/test1/_search")][0]["headers"] == {
            "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
            "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        # Search without body
        self.client.search(index="test2")
        assert len(calls) == 3
        assert calls[("POST", "/test2/_search")][0]["headers"] == {
            "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
        }

        # Multiple mimetypes in Accept
        self.client.cat.nodes()
        assert len(calls) == 4
        assert calls[("GET", "/_cat/nodes")][0]["headers"] == {
            # text/plain isn't modified.
            "Accept": "text/plain,application/vnd.elasticsearch+json; compatible-with=8",
        }

        # Bulk uses x-ndjson
        self.client.bulk(operations=[])
        assert len(calls) == 5
        assert calls[("PUT", "/_bulk")][0]["headers"] == {
            "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
            "Content-Type": "application/vnd.elasticsearch+x-ndjson; compatible-with=8",
        }

        # Mapbox vector tiles
        self.client.search_mvt(
            index="test3",
            field="field",
            zoom="z",
            y="y",
            x="x",
            query={"match_all": {}},
        )
        assert len(calls) == 6
        assert calls[("POST", "/test3/_mvt/field/z/x/y")][0]["headers"] == {
            "Accept": "application/vnd.elasticsearch+vnd.mapbox-vector-tile; compatible-with=8",
            "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8",
        }

    @pytest.mark.parametrize("mime_subtype", ["json", "x-ndjson"])
    def test_compat_serializers_used_when_given_non_compat(
        self, mime_subtype: str
    ) -> None:
        class CustomSerializer:
            pass

        ser = CustomSerializer()
        client = Elasticsearch(
            "https://localhost:9200", serializers={f"application/{mime_subtype}": ser}
        )
        serializers = client.transport.serializers.serializers

        assert set(serializers.keys()) == EXPECTED_SERIALIZERS
        assert serializers[f"application/{mime_subtype}"] is ser
        assert serializers[f"application/vnd.elasticsearch+{mime_subtype}"] is ser

    @pytest.mark.parametrize("mime_subtype", ["json", "x-ndjson"])
    def test_compat_serializers_used_when_given_compat(self, mime_subtype: str) -> None:
        class CustomSerializer:
            pass

        ser1 = CustomSerializer()
        ser2 = CustomSerializer()
        client = Elasticsearch(
            "https://localhost:9200",
            serializers={
                f"application/{mime_subtype}": ser1,
                f"application/vnd.elasticsearch+{mime_subtype}": ser2,
            },
        )
        serializers = client.transport.serializers.serializers
        assert set(serializers.keys()) == EXPECTED_SERIALIZERS
        assert serializers[f"application/{mime_subtype}"] is ser1
        assert serializers[f"application/vnd.elasticsearch+{mime_subtype}"] is ser2

    def test_compat_serializer_used_when_given_non_compat(self) -> None:
        class CustomSerializer:
            mimetype: str = "application/json"

        ser = CustomSerializer()
        client = Elasticsearch("https://localhost:9200", serializer=ser)
        serializers = client.transport.serializers.serializers
        assert set(serializers.keys()) == EXPECTED_SERIALIZERS
        assert serializers["application/json"] is ser
        assert serializers["application/vnd.elasticsearch+json"] is ser

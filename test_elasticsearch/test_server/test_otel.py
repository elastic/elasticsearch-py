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

import os

import pytest

import elasticsearch
import elasticsearch.helpers

from ..test_otel import setup_tracing

pytestmark = [
    pytest.mark.skipif(
        "TEST_WITH_OTEL" not in os.environ, reason="TEST_WITH_OTEL is not set"
    ),
    pytest.mark.otel,
]


def test_otel_end_to_end(sync_client):
    tracer, memory_exporter = setup_tracing()
    sync_client._otel.tracer = tracer

    resp = sync_client.search(index="logs-*", query={"match_all": {}})
    assert resp.meta.status == 200

    spans = memory_exporter.get_finished_spans()
    assert len(spans) == 1
    assert spans[0].name == "search"
    expected_attributes = {
        "http.request.method": "POST",
        "db.system": "elasticsearch",
        "db.operation": "search",
        "db.elasticsearch.path_parts.index": "logs-*",
    }
    # Assert expected atttributes are here, but allow other attributes too
    # to make this test robust to elastic-transport changes
    assert expected_attributes.items() <= spans[0].attributes.items()


@pytest.mark.parametrize(
    "bulk_helper_name", ["bulk", "streaming_bulk", "parallel_bulk"]
)
def test_otel_bulk(sync_client, elasticsearch_url, bulk_helper_name):
    tracer, memory_exporter = setup_tracing()

    # Create a new client with our tracer
    sync_client = sync_client.options()
    sync_client._otel.tracer = tracer
    # "Disable" options to keep our custom tracer
    sync_client.options = lambda: sync_client

    docs = [{"answer": x, "helper": bulk_helper_name, "_id": x} for x in range(10)]
    bulk_function = getattr(elasticsearch.helpers, bulk_helper_name)
    if bulk_helper_name == "bulk":
        success, failed = bulk_function(
            sync_client, docs, index="test-index", chunk_size=2, refresh=True
        )
        assert success, failed == (5, 0)
    else:
        for ok, resp in bulk_function(
            sync_client, docs, index="test-index", chunk_size=2, refresh=True
        ):
            assert ok is True

    memory_exporter.shutdown()

    assert 10 == sync_client.count(index="test-index")["count"]
    assert {"answer": 4, "helper": bulk_helper_name} == sync_client.get(
        index="test-index", id=4
    )["_source"]

    spans = list(memory_exporter.get_finished_spans())
    parent_span = spans.pop()
    assert parent_span.name == f"helpers.{bulk_helper_name}"
    assert parent_span.attributes == {
        "db.system": "elasticsearch",
        "db.operation": f"helpers.{bulk_helper_name}",
        "http.request.method": "null",
    }

    assert len(spans) == 5
    for span in spans:
        assert span.name == "bulk"
        expected_attributes = {
            "http.request.method": "PUT",
            "db.system": "elasticsearch",
            "db.operation": "bulk",
            "db.elasticsearch.path_parts.index": "test-index",
        }
        # Assert expected atttributes are here, but allow other attributes too
        # to make this test robust to elastic-transport changes
        assert expected_attributes.items() <= spans[0].attributes.items()
        assert span.parent.trace_id == parent_span.context.trace_id

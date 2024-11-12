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
from test_elasticsearch.utils import CA_CERTS

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider, export
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
        InMemorySpanExporter,
    )
except ModuleNotFoundError:
    pass

pytestmark = [
    pytest.mark.skipif(
        "TEST_WITH_OTEL" not in os.environ, reason="TEST_WITH_OTEL is not set"
    ),
    pytest.mark.otel,
]


def test_otel_end_to_end(monkeypatch, elasticsearch_url: str):
    # Sets the global default tracer provider
    tracer_provider = TracerProvider()
    memory_exporter = InMemorySpanExporter()
    span_processor = export.SimpleSpanProcessor(memory_exporter)
    tracer_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(tracer_provider)

    # Once OpenTelemetry is enabled by default, we can use the sync_client fixture instead
    monkeypatch.setenv("OTEL_PYTHON_INSTRUMENTATION_ELASTICSEARCH_ENABLED", "true")
    kw = {}
    if elasticsearch_url.startswith("https://"):
        kw["ca_certs"] = CA_CERTS
    client = elasticsearch.Elasticsearch(elasticsearch_url, **kw)

    resp = client.search(index="logs-*", query={"match_all": {}})
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

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
import uuid
from typing import Dict, Iterator

import pytest

from elasticsearch import Elasticsearch

from ._test_utils import RequestSavingTransport


@pytest.fixture
def es_client(elasticsearch_url: str) -> Iterator[Elasticsearch]:
    client = _create_es_client(elasticsearch_url)

    yield client

    # clear indices
    _clear_test_indices(client)

    # clear all test pipelines
    try:
        response = client.ingest.get_pipeline(id="test_*,*_sparse_embedding")

        for pipeline_id, _ in response.items():
            try:
                client.ingest.delete_pipeline(id=pipeline_id)
                print(f"Deleted pipeline: {pipeline_id}")  # noqa: T201
            except Exception as e:
                print(f"Pipeline error: {e}")  # noqa: T201

    except Exception:
        pass
    finally:
        client.close()


@pytest.fixture
def requests_saving_client(
    elasticsearch_url: str,
) -> Iterator[Elasticsearch]:
    client = _create_es_client(
        elasticsearch_url, es_kwargs={"transport_class": RequestSavingTransport}
    )

    try:
        yield client
    finally:
        client.close()


@pytest.fixture(scope="function")
def index_name() -> str:
    return f"test_{uuid.uuid4().hex}"


def _clear_test_indices(client: Elasticsearch) -> None:
    response = client.indices.get(index="_all")
    index_names = response.keys()
    for index_name in index_names:
        if index_name.startswith("test_"):
            client.indices.delete(index=index_name)
    client.indices.refresh(index="_all")


def _create_es_client(elasticsearch_url: str, es_kwargs: Dict = {}) -> Elasticsearch:
    if not elasticsearch_url:
        elasticsearch_url = os.environ.get("ES_URL", "http://localhost:9200")
    cloud_id = os.environ.get("ES_CLOUD_ID")
    api_key = os.environ.get("ES_API_KEY")

    if cloud_id:
        es_params = {"es_cloud_id": cloud_id, "es_api_key": api_key}
    else:
        es_params = {"es_url": elasticsearch_url}

    if "es_cloud_id" in es_params:
        return Elasticsearch(
            cloud_id=es_params["es_cloud_id"],
            api_key=es_params["es_api_key"],
            **es_kwargs,
        )
    return Elasticsearch(hosts=[es_params["es_url"]], **es_kwargs)

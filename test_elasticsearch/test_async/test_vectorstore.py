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

from unittest.mock import AsyncMock, Mock

import pytest
from elastic_transport import ApiResponseMeta, HttpHeaders, NodeConfig

from elasticsearch import AsyncElasticsearch, BadRequestError
from elasticsearch.helpers.vectorstore import AsyncBM25Strategy, AsyncVectorStore

pytestmark = pytest.mark.anyio


def create_error(message):
    return BadRequestError(
        message=message,
        meta=ApiResponseMeta(
            status=400,
            http_version="1.1",
            headers=HttpHeaders(),
            duration=0,
            node=NodeConfig("http", "localhost", 9200),
        ),
        body={"error": {"type": message}, "status": 400},
    )


@pytest.fixture
def store():
    return AsyncVectorStore(
        AsyncElasticsearch("http://localhost:9200"),
        index="test-index",
        retrieval_strategy=AsyncBM25Strategy(),
    )


async def test_existing_index_skips_creation(store, mocker):
    mocker.patch.object(
        store.client.indices,
        "exists",
        new_callable=AsyncMock,
        return_value=Mock(meta=Mock(status=200)),
    )
    create = mocker.patch.object(store.client.indices, "create", new_callable=AsyncMock)
    before = mocker.patch.object(
        store.retrieval_strategy, "before_index_creation", new_callable=AsyncMock
    )
    await store._create_index_if_not_exists()
    create.assert_not_awaited()
    before.assert_not_awaited()


async def test_missing_index_is_created(store, mocker):
    mocker.patch.object(
        store.client.indices,
        "exists",
        new_callable=AsyncMock,
        return_value=Mock(meta=Mock(status=404)),
    )
    create = mocker.patch.object(store.client.indices, "create", new_callable=AsyncMock)
    await store._create_index_if_not_exists()
    create.assert_awaited_once_with(
        index="test-index",
        mappings={
            "properties": {"text_field": {"type": "text", "similarity": "custom_bm25"}}
        },
        settings={"similarity": {"custom_bm25": {"type": "BM25"}}},
    )


async def test_concurrent_index_creation_allows_upload(store, mocker):
    mocker.patch.object(
        store.client.indices,
        "exists",
        new_callable=AsyncMock,
        return_value=Mock(meta=Mock(status=404)),
    )
    create = mocker.patch.object(
        store.client.indices,
        "create",
        new_callable=AsyncMock,
        side_effect=create_error("resource_already_exists_exception"),
    )
    bulk = mocker.patch(
        "elasticsearch.helpers.vectorstore._async.vectorstore.async_bulk",
        return_value=(1, 0),
    )
    assert await store.add_texts(["document"], ids=["1"]) == ["1"]
    create.assert_awaited_once()
    bulk.assert_awaited_once_with(
        store.client,
        [
            {
                "_op_type": "index",
                "_index": "test-index",
                "text_field": "document",
                "metadata": {},
                "_id": "1",
            }
        ],
        stats_only=True,
        refresh=True,
    )


@pytest.mark.parametrize(
    "message",
    [
        "illegal_argument_exception",
        "mapper_parsing_exception",
        "invalid_index_name_exception",
        "unrecognized error",
    ],
)
async def test_other_creation_errors_prevent_upload(store, mocker, message):
    mocker.patch.object(
        store.client.indices,
        "exists",
        new_callable=AsyncMock,
        return_value=Mock(meta=Mock(status=404)),
    )
    error = create_error(message)
    mocker.patch.object(
        store.client.indices, "create", new_callable=AsyncMock, side_effect=error
    )
    bulk = mocker.patch(
        "elasticsearch.helpers.vectorstore._async.vectorstore.async_bulk"
    )
    with pytest.raises(BadRequestError) as exc:
        await store.add_texts(["document"], ids=["1"])
    assert exc.value is error
    bulk.assert_not_awaited()


async def test_preparation_errors_are_not_suppressed(store, mocker):
    mocker.patch.object(
        store.client.indices,
        "exists",
        new_callable=AsyncMock,
        return_value=Mock(meta=Mock(status=404)),
    )
    error = create_error("resource_already_exists_exception")
    mocker.patch.object(
        store.retrieval_strategy,
        "before_index_creation",
        new_callable=AsyncMock,
        side_effect=error,
    )
    create = mocker.patch.object(store.client.indices, "create", new_callable=AsyncMock)
    with pytest.raises(BadRequestError) as exc:
        await store._create_index_if_not_exists()
    assert exc.value is error
    create.assert_not_awaited()

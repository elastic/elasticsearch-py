import os

import pytest

import pytest_asyncio
from elasticsearch import AsyncElasticsearch

from typing import AsyncGenerator

from elasticsearch.vectorstore._async._utils import async_model_is_deployed

from ._test_utils import (
    es_client_fixture,
)

from elasticsearch.vectorstore._async.embedding_service import (
    AsyncElasticsearchEmbeddings,
)

# deployed with
# https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-text-emb-vector-search-example.html
MODEL_ID = os.getenv("MODEL_ID", "sentence-transformers__msmarco-minilm-l-12-v3")
NUM_DIMENSIONS = int(os.getenv("NUM_DIMENTIONS", "384"))


@pytest_asyncio.fixture(autouse=True)
async def es_client() -> AsyncGenerator[AsyncElasticsearch, None]:
    async for x in es_client_fixture():
        yield x


@pytest.mark.asyncio
async def test_elasticsearch_embedding_documents(es_client: AsyncElasticsearch) -> None:
    """Test Elasticsearch embedding documents."""

    if not await async_model_is_deployed(es_client, MODEL_ID):
        pytest.skip(f"{MODEL_ID} model is not deployed in ML Node, skipping test")

    documents = ["foo bar", "bar foo", "foo"]
    embedding = AsyncElasticsearchEmbeddings(
        es_client=es_client, user_agent="test", model_id=MODEL_ID
    )
    output = await embedding.embed_documents(documents)
    assert len(output) == 3
    assert len(output[0]) == NUM_DIMENSIONS
    assert len(output[1]) == NUM_DIMENSIONS
    assert len(output[2]) == NUM_DIMENSIONS


@pytest.mark.asyncio
async def test_elasticsearch_embedding_query(es_client: AsyncElasticsearch) -> None:
    """Test Elasticsearch embedding query."""

    if not await async_model_is_deployed(es_client, MODEL_ID):
        pytest.skip(f"{MODEL_ID} model is not deployed in ML Node, skipping test")

    document = "foo bar"
    embedding = AsyncElasticsearchEmbeddings(
        es_client=es_client, user_agent="test", model_id=MODEL_ID
    )
    output = await embedding.embed_query(document)
    assert len(output) == NUM_DIMENSIONS

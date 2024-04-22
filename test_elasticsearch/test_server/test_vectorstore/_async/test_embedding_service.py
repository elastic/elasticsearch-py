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

from elasticsearch import AsyncElasticsearch
from elasticsearch.vectorstore._async._utils import model_is_deployed
from elasticsearch.vectorstore._async.embedding_service import (
    AsyncElasticsearchEmbeddings,
)

# deployed with
# https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-text-emb-vector-search-example.html
MODEL_ID = os.getenv("MODEL_ID", "sentence-transformers__msmarco-minilm-l-12-v3")
NUM_DIMENSIONS = int(os.getenv("NUM_DIMENTIONS", "384"))


@pytest.mark.asyncio
async def test_elasticsearch_embedding_documents(es_client: AsyncElasticsearch) -> None:
    """Test Elasticsearch embedding documents."""

    if not await model_is_deployed(es_client, MODEL_ID):
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

    if not await model_is_deployed(es_client, MODEL_ID):
        pytest.skip(f"{MODEL_ID} model is not deployed in ML Node, skipping test")

    document = "foo bar"
    embedding = AsyncElasticsearchEmbeddings(
        es_client=es_client, user_agent="test", model_id=MODEL_ID
    )
    output = await embedding.embed_query(document)
    assert len(output) == NUM_DIMENSIONS

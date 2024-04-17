import os

import pytest
from elasticsearch import AsyncElasticsearch

from elasticsearch.store.embedding_service import ElasticsearchEmbeddings

from ._test_utilities import model_is_deployed

# deployed with
# https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-text-emb-vector-search-example.html
MODEL_ID = os.getenv("MODEL_ID", "sentence-transformers__msmarco-minilm-l-12-v3")
NUM_DIMENSIONS = int(os.getenv("NUM_DIMENTIONS", "384"))

ES_URL = os.environ.get("ES_URL", "http://localhost:9200")
ES_CLIENT = AsyncElasticsearch(hosts=[ES_URL])


@pytest.mark.skipif(
    not model_is_deployed(ES_CLIENT, MODEL_ID),
    reason=f"{MODEL_ID} model is not deployed in ML Node, skipping test",
)
def test_elasticsearch_embedding_documents() -> None:
    """Test Elasticsearch embedding documents."""
    documents = ["foo bar", "bar foo", "foo"]
    embedding = ElasticsearchEmbeddings(
        agent_header="test", model_id=MODEL_ID, es_url=ES_URL
    )
    output = embedding.embed_documents(documents)
    assert len(output) == 3
    assert len(output[0]) == NUM_DIMENSIONS
    assert len(output[1]) == NUM_DIMENSIONS
    assert len(output[2]) == NUM_DIMENSIONS


@pytest.mark.skipif(
    not model_is_deployed(ES_CLIENT, MODEL_ID),
    reason=f"{MODEL_ID} model is not deployed in ML Node, skipping test",
)
def test_elasticsearch_embedding_query() -> None:
    """Test Elasticsearch embedding query."""
    document = "foo bar"
    embedding = ElasticsearchEmbeddings(
        agent_header="test", model_id=MODEL_ID, es_url=ES_URL
    )
    output = embedding.embed_query(document)
    assert len(output) == NUM_DIMENSIONS

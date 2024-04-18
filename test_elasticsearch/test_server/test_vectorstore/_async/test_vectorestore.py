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

import logging
import uuid
from functools import partial
from typing import Any, AsyncIterator, List, Optional, Union, cast

import pytest
import pytest_asyncio

from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import BulkIndexError
from elasticsearch.vectorstore._async import AsyncVectorStore
from elasticsearch.vectorstore._async._utils import model_is_deployed
from elasticsearch.vectorstore._async.strategies import (
    BM25,
    DenseVector,
    DenseVectorScriptScore,
    DistanceMetric,
    Semantic,
)

from ._test_utils import (
    AsyncConsistentFakeEmbeddings,
    AsyncFakeEmbeddings,
    AsyncRequestSavingTransport,
    create_requests_saving_client,
    es_client_fixture,
)

logging.basicConfig(level=logging.DEBUG)

"""
docker-compose up elasticsearch

By default runs against local docker instance of Elasticsearch.
To run against Elastic Cloud, set the following environment variables:
- ES_CLOUD_ID
- ES_API_KEY

Some of the tests require the following models to be deployed in the ML Node:
- elser (can be downloaded and deployed through Kibana and trained models UI)
- sentence-transformers__all-minilm-l6-v2 (can be deployed through the API,
  loaded via eland)

These tests that require the models to be deployed are skipped by default.
Enable them by adding the model name to the modelsDeployed list below.
"""

ELSER_MODEL_ID = ".elser_model_2"
TRANSFORMER_MODEL_ID = "sentence-transformers__all-minilm-l6-v2"


class TestElasticsearch:
    @pytest_asyncio.fixture
    async def es_client(self) -> AsyncIterator[AsyncElasticsearch]:
        async for x in es_client_fixture():
            yield x

    @pytest_asyncio.fixture
    async def requests_saving_client(self) -> AsyncIterator[AsyncElasticsearch]:
        client = create_requests_saving_client()
        try:
            yield client
        finally:
            await client.close()

    @pytest.fixture(scope="function")
    def index_name(self) -> str:
        """Return the index name."""
        return f"test_{uuid.uuid4().hex}"

    @pytest.mark.asyncio
    async def test_search_without_metadata(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search without metadata."""

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == {
                "knn": {
                    "field": "vector_field",
                    "filter": [],
                    "k": 1,
                    "num_candidates": 50,
                    "query_vector": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
                }
            }
            return query_body

        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(embedding_service=AsyncFakeEmbeddings()),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        output = await store.search("foo", k=1, custom_query=assert_query)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

    @pytest.mark.asyncio
    async def test_search_without_metadata_async(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search without metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(embedding_service=AsyncFakeEmbeddings()),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        output = await store.search("foo", k=1)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

    @pytest.mark.asyncio
    async def test_add_vectors(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """
        Test adding pre-built embeddings instead of using inference for the texts.
        This allows you to separate the embeddings text and the page_content
        for better proximity between user's question and embedded text.
        For example, your embedding text can be a question, whereas page_content
        is the answer.
        """
        embeddings = AsyncConsistentFakeEmbeddings()
        texts = ["foo1", "foo2", "foo3"]
        metadatas = [{"page": i} for i in range(len(texts))]

        """In real use case, embedding_input can be questions for each text"""
        embedding_vectors = await embeddings.embed_documents(texts)

        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(embedding_service=embeddings),
            es_client=es_client,
        )

        await store.add_texts(
            texts=texts, vectors=embedding_vectors, metadatas=metadatas
        )
        output = await store.search("foo1", k=1)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo1"]
        assert [doc["_source"]["metadata"]["page"] for doc in output] == [0]

    @pytest.mark.asyncio
    async def test_search_with_metadata(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search with metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(
                embedding_service=AsyncConsistentFakeEmbeddings()
            ),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        metadatas = [{"page": i} for i in range(len(texts))]
        await store.add_texts(texts=texts, metadatas=metadatas)

        output = await store.search("foo", k=1)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]
        assert [doc["_source"]["metadata"]["page"] for doc in output] == [0]

        output = await store.search("bar", k=1)
        assert [doc["_source"]["text_field"] for doc in output] == ["bar"]
        assert [doc["_source"]["metadata"]["page"] for doc in output] == [1]

    @pytest.mark.asyncio
    async def test_search_with_filter(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search with metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(embedding_service=AsyncFakeEmbeddings()),
            es_client=es_client,
        )

        texts = ["foo", "foo", "foo"]
        metadatas = [{"page": i} for i in range(len(texts))]
        await store.add_texts(texts=texts, metadatas=metadatas)

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == {
                "knn": {
                    "field": "vector_field",
                    "filter": [{"term": {"metadata.page": "1"}}],
                    "k": 3,
                    "num_candidates": 50,
                    "query_vector": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
                }
            }
            return query_body

        output = await store.search(
            query="foo",
            k=3,
            filter=[{"term": {"metadata.page": "1"}}],
            custom_query=assert_query,
        )
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]
        assert [doc["_source"]["metadata"]["page"] for doc in output] == [1]

    @pytest.mark.asyncio
    async def test_search_script_score(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search with metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVectorScriptScore(
                embedding_service=AsyncFakeEmbeddings()
            ),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        expected_query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'vector_field') + 1.0",  # noqa: E501
                        "params": {
                            "query_vector": [
                                1.0,
                                1.0,
                                1.0,
                                1.0,
                                1.0,
                                1.0,
                                1.0,
                                1.0,
                                1.0,
                                0.0,
                            ]
                        },
                    },
                }
            }
        }

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == expected_query
            return query_body

        output = await store.search("foo", k=1, custom_query=assert_query)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

    @pytest.mark.asyncio
    async def test_search_script_score_with_filter(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search with metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVectorScriptScore(
                embedding_service=AsyncFakeEmbeddings()
            ),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        metadatas = [{"page": i} for i in range(len(texts))]
        await store.add_texts(texts=texts, metadatas=metadatas)

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            expected_query = {
                "query": {
                    "script_score": {
                        "query": {"bool": {"filter": [{"term": {"metadata.page": 0}}]}},
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'vector_field') + 1.0",  # noqa: E501
                            "params": {
                                "query_vector": [
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    0.0,
                                ]
                            },
                        },
                    }
                }
            }
            assert query_body == expected_query
            return query_body

        output = await store.search(
            "foo",
            k=1,
            custom_query=assert_query,
            filter=[{"term": {"metadata.page": 0}}],
        )
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]
        assert [doc["_source"]["metadata"]["page"] for doc in output] == [0]

    @pytest.mark.asyncio
    async def test_search_script_score_distance_dot_product(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search with metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVectorScriptScore(
                embedding_service=AsyncFakeEmbeddings(),
                distance=DistanceMetric.DOT_PRODUCT,
            ),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == {
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},
                        "script": {
                            "source": """
            double value = dotProduct(params.query_vector, 'vector_field');
            return sigmoid(1, Math.E, -value);
            """,
                            "params": {
                                "query_vector": [
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    1.0,
                                    0.0,
                                ]
                            },
                        },
                    }
                }
            }
            return query_body

        output = await store.search("foo", k=1, custom_query=assert_query)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

    @pytest.mark.asyncio
    async def test_search_knn_with_hybrid_search(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and search with metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(
                embedding_service=AsyncFakeEmbeddings(),
                hybrid=True,
            ),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == {
                "knn": {
                    "field": "vector_field",
                    "filter": [],
                    "k": 1,
                    "num_candidates": 50,
                    "query_vector": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
                },
                "query": {
                    "bool": {
                        "filter": [],
                        "must": [{"match": {"text_field": {"query": "foo"}}}],
                    }
                },
                "rank": {"rrf": {}},
            }
            return query_body

        output = await store.search("foo", k=1, custom_query=assert_query)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

    @pytest.mark.asyncio
    async def test_search_knn_with_hybrid_search_rrf(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end construction and rrf hybrid search with metadata."""
        texts = ["foo", "bar", "baz"]

        def assert_query(
            query_body: dict,
            query: Optional[str],
            expected_rrf: Union[dict, bool],
        ) -> dict:
            cmp_query_body = {
                "knn": {
                    "field": "vector_field",
                    "filter": [],
                    "k": 3,
                    "num_candidates": 50,
                    "query_vector": [
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        1.0,
                        0.0,
                    ],
                },
                "query": {
                    "bool": {
                        "filter": [],
                        "must": [{"match": {"text_field": {"query": "foo"}}}],
                    }
                },
            }

            if isinstance(expected_rrf, dict):
                cmp_query_body["rank"] = {"rrf": expected_rrf}
            elif isinstance(expected_rrf, bool) and expected_rrf is True:
                cmp_query_body["rank"] = {"rrf": {}}

            assert query_body == cmp_query_body

            return query_body

        # 1. check query_body is okay
        rrf_test_cases: List[Union[dict, bool]] = [
            True,
            False,
            {"rank_constant": 1, "window_size": 5},
        ]
        for rrf_test_case in rrf_test_cases:
            store = AsyncVectorStore(
                user_agent="test",
                index_name=index_name,
                retrieval_strategy=DenseVector(
                    embedding_service=AsyncFakeEmbeddings(),
                    hybrid=True,
                    rrf=rrf_test_case,
                ),
                es_client=es_client,
            )
            await store.add_texts(texts)

            ## without fetch_k parameter
            output = await store.search(
                "foo",
                k=3,
                custom_query=partial(assert_query, expected_rrf=rrf_test_case),
            )

        # 2. check query result is okay
        es_output = await store.es_client.search(
            index=index_name,
            query={
                "bool": {
                    "filter": [],
                    "must": [{"match": {"text_field": {"query": "foo"}}}],
                }
            },
            knn={
                "field": "vector_field",
                "filter": [],
                "k": 3,
                "num_candidates": 50,
                "query_vector": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            },
            size=3,
            rank={"rrf": {"rank_constant": 1, "window_size": 5}},
        )

        assert [o["_source"]["text_field"] for o in output] == [
            e["_source"]["text_field"] for e in es_output["hits"]["hits"]
        ]

        # 3. check rrf default option is okay
        store = AsyncVectorStore(
            user_agent="test",
            index_name=f"{index_name}_default",
            retrieval_strategy=DenseVector(
                embedding_service=AsyncFakeEmbeddings(),
                hybrid=True,
            ),
            es_client=es_client,
        )
        await store.add_texts(texts)

        ## with fetch_k parameter
        output = await store.search(
            "foo",
            k=3,
            num_candidates=50,
            custom_query=partial(assert_query, expected_rrf={}),
        )

    @pytest.mark.asyncio
    async def test_search_knn_with_custom_query_fn(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """test that custom query function is called
        with the query string and query body"""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(embedding_service=AsyncFakeEmbeddings()),
            es_client=es_client,
        )

        def my_custom_query(query_body: dict, query: Optional[str]) -> dict:
            assert query == "foo"
            assert query_body == {
                "knn": {
                    "field": "vector_field",
                    "filter": [],
                    "k": 1,
                    "num_candidates": 50,
                    "query_vector": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
                }
            }
            return {"query": {"match": {"text_field": {"query": "bar"}}}}

        """Test end to end construction and search with metadata."""
        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        output = await store.search("foo", k=1, custom_query=my_custom_query)
        assert [doc["_source"]["text_field"] for doc in output] == ["bar"]

    @pytest.mark.asyncio
    async def test_search_with_knn_infer_instack(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """test end to end with knn retrieval strategy and inference in-stack"""

        if not await model_is_deployed(es_client, TRANSFORMER_MODEL_ID):
            pytest.skip(
                f"{TRANSFORMER_MODEL_ID} model not deployed in ML Node skipping test"
            )

        text_field = "text_field"

        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=Semantic(
                model_id="sentence-transformers__all-minilm-l6-v2",
                text_field=text_field,
            ),
            es_client=es_client,
        )

        # setting up the pipeline for inference
        await store.es_client.ingest.put_pipeline(
            id="test_pipeline",
            processors=[
                {
                    "inference": {
                        "model_id": TRANSFORMER_MODEL_ID,
                        "field_map": {"query_field": text_field},
                        "target_field": "vector_query_field",
                    }
                }
            ],
        )

        # creating a new index with the pipeline,
        # not relying on langchain to create the index
        await store.es_client.indices.create(
            index=index_name,
            mappings={
                "properties": {
                    text_field: {"type": "text_field"},
                    "vector_query_field": {
                        "properties": {
                            "predicted_value": {
                                "type": "dense_vector",
                                "dims": 384,
                                "index": True,
                                "similarity": "l2_norm",
                            }
                        }
                    },
                }
            },
            settings={"index": {"default_pipeline": "test_pipeline"}},
        )

        # adding documents to the index
        texts = ["foo", "bar", "baz"]

        for i, text in enumerate(texts):
            await store.es_client.create(
                index=index_name,
                id=str(i),
                document={text_field: text, "metadata": {}},
            )

        await store.es_client.indices.refresh(index=index_name)

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == {
                "knn": {
                    "filter": [],
                    "field": "vector_query_field.predicted_value",
                    "k": 1,
                    "num_candidates": 50,
                    "query_vector_builder": {
                        "text_embedding": {
                            "model_id": TRANSFORMER_MODEL_ID,
                            "model_text": "foo",
                        }
                    },
                }
            }
            return query_body

        output = await store.search("foo", k=1, custom_query=assert_query)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

        output = await store.search("bar", k=1)
        assert [doc["_source"]["text_field"] for doc in output] == ["bar"]

    @pytest.mark.asyncio
    async def test_search_with_sparse_infer_instack(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """test end to end with sparse retrieval strategy and inference in-stack"""

        if not await model_is_deployed(es_client, ELSER_MODEL_ID):
            reason = f"{ELSER_MODEL_ID} model not deployed in ML Node, skipping test"

            pytest.skip(reason)

        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=Semantic(model_id=ELSER_MODEL_ID),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        output = await store.search("foo", k=1)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

    @pytest.mark.asyncio
    async def test_deployed_model_check_fails_semantic(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """test that exceptions are raised if a specified model is not deployed"""
        with pytest.raises(NotFoundError):
            store = AsyncVectorStore(
                user_agent="test",
                index_name=index_name,
                retrieval_strategy=Semantic(model_id="non-existing model ID"),
                es_client=es_client,
            )
            await store.add_texts(["foo", "bar", "baz"])

    @pytest.mark.asyncio
    async def test_search_bm25(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to end using the BM25 retrieval strategy."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=BM25(),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz"]
        await store.add_texts(texts)

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == {
                "query": {
                    "bool": {
                        "must": [{"match": {"text_field": {"query": "foo"}}}],
                        "filter": [],
                    }
                }
            }
            return query_body

        output = await store.search("foo", k=1, custom_query=assert_query)
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]

    @pytest.mark.asyncio
    async def test_search_bm25_with_filter(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test end to using the BM25 retrieval strategy with metadata."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=BM25(),
            es_client=es_client,
        )

        texts = ["foo", "foo", "foo"]
        metadatas = [{"page": i} for i in range(len(texts))]
        await store.add_texts(texts=texts, metadatas=metadatas)

        def assert_query(query_body: dict, query: Optional[str]) -> dict:
            assert query_body == {
                "query": {
                    "bool": {
                        "must": [{"match": {"text_field": {"query": "foo"}}}],
                        "filter": [{"term": {"metadata.page": 1}}],
                    }
                }
            }
            return query_body

        output = await store.search(
            "foo",
            k=3,
            custom_query=assert_query,
            filter=[{"term": {"metadata.page": 1}}],
        )
        assert [doc["_source"]["text_field"] for doc in output] == ["foo"]
        assert [doc["_source"]["metadata"]["page"] for doc in output] == [1]

    @pytest.mark.asyncio
    async def test_delete(self, es_client: AsyncElasticsearch, index_name: str) -> None:
        """Test delete methods from vector store."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVector(embedding_service=AsyncFakeEmbeddings()),
            es_client=es_client,
        )

        texts = ["foo", "bar", "baz", "gni"]
        metadatas = [{"page": i} for i in range(len(texts))]
        ids = await store.add_texts(texts=texts, metadatas=metadatas)

        output = await store.search("foo", k=10)
        assert len(output) == 4

        await store.delete(ids[1:3])
        output = await store.search("foo", k=10)
        assert len(output) == 2

        await store.delete(["not-existing"])
        output = await store.search("foo", k=10)
        assert len(output) == 2

        await store.delete([ids[0]])
        output = await store.search("foo", k=10)
        assert len(output) == 1

        await store.delete([ids[3]])
        output = await store.search("gni", k=10)
        assert len(output) == 0

    @pytest.mark.asyncio
    async def test_indexing_exception_error(
        self,
        es_client: AsyncElasticsearch,
        index_name: str,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Test bulk exception logging is giving better hints."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=BM25(),
            es_client=es_client,
        )

        await store.es_client.indices.create(
            index=index_name,
            mappings={"properties": {}},
            settings={"index": {"default_pipeline": "not-existing-pipeline"}},
        )

        texts = ["foo"]

        with pytest.raises(BulkIndexError):
            await store.add_texts(texts)

        error_reason = "pipeline with id [not-existing-pipeline] does not exist"
        log_message = f"First error reason: {error_reason}"

        assert log_message in caplog.text

    @pytest.mark.asyncio
    async def test_user_agent(
        self, requests_saving_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test to make sure the user-agent is set correctly."""
        user_agent = "this is THE user_agent!"
        store = AsyncVectorStore(
            user_agent=user_agent,
            index_name=index_name,
            retrieval_strategy=BM25(),
            es_client=requests_saving_client,
        )

        assert store.es_client._headers["User-Agent"] == user_agent

        texts = ["foo", "bob", "baz"]
        await store.add_texts(texts)

        transport = cast(AsyncRequestSavingTransport, store.es_client.transport)

        for request in transport.requests:
            assert request["headers"]["User-Agent"] == user_agent

    @pytest.mark.asyncio
    async def test_bulk_args(
        self, requests_saving_client: Any, index_name: str
    ) -> None:
        """Test to make sure the bulk arguments work as expected."""
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=BM25(),
            es_client=requests_saving_client,
        )

        texts = ["foo", "bob", "baz"]
        await store.add_texts(texts, bulk_kwargs={"chunk_size": 1})

        # 1 for index exist, 1 for index create, 3 to index docs
        assert len(store.es_client.transport.requests) == 5  # type: ignore

    @pytest.mark.asyncio
    async def test_max_marginal_relevance_search(
        self, es_client: AsyncElasticsearch, index_name: str
    ) -> None:
        """Test max marginal relevance search."""
        texts = ["foo", "bar", "baz"]
        vector_field = "vector_field"
        text_field = "text_field"
        embedding_service = AsyncConsistentFakeEmbeddings()
        store = AsyncVectorStore(
            user_agent="test",
            index_name=index_name,
            retrieval_strategy=DenseVectorScriptScore(
                embedding_service=embedding_service
            ),
            vector_field=vector_field,
            text_field=text_field,
            es_client=es_client,
        )
        await store.add_texts(texts)

        mmr_output = await store.max_marginal_relevance_search(
            embedding_service,
            texts[0],
            vector_field=vector_field,
            k=3,
            num_candidates=3,
        )
        sim_output = await store.search(texts[0], k=3)
        assert mmr_output == sim_output

        mmr_output = await store.max_marginal_relevance_search(
            embedding_service,
            texts[0],
            vector_field=vector_field,
            k=2,
            num_candidates=3,
        )
        assert len(mmr_output) == 2
        assert mmr_output[0]["_source"][text_field] == texts[0]
        assert mmr_output[1]["_source"][text_field] == texts[1]

        mmr_output = await store.max_marginal_relevance_search(
            embedding_service,
            texts[0],
            vector_field=vector_field,
            k=2,
            num_candidates=3,
            lambda_mult=0.1,  # more diversity
        )
        assert len(mmr_output) == 2
        assert mmr_output[0]["_source"][text_field] == texts[0]
        assert mmr_output[1]["_source"][text_field] == texts[2]

        # if fetch_k < k, then the output will be less than k
        mmr_output = await store.max_marginal_relevance_search(
            embedding_service,
            texts[0],
            vector_field=vector_field,
            k=3,
            num_candidates=2,
        )
        assert len(mmr_output) == 2

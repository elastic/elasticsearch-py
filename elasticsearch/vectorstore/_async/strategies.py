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

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union, cast

from elasticsearch import AsyncElasticsearch
from elasticsearch.vectorstore._async._utils import model_must_be_deployed
from elasticsearch.vectorstore._utils import DistanceMetric


class AsyncRetrievalStrategy(ABC):
    @abstractmethod
    def es_query(
        self,
        query: Optional[str],
        query_vector: Optional[List[float]],
        text_field: str,
        vector_field: str,
        k: int,
        num_candidates: int,
        filter: List[Dict[str, Any]] = [],
    ) -> Dict[str, Any]:
        """
        Returns the Elasticsearch query body for the given parameters.
        The store will execute the query.

        Args:
            query: The text query. Can be None if query_vector is given.
            k: The total number of results to retrieve.
            num_candidates: The number of results to fetch initially in knn search.
            filter: List of filter clauses to apply to the query.
            query_vector: The query vector. Can be None if a query string is given.

        Returns:
            Dict: The Elasticsearch query body.
        """

    @abstractmethod
    def es_mappings_settings(
        self,
        text_field: str,
        vector_field: str,
        num_dimensions: Optional[int],
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Create the required index and do necessary preliminary work, like
        creating inference pipelines or checking if a required model was deployed.

        Args:
            client: Elasticsearch client connection.
            index_name: The name of the Elasticsearch index to create.
            metadata_mapping: Flat dictionary with field and field type pairs that
                describe the schema of the metadata.
        """

    async def before_index_creation(
        self, client: AsyncElasticsearch, text_field: str, vector_field: str
    ) -> None:
        """
        Executes before the index is created. Used for setting up
        any required Elasticsearch resources like a pipeline.

        Args:
            client: The Elasticsearch client.
            text_field: The field containing the text data in the index.
            vector_field: The field containing the vector representations in the index.
        """
        pass

    def needs_inference(self) -> bool:
        """
        TODO
        """
        return False


class AsyncSparseVector(AsyncRetrievalStrategy):
    """Sparse retrieval strategy using the `text_expansion` processor."""

    def __init__(self, model_id: str = ".elser_model_2"):
        self.model_id = model_id
        self._tokens_field = "tokens"
        self._pipeline_name = f"{self.model_id}_sparse_embedding"

    def es_query(
        self,
        query: Optional[str],
        query_vector: Optional[List[float]],
        text_field: str,
        vector_field: str,
        k: int,
        num_candidates: int,
        filter: List[Dict[str, Any]] = [],
    ) -> Dict[str, Any]:
        if query_vector:
            raise ValueError(
                "Cannot do sparse retrieval with a query_vector. "
                "Inference is currently always applied in Elasticsearch."
            )
        if query is None:
            raise ValueError("please specify a query string")

        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "text_expansion": {
                                f"{vector_field}.{self._tokens_field}": {
                                    "model_id": self.model_id,
                                    "model_text": query,
                                }
                            }
                        }
                    ],
                    "filter": filter,
                }
            },
            "size": k,
        }

    def es_mappings_settings(
        self,
        text_field: str,
        vector_field: str,
        num_dimensions: Optional[int],
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        mappings: Dict[str, Any] = {
            "properties": {
                vector_field: {
                    "properties": {self._tokens_field: {"type": "rank_features"}}
                }
            }
        }
        settings = {"default_pipeline": self._pipeline_name}

        return mappings, settings

    async def before_index_creation(
        self, client: AsyncElasticsearch, text_field: str, vector_field: str
    ) -> None:
        if self.model_id:
            await model_must_be_deployed(client, self.model_id)

            # Create a pipeline for the model
            await client.ingest.put_pipeline(
                id=self._pipeline_name,
                description="Embedding pipeline for Python VectorStore",
                processors=[
                    {
                        "inference": {
                            "model_id": self.model_id,
                            "target_field": vector_field,
                            "field_map": {text_field: "text_field"},
                            "inference_config": {
                                "text_expansion": {"results_field": self._tokens_field}
                            },
                        }
                    }
                ],
            )


class AsyncDenseVector(AsyncRetrievalStrategy):
    """K-nearest-neighbors retrieval."""

    def __init__(
        self,
        distance: DistanceMetric = DistanceMetric.COSINE,
        model_id: Optional[str] = None,
        hybrid: bool = False,
        rrf: Union[bool, Dict[str, Any]] = True,
        text_field: Optional[str] = "text_field",
    ):
        if hybrid and not text_field:
            raise ValueError(
                "to enable hybrid you have to specify a text_field (for BM25 matching)"
            )

        self.distance = distance
        self.model_id = model_id
        self.hybrid = hybrid
        self.rrf = rrf
        self.text_field = text_field

    def es_query(
        self,
        query: Optional[str],
        query_vector: Optional[List[float]],
        text_field: str,
        vector_field: str,
        k: int,
        num_candidates: int,
        filter: List[Dict[str, Any]] = [],
    ) -> Dict[str, Any]:
        knn = {
            "filter": filter,
            "field": vector_field,
            "k": k,
            "num_candidates": num_candidates,
        }

        if query_vector:
            knn["query_vector"] = query_vector
        else:
            # Inference in Elasticsearch. When initializing we make sure to always have
            # a model_id if don't have an embedding_service.
            knn["query_vector_builder"] = {
                "text_embedding": {
                    "model_id": self.model_id,
                    "model_text": query,
                }
            }

        if self.hybrid:
            return self._hybrid(query=cast(str, query), knn=knn, filter=filter)

        return {"knn": knn}

    def es_mappings_settings(
        self,
        text_field: str,
        vector_field: str,
        num_dimensions: Optional[int],
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        if self.distance is DistanceMetric.COSINE:
            similarityAlgo = "cosine"
        elif self.distance is DistanceMetric.EUCLIDEAN_DISTANCE:
            similarityAlgo = "l2_norm"
        elif self.distance is DistanceMetric.DOT_PRODUCT:
            similarityAlgo = "dot_product"
        elif self.distance is DistanceMetric.MAX_INNER_PRODUCT:
            similarityAlgo = "max_inner_product"
        else:
            raise ValueError(f"Similarity {self.distance} not supported.")

        mappings: Dict[str, Any] = {
            "properties": {
                vector_field: {
                    "type": "dense_vector",
                    "dims": num_dimensions,
                    "index": True,
                    "similarity": similarityAlgo,
                },
            }
        }

        return mappings, {}

    async def before_index_creation(
        self, client: AsyncElasticsearch, text_field: str, vector_field: str
    ) -> None:
        if self.model_id:
            await model_must_be_deployed(client, self.model_id)

    def _hybrid(
        self, query: str, knn: Dict[str, Any], filter: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        # Add a query to the knn query.
        # RRF is used to even the score from the knn query and text query
        # RRF has two optional parameters: {'rank_constant':int, 'window_size':int}
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html
        query_body = {
            "knn": knn,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                self.text_field: {
                                    "query": query,
                                }
                            }
                        }
                    ],
                    "filter": filter,
                }
            },
        }

        if isinstance(self.rrf, Dict):
            query_body["rank"] = {"rrf": self.rrf}
        elif isinstance(self.rrf, bool) and self.rrf is True:
            query_body["rank"] = {"rrf": {}}

        return query_body

    def needs_inference(self) -> bool:
        return not self.model_id


class AsyncDenseVectorScriptScore(AsyncRetrievalStrategy):
    """Exact nearest neighbors retrieval using the `script_score` query."""

    def __init__(self, distance: DistanceMetric = DistanceMetric.COSINE) -> None:
        self.distance = distance

    def es_query(
        self,
        query: Optional[str],
        query_vector: Optional[List[float]],
        text_field: str,
        vector_field: str,
        k: int,
        num_candidates: int,
        filter: List[Dict[str, Any]] = [],
    ) -> Dict[str, Any]:
        if not query_vector:
            raise ValueError("specify a query_vector")

        if self.distance is DistanceMetric.COSINE:
            similarityAlgo = (
                f"cosineSimilarity(params.query_vector, '{vector_field}') + 1.0"
            )
        elif self.distance is DistanceMetric.EUCLIDEAN_DISTANCE:
            similarityAlgo = f"1 / (1 + l2norm(params.query_vector, '{vector_field}'))"
        elif self.distance is DistanceMetric.DOT_PRODUCT:
            similarityAlgo = f"""
            double value = dotProduct(params.query_vector, '{vector_field}');
            return sigmoid(1, Math.E, -value);
            """
        elif self.distance is DistanceMetric.MAX_INNER_PRODUCT:
            similarityAlgo = f"""
            double value = dotProduct(params.query_vector, '{vector_field}');
            if (dotProduct < 0) {{
                return 1 / (1 + -1 * dotProduct);
            }}
            return dotProduct + 1;
            """
        else:
            raise ValueError(f"Similarity {self.distance} not supported.")

        queryBool: Dict[str, Any] = {"match_all": {}}
        if filter:
            queryBool = {"bool": {"filter": filter}}

        return {
            "query": {
                "script_score": {
                    "query": queryBool,
                    "script": {
                        "source": similarityAlgo,
                        "params": {"query_vector": query_vector},
                    },
                },
            }
        }

    def es_mappings_settings(
        self,
        text_field: str,
        vector_field: str,
        num_dimensions: Optional[int],
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        mappings = {
            "properties": {
                vector_field: {
                    "type": "dense_vector",
                    "dims": num_dimensions,
                    "index": False,
                }
            }
        }

        return mappings, {}

    def needs_inference(self) -> bool:
        return True


class AsyncBM25(AsyncRetrievalStrategy):
    def __init__(
        self,
        k1: Optional[float] = None,
        b: Optional[float] = None,
    ):
        self.k1 = k1
        self.b = b

    def es_query(
        self,
        query: Optional[str],
        query_vector: Optional[List[float]],
        text_field: str,
        vector_field: str,
        k: int,
        num_candidates: int,
        filter: List[Dict[str, Any]] = [],
    ) -> Dict[str, Any]:
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                text_field: {
                                    "query": query,
                                }
                            },
                        },
                    ],
                    "filter": filter,
                },
            },
        }

    def es_mappings_settings(
        self,
        text_field: str,
        vector_field: str,
        num_dimensions: Optional[int],
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        similarity_name = "custom_bm25"

        mappings: Dict[str, Any] = {
            "properties": {
                text_field: {
                    "type": "text",
                    "similarity": similarity_name,
                },
            },
        }

        bm25: Dict[str, Any] = {
            "type": "BM25",
        }
        if self.k1 is not None:
            bm25["k1"] = self.k1
        if self.b is not None:
            bm25["b"] = self.b
        settings = {
            "similarity": {
                similarity_name: bm25,
            }
        }

        return mappings, settings

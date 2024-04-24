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
from typing import List, Optional

from elasticsearch import Elasticsearch


class EmbeddingService(ABC):
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents.

        Args:
            texts: A list of document strings to generate embeddings for.

        Returns:
            A list of embeddings, one for each document in the input.
        """

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generate an embedding for a single query text.

        Args:
            text: The query text to generate an embedding for.

        Returns:
            The embedding for the input query text.
        """


class ElasticsearchEmbeddings(EmbeddingService):
    """Elasticsearch as a service for embedding model inference.

    You need to have an embedding model downloaded and deployed in Elasticsearch:
    - https://www.elastic.co/guide/en/elasticsearch/reference/current/infer-trained-model.html
    - https://www.elastic.co/guide/en/machine-learning/current/ml-nlp-deploy-models.html
    """  # noqa: E501

    def __init__(
        self,
        es_client: Elasticsearch,
        user_agent: str,
        model_id: str,
        input_field: str = "text_field",
        num_dimensions: Optional[int] = None,
    ):
        """
        Args:
            agent_header: user agent header specific to the 3rd party integration.
                Used for usage tracking in Elastic Cloud.
            model_id: The model_id of the model deployed in the Elasticsearch cluster.
            input_field: The name of the key for the input text field in the
                document. Defaults to 'text_field'.
            num_dimensions: The number of embedding dimensions. If None, then dimensions
                will be infer from an example inference call.
            es_client: Elasticsearch client connection. Alternatively specify the
                Elasticsearch connection with the other es_* parameters.
        """
        # Add integration-specific usage header for tracking usage in Elastic Cloud.
        # client.options preserces existing (non-user-agent) headers.
        es_client = es_client.options(headers={"User-Agent": user_agent})

        self.client = es_client.ml
        self.model_id = model_id
        self.input_field = input_field
        self._num_dimensions = num_dimensions

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        result = self._embedding_func(texts)
        return result

    def embed_query(self, text: str) -> List[float]:
        result = self._embedding_func([text])
        return result[0]

    def _embedding_func(self, texts: List[str]) -> List[List[float]]:
        response = self.client.infer_trained_model(
            model_id=self.model_id, docs=[{self.input_field: text} for text in texts]
        )
        return [doc["predicted_value"] for doc in response["inference_results"]]

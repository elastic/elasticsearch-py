import asyncio
from abc import ABC, abstractmethod
from typing import List, Optional

import nest_asyncio  # type: ignore
from elasticsearch import AsyncElasticsearch

from elasticsearch.store._utilities import create_elasticsearch_client


class EmbeddingService(ABC):
    @abstractmethod
    async def embed_documents_async(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents.

        Args:
            texts: A list of document strings to generate embeddings for.

        Returns:
            A list of embeddings, one for each document in the input.
        """

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents.

        Args:
            texts: A list of document strings to generate embeddings for.

        Returns:
            A list of embeddings, one for each document in the input.
        """

    @abstractmethod
    async def embed_query_async(self, query: str) -> List[float]:
        """Generate an embedding for a single query text.

        Args:
            text: The query text to generate an embedding for.

        Returns:
            The embedding for the input query text.
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
        agent_header: str,
        model_id: str,
        input_field: str = "text_field",
        num_dimensions: Optional[int] = None,
        # Connection params
        es_client: Optional[AsyncElasticsearch] = None,
        es_url: Optional[str] = None,
        es_cloud_id: Optional[str] = None,
        es_api_key: Optional[str] = None,
        es_user: Optional[str] = None,
        es_password: Optional[str] = None,
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
        nest_asyncio.apply()

        client = create_elasticsearch_client(
            agent_header=agent_header,
            client=es_client,
            url=es_url,
            cloud_id=es_cloud_id,
            api_key=es_api_key,
            username=es_user,
            password=es_password,
        )

        self.client = client.ml
        self.model_id = model_id
        self.input_field = input_field
        self._num_dimensions = num_dimensions

    async def embed_documents_async(self, texts: List[str]) -> List[List[float]]:
        result = await self._embedding_func_async(texts)
        return result

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return asyncio.get_event_loop().run_until_complete(
            self.embed_documents_async(texts)
        )

    async def embed_query_async(self, text: str) -> List[float]:
        result = await self._embedding_func_async([text])
        return result[0]

    def embed_query(self, query: str) -> List[float]:
        return asyncio.get_event_loop().run_until_complete(
            self.embed_query_async(query)
        )

    async def _embedding_func_async(self, texts: List[str]) -> List[List[float]]:
        response = await self.client.infer_trained_model(
            model_id=self.model_id, docs=[{self.input_field: text} for text in texts]
        )

        embeddings = [doc["predicted_value"] for doc in response["inference_results"]]
        return embeddings

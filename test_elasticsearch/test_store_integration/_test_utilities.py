import asyncio
import os
from typing import Any, Dict, List, Optional

import nest_asyncio  # type: ignore
from elastic_transport import AsyncTransport
from elasticsearch import AsyncElasticsearch

from elasticsearch.store._utilities import model_is_deployed_async
from elasticsearch.store.embedding_service import EmbeddingService


class FakeEmbeddings(EmbeddingService):
    """Fake embeddings functionality for testing."""

    def __init__(self, dimensionality: int = 10) -> None:
        nest_asyncio.apply()

        self.dimensionality = dimensionality

    def num_dimensions(self) -> int:
        return self.dimensionality

    async def embed_documents_async(self, texts: List[str]) -> List[List[float]]:
        """Return simple embeddings. Embeddings encode each text as its index."""
        return [
            [float(1.0)] * (self.dimensionality - 1) + [float(i)]
            for i in range(len(texts))
        ]

    async def embed_query_async(self, text: str) -> List[float]:
        """Return constant query embeddings.
        Embeddings are identical to embed_documents(texts)[0].
        Distance to each text will be that text's index,
        as it was passed to embed_documents.
        """
        return [float(1.0)] * (self.dimensionality - 1) + [float(0.0)]

    def embed_query(self, text: str) -> List[float]:
        return asyncio.get_event_loop().run_until_complete(self.embed_query_async(text))

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return asyncio.get_event_loop().run_until_complete(
            self.embed_documents_async(texts)
        )


class ConsistentFakeEmbeddings(FakeEmbeddings):
    """Fake embeddings which remember all the texts seen so far to return consistent
    vectors for the same texts."""

    def __init__(self, dimensionality: int = 10) -> None:
        self.known_texts: List[str] = []
        self.dimensionality = dimensionality

    def num_dimensions(self) -> int:
        return self.dimensionality

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return consistent embeddings for each text seen so far."""
        out_vectors = []
        for text in texts:
            if text not in self.known_texts:
                self.known_texts.append(text)
            vector = [float(1.0)] * (self.dimensionality - 1) + [
                float(self.known_texts.index(text))
            ]
            out_vectors.append(vector)
        return out_vectors

    def embed_query(self, text: str) -> List[float]:
        """Return consistent embeddings for the text, if seen before, or a constant
        one if the text is unknown."""
        return self.embed_documents([text])[0]


class RequestSavingTransport(AsyncTransport):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.requests: List[Dict] = []

    async def perform_request(self, *args, **kwargs):  # type: ignore
        self.requests.append(kwargs)
        return await super().perform_request(*args, **kwargs)


def create_es_client(
    es_params: Optional[Dict[str, str]] = None, es_kwargs: Dict = {}
) -> AsyncElasticsearch:
    if es_params is None:
        es_params = read_env()
    if not es_kwargs:
        es_kwargs = {}

    if "es_cloud_id" in es_params:
        return AsyncElasticsearch(
            cloud_id=es_params["es_cloud_id"],
            api_key=es_params["es_api_key"],
            **es_kwargs,
        )
    return AsyncElasticsearch(hosts=[es_params["es_url"]], **es_kwargs)


def create_requests_saving_client() -> AsyncElasticsearch:
    return create_es_client(es_kwargs={"transport_class": RequestSavingTransport})


async def clear_test_indices(client: AsyncElasticsearch) -> None:
    response = await client.indices.get(index="_all")
    index_names = response.keys()
    for index_name in index_names:
        if index_name.startswith("test_"):
            await client.indices.delete(index=index_name)
    await client.indices.refresh(index="_all")


def model_is_deployed(es_client: AsyncElasticsearch, model_id: str) -> bool:
    return asyncio.get_event_loop().run_until_complete(
        model_is_deployed_async(es_client, model_id)
    )


def read_env() -> Dict:
    url = os.environ.get("ES_URL", "http://localhost:9200")
    cloud_id = os.environ.get("ES_CLOUD_ID")
    api_key = os.environ.get("ES_API_KEY")

    if cloud_id:
        return {"es_cloud_id": cloud_id, "es_api_key": api_key}
    return {"es_url": url}

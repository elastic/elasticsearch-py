import os
from typing import Any, AsyncIterator, Dict, List, Optional

from elastic_transport import AsyncTransport

from elasticsearch import AsyncElasticsearch
from elasticsearch.vectorstore._async.embedding_service import AsyncEmbeddingService


class AsyncFakeEmbeddings(AsyncEmbeddingService):
    """Fake embeddings functionality for testing."""

    def __init__(self, dimensionality: int = 10) -> None:
        self.dimensionality = dimensionality

    def num_dimensions(self) -> int:
        return self.dimensionality

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return simple embeddings. Embeddings encode each text as its index."""
        return [
            [float(1.0)] * (self.dimensionality - 1) + [float(i)]
            for i in range(len(texts))
        ]

    async def embed_query(self, text: str) -> List[float]:
        """Return constant query embeddings.
        Embeddings are identical to embed_documents(texts)[0].
        Distance to each text will be that text's index,
        as it was passed to embed_documents.
        """
        return [float(1.0)] * (self.dimensionality - 1) + [float(0.0)]


class AsyncConsistentFakeEmbeddings(AsyncFakeEmbeddings):
    """Fake embeddings which remember all the texts seen so far to return consistent
    vectors for the same texts."""

    def __init__(self, dimensionality: int = 10) -> None:
        self.known_texts: List[str] = []
        self.dimensionality = dimensionality

    def num_dimensions(self) -> int:
        return self.dimensionality

    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
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

    async def embed_query(self, text: str) -> List[float]:
        """Return consistent embeddings for the text, if seen before, or a constant
        one if the text is unknown."""
        result = await self.embed_documents([text])
        return result[0]


class AsyncRequestSavingTransport(AsyncTransport):
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
    return create_es_client(es_kwargs={"transport_class": AsyncRequestSavingTransport})


async def es_client_fixture() -> AsyncIterator[AsyncElasticsearch]:
    params = read_env()
    client = create_es_client(params)

    yield client

    # clear indices
    await clear_test_indices(client)

    # clear all test pipelines
    try:
        response = await client.ingest.get_pipeline(id="test_*,*_sparse_embedding")

        for pipeline_id, _ in response.items():
            try:
                await client.ingest.delete_pipeline(id=pipeline_id)
                print(f"Deleted pipeline: {pipeline_id}")  # noqa: T201
            except Exception as e:
                print(f"Pipeline error: {e}")  # noqa: T201

    except Exception:
        pass
    finally:
        await client.close()


async def clear_test_indices(client: AsyncElasticsearch) -> None:
    response = await client.indices.get(index="_all")
    index_names = response.keys()
    for index_name in index_names:
        if index_name.startswith("test_"):
            await client.indices.delete(index=index_name)
    await client.indices.refresh(index="_all")


def read_env() -> Dict:
    url = os.environ.get("ES_URL", "http://localhost:9200")
    cloud_id = os.environ.get("ES_CLOUD_ID")
    api_key = os.environ.get("ES_API_KEY")

    if cloud_id:
        return {"es_cloud_id": cloud_id, "es_api_key": api_key}
    return {"es_url": url}

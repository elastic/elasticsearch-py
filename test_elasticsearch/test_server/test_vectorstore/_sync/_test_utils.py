import os
from typing import Any, Dict, Iterator, List, Optional

from elastic_transport import Transport

from elasticsearch import Elasticsearch
from elasticsearch.vectorstore._sync.embedding_service import EmbeddingService


class FakeEmbeddings(EmbeddingService):
    """Fake embeddings functionality for testing."""

    def __init__(self, dimensionality: int = 10) -> None:
        self.dimensionality = dimensionality

    def num_dimensions(self) -> int:
        return self.dimensionality

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Return simple embeddings. Embeddings encode each text as its index."""
        return [
            [float(1.0)] * (self.dimensionality - 1) + [float(i)]
            for i in range(len(texts))
        ]

    def embed_query(self, text: str) -> List[float]:
        """Return constant query embeddings.
        Embeddings are identical to embed_documents(texts)[0].
        Distance to each text will be that text's index,
        as it was passed to embed_documents.
        """
        return [float(1.0)] * (self.dimensionality - 1) + [float(0.0)]


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
        result = self.embed_documents([text])
        return result[0]


class RequestSavingTransport(Transport):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.requests: List[Dict] = []

    def perform_request(self, *args, **kwargs):  # type: ignore
        self.requests.append(kwargs)
        return super().perform_request(*args, **kwargs)


def create_es_client(
    es_params: Optional[Dict[str, str]] = None, es_kwargs: Dict = {}
) -> Elasticsearch:
    if es_params is None:
        es_params = read_env()
    if not es_kwargs:
        es_kwargs = {}

    if "es_cloud_id" in es_params:
        return Elasticsearch(
            cloud_id=es_params["es_cloud_id"],
            api_key=es_params["es_api_key"],
            **es_kwargs,
        )
    return Elasticsearch(hosts=[es_params["es_url"]], **es_kwargs)


def create_requests_saving_client() -> Elasticsearch:
    return create_es_client(es_kwargs={"transport_class": RequestSavingTransport})


def es_client_fixture() -> Iterator[Elasticsearch]:
    params = read_env()
    client = create_es_client(params)

    yield client

    # clear indices
    clear_test_indices(client)

    # clear all test pipelines
    try:
        response = client.ingest.get_pipeline(id="test_*,*_sparse_embedding")

        for pipeline_id, _ in response.items():
            try:
                client.ingest.delete_pipeline(id=pipeline_id)
                print(f"Deleted pipeline: {pipeline_id}")  # noqa: T201
            except Exception as e:
                print(f"Pipeline error: {e}")  # noqa: T201

    except Exception:
        pass
    finally:
        client.close()


def clear_test_indices(client: Elasticsearch) -> None:
    response = client.indices.get(index="_all")
    index_names = response.keys()
    for index_name in index_names:
        if index_name.startswith("test_"):
            client.indices.delete(index=index_name)
    client.indices.refresh(index="_all")


def read_env() -> Dict:
    url = os.environ.get("ES_URL", "http://localhost:9200")
    cloud_id = os.environ.get("ES_CLOUD_ID")
    api_key = os.environ.get("ES_API_KEY")

    if cloud_id:
        return {"es_cloud_id": cloud_id, "es_api_key": api_key}
    return {"es_url": url}

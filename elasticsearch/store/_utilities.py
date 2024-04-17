from typing import Any, Dict, List, Optional, Union

import numpy as np
from elasticsearch import (
    AsyncElasticsearch,
    BadRequestError,
    ConflictError,
    NotFoundError,
)

Matrix = Union[List[List[float]], List[np.ndarray], np.ndarray]


def create_elasticsearch_client(
    agent_header: str,
    client: Optional[AsyncElasticsearch] = None,
    url: Optional[str] = None,
    cloud_id: Optional[str] = None,
    api_key: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    client_params: Optional[Dict[str, Any]] = None,
) -> AsyncElasticsearch:
    if not client:
        if url and cloud_id:
            raise ValueError(
                "Both es_url and cloud_id are defined. Please provide only one."
            )

        connection_params: Dict[str, Any] = {}

        if url:
            connection_params["hosts"] = [url]
        elif cloud_id:
            connection_params["cloud_id"] = cloud_id
        else:
            raise ValueError("Please provide either elasticsearch_url or cloud_id.")

        if api_key:
            connection_params["api_key"] = api_key
        elif username and password:
            connection_params["basic_auth"] = (username, password)

        if client_params is not None:
            connection_params.update(client_params)

        client = AsyncElasticsearch(**connection_params)

    if not isinstance(client, AsyncElasticsearch):
        raise TypeError("Elasticsearch client must be AsyncElasticsearch client")

    # Add integration-specific usage header for tracking usage in Elastic Cloud.
    # client.options preserces existing (non-user-agent) headers.
    client = client.options(headers={"User-Agent": agent_header})

    return client


async def model_must_be_deployed_async(
    client: AsyncElasticsearch, model_id: str
) -> None:
    try:
        dummy = {"x": "y"}
        await client.ml.infer_trained_model(model_id=model_id, docs=[dummy])
    except NotFoundError as err:
        raise err
    except ConflictError as err:
        raise NotFoundError(
            f"model '{model_id}' not found, please deploy it first",
            meta=err.meta,
            body=err.body,
        ) from err
    except BadRequestError:
        # This error is expected because we do not know the expected document
        # shape and just use a dummy doc above.
        pass

    return None


async def model_is_deployed_async(es_client: AsyncElasticsearch, model_id: str) -> bool:
    try:
        await model_must_be_deployed_async(es_client, model_id)
        return True
    except NotFoundError:
        return False


def maximal_marginal_relevance(
    query_embedding: list,
    embedding_list: list,
    lambda_mult: float = 0.5,
    k: int = 4,
) -> List[int]:
    """Calculate maximal marginal relevance."""
    query_embedding_arr = np.array(query_embedding)

    if min(k, len(embedding_list)) <= 0:
        return []
    if query_embedding_arr.ndim == 1:
        query_embedding_arr = np.expand_dims(query_embedding_arr, axis=0)
    similarity_to_query = _cosine_similarity(query_embedding_arr, embedding_list)[0]
    most_similar = int(np.argmax(similarity_to_query))
    idxs = [most_similar]
    selected = np.array([embedding_list[most_similar]])
    while len(idxs) < min(k, len(embedding_list)):
        best_score = -np.inf
        idx_to_add = -1
        similarity_to_selected = _cosine_similarity(embedding_list, selected)
        for i, query_score in enumerate(similarity_to_query):
            if i in idxs:
                continue
            redundant_score = max(similarity_to_selected[i])
            equation_score = (
                lambda_mult * query_score - (1 - lambda_mult) * redundant_score
            )
            if equation_score > best_score:
                best_score = equation_score
                idx_to_add = i
        idxs.append(idx_to_add)
        selected = np.append(selected, [embedding_list[idx_to_add]], axis=0)
    return idxs


def _cosine_similarity(X: Matrix, Y: Matrix) -> np.ndarray:
    """Row-wise cosine similarity between two equal-width matrices."""
    if len(X) == 0 or len(Y) == 0:
        return np.array([])

    X = np.array(X)
    Y = np.array(Y)
    if X.shape[1] != Y.shape[1]:
        raise ValueError(
            f"Number of columns in X and Y must be the same. X has shape {X.shape} "
            f"and Y has shape {Y.shape}."
        )
    try:
        import simsimd as simd  # type: ignore

        X = np.array(X, dtype=np.float32)
        Y = np.array(Y, dtype=np.float32)
        Z = 1 - simd.cdist(X, Y, metric="cosine")
        if isinstance(Z, float):
            return np.array([Z])
        return np.array(Z)
    except ImportError:
        X_norm = np.linalg.norm(X, axis=1)
        Y_norm = np.linalg.norm(Y, axis=1)
        # Ignore divide by zero errors run time warnings as those are handled below.
        with np.errstate(divide="ignore", invalid="ignore"):
            similarity = np.dot(X, Y.T) / np.outer(X_norm, Y_norm)
        similarity[np.isnan(similarity) | np.isinf(similarity)] = 0.0
        return similarity

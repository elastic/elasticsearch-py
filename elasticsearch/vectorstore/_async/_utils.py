from elasticsearch import (
    AsyncElasticsearch,
    BadRequestError,
    ConflictError,
    NotFoundError,
)


async def async_model_must_be_deployed(
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


async def async_model_is_deployed(es_client: AsyncElasticsearch, model_id: str) -> bool:
    try:
        await async_model_must_be_deployed(es_client, model_id)
        return True
    except NotFoundError:
        return False

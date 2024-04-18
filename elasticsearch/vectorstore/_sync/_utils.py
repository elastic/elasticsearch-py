from elasticsearch import BadRequestError, ConflictError, Elasticsearch, NotFoundError


def model_must_be_deployed(client: Elasticsearch, model_id: str) -> None:
    try:
        dummy = {"x": "y"}
        client.ml.infer_trained_model(model_id=model_id, docs=[dummy])
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


def model_is_deployed(es_client: Elasticsearch, model_id: str) -> bool:
    try:
        model_must_be_deployed(es_client, model_id)
        return True
    except NotFoundError:
        return False

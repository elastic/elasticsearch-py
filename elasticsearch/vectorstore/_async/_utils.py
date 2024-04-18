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

from elasticsearch import (
    AsyncElasticsearch,
    BadRequestError,
    ConflictError,
    NotFoundError,
)


async def model_must_be_deployed(client: AsyncElasticsearch, model_id: str) -> None:
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


async def model_is_deployed(es_client: AsyncElasticsearch, model_id: str) -> bool:
    try:
        await model_must_be_deployed(es_client, model_id)
        return True
    except NotFoundError:
        return False

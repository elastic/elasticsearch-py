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

import typing as t

from elastic_transport import ObjectApiResponse

from ._base import NamespacedClient
from .utils import (
    SKIP_IN_PATH,
    Stability,
    _quote,
    _rewrite_parameters,
    _stability_warning,
)


class InferenceClient(NamespacedClient):

    @_rewrite_parameters()
    @_stability_warning(Stability.EXPERIMENTAL)
    def delete(
        self,
        *,
        inference_id: str,
        task_type: t.Optional[
            t.Union[
                str,
                t.Literal["completion", "rerank", "sparse_embedding", "text_embedding"],
            ]
        ] = None,
        dry_run: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        force: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Delete an inference endpoint

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/delete-inference-api.html>`_

        :param inference_id: The inference Id
        :param task_type: The task type
        :param dry_run: When true, the endpoint is not deleted, and a list of ingest
            processors which reference this endpoint is returned
        :param force: When true, the inference endpoint is forcefully deleted even if
            it is still being used by ingest processors or semantic text fields
        """
        if inference_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'inference_id'")
        __path_parts: t.Dict[str, str]
        if task_type not in SKIP_IN_PATH and inference_id not in SKIP_IN_PATH:
            __path_parts = {
                "task_type": _quote(task_type),
                "inference_id": _quote(inference_id),
            }
            __path = f'/_inference/{__path_parts["task_type"]}/{__path_parts["inference_id"]}'
        elif inference_id not in SKIP_IN_PATH:
            __path_parts = {"inference_id": _quote(inference_id)}
            __path = f'/_inference/{__path_parts["inference_id"]}'
        else:
            raise ValueError("Couldn't find a path for the given parameters")
        __query: t.Dict[str, t.Any] = {}
        if dry_run is not None:
            __query["dry_run"] = dry_run
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if force is not None:
            __query["force"] = force
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="inference.delete",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_stability_warning(Stability.EXPERIMENTAL)
    def get(
        self,
        *,
        task_type: t.Optional[
            t.Union[
                str,
                t.Literal["completion", "rerank", "sparse_embedding", "text_embedding"],
            ]
        ] = None,
        inference_id: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Get an inference endpoint

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/get-inference-api.html>`_

        :param task_type: The task type
        :param inference_id: The inference Id
        """
        __path_parts: t.Dict[str, str]
        if task_type not in SKIP_IN_PATH and inference_id not in SKIP_IN_PATH:
            __path_parts = {
                "task_type": _quote(task_type),
                "inference_id": _quote(inference_id),
            }
            __path = f'/_inference/{__path_parts["task_type"]}/{__path_parts["inference_id"]}'
        elif inference_id not in SKIP_IN_PATH:
            __path_parts = {"inference_id": _quote(inference_id)}
            __path = f'/_inference/{__path_parts["inference_id"]}'
        else:
            __path_parts = {}
            __path = "/_inference"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="inference.get",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("input", "query", "task_settings"),
    )
    @_stability_warning(Stability.EXPERIMENTAL)
    def inference(
        self,
        *,
        inference_id: str,
        input: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        task_type: t.Optional[
            t.Union[
                str,
                t.Literal["completion", "rerank", "sparse_embedding", "text_embedding"],
            ]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        query: t.Optional[str] = None,
        task_settings: t.Optional[t.Any] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Perform inference on the service

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/post-inference-api.html>`_

        :param inference_id: The inference Id
        :param input: Inference input. Either a string or an array of strings.
        :param task_type: The task type
        :param query: Query input, required for rerank task. Not required for other tasks.
        :param task_settings: Optional task settings
        :param timeout: Specifies the amount of time to wait for the inference request
            to complete.
        """
        if inference_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'inference_id'")
        if input is None and body is None:
            raise ValueError("Empty value passed for parameter 'input'")
        __path_parts: t.Dict[str, str]
        if task_type not in SKIP_IN_PATH and inference_id not in SKIP_IN_PATH:
            __path_parts = {
                "task_type": _quote(task_type),
                "inference_id": _quote(inference_id),
            }
            __path = f'/_inference/{__path_parts["task_type"]}/{__path_parts["inference_id"]}'
        elif inference_id not in SKIP_IN_PATH:
            __path_parts = {"inference_id": _quote(inference_id)}
            __path = f'/_inference/{__path_parts["inference_id"]}'
        else:
            raise ValueError("Couldn't find a path for the given parameters")
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = body if body is not None else {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if not __body:
            if input is not None:
                __body["input"] = input
            if query is not None:
                __body["query"] = query
            if task_settings is not None:
                __body["task_settings"] = task_settings
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="inference.inference",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_name="inference_config",
    )
    @_stability_warning(Stability.EXPERIMENTAL)
    def put(
        self,
        *,
        inference_id: str,
        inference_config: t.Optional[t.Mapping[str, t.Any]] = None,
        body: t.Optional[t.Mapping[str, t.Any]] = None,
        task_type: t.Optional[
            t.Union[
                str,
                t.Literal["completion", "rerank", "sparse_embedding", "text_embedding"],
            ]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Create an inference endpoint

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/put-inference-api.html>`_

        :param inference_id: The inference Id
        :param inference_config:
        :param task_type: The task type
        """
        if inference_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'inference_id'")
        if inference_config is None and body is None:
            raise ValueError(
                "Empty value passed for parameters 'inference_config' and 'body', one of them should be set."
            )
        elif inference_config is not None and body is not None:
            raise ValueError("Cannot set both 'inference_config' and 'body'")
        __path_parts: t.Dict[str, str]
        if task_type not in SKIP_IN_PATH and inference_id not in SKIP_IN_PATH:
            __path_parts = {
                "task_type": _quote(task_type),
                "inference_id": _quote(inference_id),
            }
            __path = f'/_inference/{__path_parts["task_type"]}/{__path_parts["inference_id"]}'
        elif inference_id not in SKIP_IN_PATH:
            __path_parts = {"inference_id": _quote(inference_id)}
            __path = f'/_inference/{__path_parts["inference_id"]}'
        else:
            raise ValueError("Couldn't find a path for the given parameters")
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __body = inference_config if inference_config is not None else body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="inference.put",
            path_parts=__path_parts,
        )

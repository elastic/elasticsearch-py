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

from typing import Any, Dict, List, Optional, Union

from elastic_transport import ObjectApiResponse

from ._base import NamespacedClient
from .utils import SKIP_IN_PATH, _quote, _rewrite_parameters


class IngestClient(NamespacedClient):
    @_rewrite_parameters()
    async def delete_pipeline(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes a pipeline.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/delete-pipeline-api.html>`_

        :param id: Pipeline ID
        :param master_timeout: Explicit operation timeout for connection to master node
        :param timeout: Explicit operation timeout
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_ingest/pipeline/{_quote(id)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def geo_ip_stats(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns statistical information about geoip databases

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/geoip-stats-api.html>`_
        """
        __path = "/_ingest/geoip/stats"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_pipeline(
        self,
        *,
        id: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        summary: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns a pipeline.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/get-pipeline-api.html>`_

        :param id: Comma separated list of pipeline ids. Wildcards supported
        :param master_timeout: Explicit operation timeout for connection to master node
        :param summary: Return pipelines without their definitions (default: false)
        """
        if id not in SKIP_IN_PATH:
            __path = f"/_ingest/pipeline/{_quote(id)}"
        else:
            __path = "/_ingest/pipeline"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if summary is not None:
            __query["summary"] = summary
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def processor_grok(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns a list of the built-in patterns.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/grok-processor.html#grok-processor-rest-get>`_
        """
        __path = "/_ingest/processor/grok"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"_meta": "meta"},
    )
    async def put_pipeline(
        self,
        *,
        id: Any,
        description: Optional[str] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        meta: Optional[Any] = None,
        on_failure: Optional[List[Any]] = None,
        pretty: Optional[bool] = None,
        processors: Optional[List[Any]] = None,
        timeout: Optional[Any] = None,
        version: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates or updates a pipeline.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/put-pipeline-api.html>`_

        :param id: ID of the ingest pipeline to create or update.
        :param description: Description of the ingest pipeline.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param meta: Optional metadata about the ingest pipeline. May have any contents.
            This map is not automatically generated by Elasticsearch.
        :param on_failure: Processors to run immediately after a processor failure. Each
            processor supports a processor-level `on_failure` value. If a processor without
            an `on_failure` value fails, Elasticsearch uses this pipeline-level parameter
            as a fallback. The processors in this parameter run sequentially in the order
            specified. Elasticsearch will not attempt to run the pipeline's remaining
            processors.
        :param processors: Processors used to perform transformations on documents before
            indexing. Processors run sequentially in the order specified.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        :param version: Version number used by external systems to track ingest pipelines.
            This parameter is intended for external systems only. Elasticsearch does
            not use or validate pipeline version numbers.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_ingest/pipeline/{_quote(id)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if description is not None:
            __body["description"] = description
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if meta is not None:
            __body["_meta"] = meta
        if on_failure is not None:
            __body["on_failure"] = on_failure
        if pretty is not None:
            __query["pretty"] = pretty
        if processors is not None:
            __body["processors"] = processors
        if timeout is not None:
            __query["timeout"] = timeout
        if version is not None:
            __body["version"] = version
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    async def simulate(
        self,
        *,
        id: Optional[Any] = None,
        docs: Optional[List[Any]] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pipeline: Optional[Any] = None,
        pretty: Optional[bool] = None,
        verbose: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Allows to simulate a pipeline with example documents.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/simulate-pipeline-api.html>`_

        :param id: Pipeline ID
        :param docs:
        :param pipeline:
        :param verbose: Verbose mode. Display data output for each processor in executed
            pipeline
        """
        if id not in SKIP_IN_PATH:
            __path = f"/_ingest/pipeline/{_quote(id)}/_simulate"
        else:
            __path = "/_ingest/pipeline/_simulate"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if docs is not None:
            __body["docs"] = docs
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pipeline is not None:
            __body["pipeline"] = pipeline
        if pretty is not None:
            __query["pretty"] = pretty
        if verbose is not None:
            __query["verbose"] = verbose
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

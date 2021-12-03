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
from .utils import SKIP_IN_PATH, _quote, _quote_query, _rewrite_parameters


class RollupClient(NamespacedClient):
    @_rewrite_parameters()
    def delete_job(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes an existing rollup job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-delete-job.html>`_

        :param id: The ID of the job to delete
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_rollup/job/{_quote(id)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def get_jobs(
        self,
        *,
        id: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves the configuration, stats, and status of rollup jobs.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-get-job.html>`_

        :param id: The ID of the job(s) to fetch. Accepts glob patterns, or left blank
            for all jobs
        """
        if id not in SKIP_IN_PATH:
            __path = f"/_rollup/job/{_quote(id)}"
        else:
            __path = "/_rollup/job"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def get_rollup_caps(
        self,
        *,
        id: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns the capabilities of any rollup jobs that have been configured for a specific
        index or index pattern.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-get-rollup-caps.html>`_

        :param id: The ID of the index to check rollup capabilities on, or left blank
            for all jobs
        """
        if id not in SKIP_IN_PATH:
            __path = f"/_rollup/data/{_quote(id)}"
        else:
            __path = "/_rollup/data"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def get_rollup_index_caps(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns the rollup capabilities of all jobs inside of a rollup index (e.g. the
        index where rollup data is stored).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-get-rollup-index-caps.html>`_

        :param index: The rollup index or index pattern to obtain rollup capabilities
            from.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_rollup/data"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_job(
        self,
        *,
        id: Any,
        cron: Optional[str] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        groups: Optional[Any] = None,
        human: Optional[bool] = None,
        index_pattern: Optional[str] = None,
        metrics: Optional[List[Any]] = None,
        page_size: Optional[int] = None,
        pretty: Optional[bool] = None,
        rollup_index: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a rollup job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-put-job.html>`_

        :param id: The ID of the job to create
        :param cron:
        :param groups:
        :param index_pattern:
        :param metrics:
        :param page_size:
        :param rollup_index:
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_rollup/job/{_quote(id)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if cron is not None:
            __body["cron"] = cron
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if groups is not None:
            __body["groups"] = groups
        if human is not None:
            __query["human"] = human
        if index_pattern is not None:
            __body["index_pattern"] = index_pattern
        if metrics is not None:
            __body["metrics"] = metrics
        if page_size is not None:
            __body["page_size"] = page_size
        if pretty is not None:
            __query["pretty"] = pretty
        if rollup_index is not None:
            __body["rollup_index"] = rollup_index
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_name="config",
    )
    def rollup(
        self,
        *,
        index: Any,
        rollup_index: Any,
        config: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Rollup an index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-rollup.html>`_

        :param index: The index to roll up
        :param rollup_index: The name of the rollup index to create
        :param config:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if rollup_index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'rollup_index'")
        if config is None:
            raise ValueError("Empty value passed for parameter 'config'")
        __path = f"/{_quote(index)}/_rollup/{_quote(rollup_index)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __body = config
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def rollup_search(
        self,
        *,
        index: Any,
        aggregations: Optional[Dict[str, Any]] = None,
        aggs: Optional[Dict[str, Any]] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        query: Optional[Any] = None,
        rest_total_hits_as_int: Optional[bool] = None,
        size: Optional[int] = None,
        typed_keys: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Enables searching rolled-up data using the standard query DSL.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-search.html>`_

        :param index: The indices or index-pattern(s) (containing rollup or regular data)
            that should be searched
        :param aggregations:
        :param aggs:
        :param query:
        :param rest_total_hits_as_int: Indicates whether hits.total should be rendered
            as an integer or an object in the rest search response
        :param size: Must be zero if set, as rollups work on pre-aggregated data
        :param typed_keys: Specify whether aggregation and suggester names should be
            prefixed by their respective types in the response
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_rollup_search"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if aggregations is not None:
            __body["aggregations"] = aggregations
        if aggs is not None:
            __body["aggs"] = aggs
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if query is not None:
            __body["query"] = query
        if rest_total_hits_as_int is not None:
            __query["rest_total_hits_as_int"] = rest_total_hits_as_int
        if size is not None:
            __body["size"] = size
        if typed_keys is not None:
            __query["typed_keys"] = typed_keys
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def start_job(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Starts an existing, stopped rollup job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-start-job.html>`_

        :param id: The ID of the job to start
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_rollup/job/{_quote(id)}/_start"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def stop_job(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Stops an existing, started rollup job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-stop-job.html>`_

        :param id: The ID of the job to stop
        :param timeout: Block for (at maximum) the specified duration while waiting for
            the job to stop. Defaults to 30s.
        :param wait_for_completion: True if the API should block until the job has fully
            stopped, false if should be executed async. Defaults to false.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_rollup/job/{_quote(id)}/_stop"
        __query: Dict[str, Any] = {}
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
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

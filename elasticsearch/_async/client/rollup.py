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


class RollupClient(NamespacedClient):
    @_rewrite_parameters()
    async def delete_job(
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_jobs(
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_rollup_caps(
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_rollup_index_caps(
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
        ignore_deprecated_options={"headers"},
    )
    async def put_job(
        self,
        *,
        id: Any,
        cron: str,
        groups: Any,
        index_pattern: str,
        page_size: int,
        rollup_index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        headers: Optional[Any] = None,
        human: Optional[bool] = None,
        metrics: Optional[List[Any]] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a rollup job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/rollup-put-job.html>`_

        :param id: Identifier for the rollup job. This can be any alphanumeric string
            and uniquely identifies the data that is associated with the rollup job.
            The ID is persistent; it is stored with the rolled up data. If you create
            a job, let it run for a while, then delete the job, the data that the job
            rolled up is still be associated with this job ID. You cannot create a new
            job with the same ID since that could lead to problems with mismatched job
            configurations.
        :param cron: A cron string which defines the intervals when the rollup job should
            be executed. When the interval triggers, the indexer attempts to rollup the
            data in the index pattern. The cron pattern is unrelated to the time interval
            of the data being rolled up. For example, you may wish to create hourly rollups
            of your document but to only run the indexer on a daily basis at midnight,
            as defined by the cron. The cron pattern is defined just like a Watcher cron
            schedule.
        :param groups: Defines the grouping fields and aggregations that are defined
            for this rollup job. These fields will then be available later for aggregating
            into buckets. These aggs and fields can be used in any combination. Think
            of the groups configuration as defining a set of tools that can later be
            used in aggregations to partition the data. Unlike raw data, we have to think
            ahead to which fields and aggregations might be used. Rollups provide enough
            flexibility that you simply need to determine which fields are needed, not
            in what order they are needed.
        :param index_pattern: The index or index pattern to roll up. Supports wildcard-style
            patterns (`logstash-*`). The job attempts to rollup the entire index or index-pattern.
        :param page_size: The number of bucket results that are processed on each iteration
            of the rollup indexer. A larger value tends to execute faster, but requires
            more memory during processing. This value has no effect on how the data is
            rolled up; it is merely used for tweaking the speed or memory cost of the
            indexer.
        :param rollup_index: The index that contains the rollup results. The index can
            be shared with other rollup jobs. The data is stored so that it doesn’t interfere
            with unrelated jobs.
        :param headers:
        :param metrics: Defines the metrics to collect for each grouping tuple. By default,
            only the doc_counts are collected for each group. To make rollup useful,
            you will often add metrics like averages, mins, maxes, etc. Metrics are defined
            on a per-field basis and for each field you configure which metric should
            be collected.
        :param timeout: Time to wait for the request to complete.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        if cron is None:
            raise ValueError("Empty value passed for parameter 'cron'")
        if groups is None:
            raise ValueError("Empty value passed for parameter 'groups'")
        if index_pattern is None:
            raise ValueError("Empty value passed for parameter 'index_pattern'")
        if page_size is None:
            raise ValueError("Empty value passed for parameter 'page_size'")
        if rollup_index is None:
            raise ValueError("Empty value passed for parameter 'rollup_index'")
        __path = f"/_rollup/job/{_quote(id)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if cron is not None:
            __body["cron"] = cron
        if groups is not None:
            __body["groups"] = groups
        if index_pattern is not None:
            __body["index_pattern"] = index_pattern
        if page_size is not None:
            __body["page_size"] = page_size
        if rollup_index is not None:
            __body["rollup_index"] = rollup_index
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if headers is not None:
            __body["headers"] = headers
        if human is not None:
            __query["human"] = human
        if metrics is not None:
            __body["metrics"] = metrics
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __body["timeout"] = timeout
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_name="config",
    )
    async def rollup(
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
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    async def rollup_search(
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
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    async def start_job(
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def stop_job(
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

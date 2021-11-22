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

from elastic_transport import ObjectApiResponse, TextApiResponse

from ._base import NamespacedClient
from .utils import SKIP_IN_PATH, _quote, _quote_query, _rewrite_parameters


class NodesClient(NamespacedClient):
    @_rewrite_parameters()
    def hot_threads(
        self,
        *,
        node_id: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_idle_threads: Optional[bool] = None,
        interval: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        snapshots: Optional[int] = None,
        threads: Optional[int] = None,
        timeout: Optional[Any] = None,
        type: Optional[Any] = None,
    ) -> TextApiResponse:
        """
        Returns information about hot threads on each node in the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/cluster-nodes-hot-threads.html>`_

        :param node_id: List of node IDs or names used to limit returned information.
        :param ignore_idle_threads: If true, known idle threads (e.g. waiting in a socket
            select, or to get a task from an empty queue) are filtered out.
        :param interval: The interval to do the second sampling of threads.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param snapshots: Number of samples of thread stacktrace.
        :param threads: Specifies the number of hot threads to provide information for.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        :param type: The type to sample.
        """
        if node_id not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/hot_threads"
        else:
            __path = "/_nodes/hot_threads"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_idle_threads is not None:
            __query["ignore_idle_threads"] = ignore_idle_threads
        if interval is not None:
            __query["interval"] = interval
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if snapshots is not None:
            __query["snapshots"] = snapshots
        if threads is not None:
            __query["threads"] = threads
        if timeout is not None:
            __query["timeout"] = timeout
        if type is not None:
            __query["type"] = type
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "text/plain"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def info(
        self,
        *,
        node_id: Optional[Any] = None,
        metric: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        flat_settings: Optional[bool] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns information about nodes in the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/cluster-nodes-info.html>`_

        :param node_id: Comma-separated list of node IDs or names used to limit returned
            information.
        :param metric: Limits the information returned to the specific metrics. Supports
            a comma-separated list, such as http,ingest.
        :param flat_settings: If true, returns settings in flat format.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        if node_id not in SKIP_IN_PATH and metric not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/{_quote(metric)}"
        elif node_id not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}"
        elif metric not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(metric)}"
        else:
            __path = "/_nodes"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def reload_secure_settings(
        self,
        *,
        node_id: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        secure_settings_password: Optional[Any] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Reloads secure settings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/secure-settings.html#reloadable-secure-settings>`_

        :param node_id: A comma-separated list of node IDs to span the reload/reinit
            call. Should stay empty because reloading usually involves all cluster nodes.
        :param secure_settings_password:
        :param timeout: Explicit operation timeout
        """
        if node_id not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/reload_secure_settings"
        else:
            __path = "/_nodes/reload_secure_settings"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if secure_settings_password is not None:
            __body["secure_settings_password"] = secure_settings_password
        if timeout is not None:
            __query["timeout"] = timeout
        if not __body:
            __body = None  # type: ignore[assignment]
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def stats(
        self,
        *,
        node_id: Optional[Any] = None,
        metric: Optional[Any] = None,
        index_metric: Optional[Any] = None,
        completion_fields: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        fielddata_fields: Optional[Any] = None,
        fields: Optional[Any] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        groups: Optional[bool] = None,
        human: Optional[bool] = None,
        include_segment_file_sizes: Optional[bool] = None,
        include_unloaded_segments: Optional[bool] = None,
        level: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
        types: Optional[List[str]] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns statistical information about nodes in the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/cluster-nodes-stats.html>`_

        :param node_id: Comma-separated list of node IDs or names used to limit returned
            information.
        :param metric: Limit the information returned to the specified metrics
        :param index_metric: Limit the information returned for indices metric to the
            specific index metrics. It can be used only if indices (or all) metric is
            specified.
        :param completion_fields: Comma-separated list or wildcard expressions of fields
            to include in fielddata and suggest statistics.
        :param fielddata_fields: Comma-separated list or wildcard expressions of fields
            to include in fielddata statistics.
        :param fields: Comma-separated list or wildcard expressions of fields to include
            in the statistics.
        :param groups: Comma-separated list of search groups to include in the search
            statistics.
        :param include_segment_file_sizes: If true, the call reports the aggregated disk
            usage of each one of the Lucene index files (only applies if segment stats
            are requested).
        :param include_unloaded_segments: If set to true segment stats will include stats
            for segments that are not currently loaded into memory
        :param level: Indicates whether statistics are aggregated at the cluster, index,
            or shard level.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        :param types: A comma-separated list of document types for the indexing index
            metric.
        """
        if (
            node_id not in SKIP_IN_PATH
            and metric not in SKIP_IN_PATH
            and index_metric not in SKIP_IN_PATH
        ):
            __path = f"/_nodes/{_quote(node_id)}/stats/{_quote(metric)}/{_quote(index_metric)}"
        elif node_id not in SKIP_IN_PATH and metric not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/stats/{_quote(metric)}"
        elif metric not in SKIP_IN_PATH and index_metric not in SKIP_IN_PATH:
            __path = f"/_nodes/stats/{_quote(metric)}/{_quote(index_metric)}"
        elif node_id not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/stats"
        elif metric not in SKIP_IN_PATH:
            __path = f"/_nodes/stats/{_quote(metric)}"
        else:
            __path = "/_nodes/stats"
        __query: Dict[str, Any] = {}
        if completion_fields is not None:
            __query["completion_fields"] = completion_fields
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if fielddata_fields is not None:
            __query["fielddata_fields"] = fielddata_fields
        if fields is not None:
            __query["fields"] = fields
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if groups is not None:
            __query["groups"] = groups
        if human is not None:
            __query["human"] = human
        if include_segment_file_sizes is not None:
            __query["include_segment_file_sizes"] = include_segment_file_sizes
        if include_unloaded_segments is not None:
            __query["include_unloaded_segments"] = include_unloaded_segments
        if level is not None:
            __query["level"] = level
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if types is not None:
            __query["types"] = types
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def usage(
        self,
        *,
        node_id: Optional[Any] = None,
        metric: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns low-level information about REST actions usage on nodes.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/cluster-nodes-usage.html>`_

        :param node_id: A comma-separated list of node IDs or names to limit the returned
            information; use `_local` to return information from the node you're connecting
            to, leave empty to get information from all nodes
        :param metric: Limit the information returned to the specified metrics
        :param timeout: Explicit operation timeout
        """
        if node_id not in SKIP_IN_PATH and metric not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/usage/{_quote(metric)}"
        elif node_id not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/usage"
        elif metric not in SKIP_IN_PATH:
            __path = f"/_nodes/usage/{_quote(metric)}"
        else:
            __path = "/_nodes/usage"
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

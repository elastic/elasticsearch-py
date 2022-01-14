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


class WatcherClient(NamespacedClient):
    @_rewrite_parameters()
    def ack_watch(
        self,
        *,
        watch_id: Any,
        action_id: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Acknowledges a watch, manually throttling the execution of the watch's actions.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-ack-watch.html>`_

        :param watch_id: Watch ID
        :param action_id: A comma-separated list of the action ids to be acked
        """
        if watch_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'watch_id'")
        if watch_id not in SKIP_IN_PATH and action_id not in SKIP_IN_PATH:
            __path = f"/_watcher/watch/{_quote(watch_id)}/_ack/{_quote(action_id)}"
        elif watch_id not in SKIP_IN_PATH:
            __path = f"/_watcher/watch/{_quote(watch_id)}/_ack"
        else:
            raise ValueError("Couldn't find a path for the given parameters")
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
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def activate_watch(
        self,
        *,
        watch_id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Activates a currently inactive watch.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-activate-watch.html>`_

        :param watch_id: Watch ID
        """
        if watch_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'watch_id'")
        __path = f"/_watcher/watch/{_quote(watch_id)}/_activate"
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
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def deactivate_watch(
        self,
        *,
        watch_id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deactivates a currently active watch.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-deactivate-watch.html>`_

        :param watch_id: Watch ID
        """
        if watch_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'watch_id'")
        __path = f"/_watcher/watch/{_quote(watch_id)}/_deactivate"
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
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_watch(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes a watch from Watcher.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-delete-watch.html>`_

        :param id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_watcher/watch/{_quote(id)}"
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
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def execute_watch(
        self,
        *,
        id: Optional[Any] = None,
        action_modes: Optional[Dict[str, Any]] = None,
        alternative_input: Optional[Dict[str, Any]] = None,
        debug: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_condition: Optional[bool] = None,
        pretty: Optional[bool] = None,
        record_execution: Optional[bool] = None,
        simulated_actions: Optional[Any] = None,
        trigger_data: Optional[Any] = None,
        watch: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Forces the execution of a stored watch.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-execute-watch.html>`_

        :param id: Identifier for the watch.
        :param action_modes: Determines how to handle the watch actions as part of the
            watch execution. See [Action execution modes](https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-execute-watch.html#watcher-api-execute-watch-action-mode)
            for more information.
        :param alternative_input: When present, the watch uses this object as a payload
            instead of executing its own input.
        :param debug: Defines whether the watch runs in debug mode.
        :param ignore_condition: When set to `true`, the watch execution uses the always
            condition. This can also be specified as an HTTP parameter.
        :param record_execution: When set to `true`, the watch record representing the
            watch execution result is persisted to the `.watcher-history` index for the
            current time. In addition, the status of the watch is updated, possibly throttling
            subsequent executions. This can also be specified as an HTTP parameter.
        :param simulated_actions:
        :param trigger_data: This structure is parsed as the data of the trigger event
            that will be used during the watch execution
        :param watch: When present, this [watch](https://www.elastic.co/guide/en/elasticsearch/reference/current/how-watcher-works.html#watch-definition)
            is used instead of the one specified in the request. This watch is not persisted
            to the index and record_execution cannot be set.
        """
        if id not in SKIP_IN_PATH:
            __path = f"/_watcher/watch/{_quote(id)}/_execute"
        else:
            __path = "/_watcher/watch/_execute"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if action_modes is not None:
            __body["action_modes"] = action_modes
        if alternative_input is not None:
            __body["alternative_input"] = alternative_input
        if debug is not None:
            __query["debug"] = debug
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_condition is not None:
            __body["ignore_condition"] = ignore_condition
        if pretty is not None:
            __query["pretty"] = pretty
        if record_execution is not None:
            __body["record_execution"] = record_execution
        if simulated_actions is not None:
            __body["simulated_actions"] = simulated_actions
        if trigger_data is not None:
            __body["trigger_data"] = trigger_data
        if watch is not None:
            __body["watch"] = watch
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def get_watch(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves a watch by its ID.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-get-watch.html>`_

        :param id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_watcher/watch/{_quote(id)}"
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
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_watch(
        self,
        *,
        id: Any,
        actions: Optional[Dict[str, Any]] = None,
        active: Optional[bool] = None,
        condition: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        if_primary_term: Optional[int] = None,
        if_seq_no: Optional[Any] = None,
        input: Optional[Any] = None,
        metadata: Optional[Any] = None,
        pretty: Optional[bool] = None,
        throttle_period: Optional[str] = None,
        transform: Optional[Any] = None,
        trigger: Optional[Any] = None,
        version: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a new watch, or updates an existing one.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-put-watch.html>`_

        :param id: Watch ID
        :param actions:
        :param active: Specify whether the watch is in/active by default
        :param condition:
        :param if_primary_term: only update the watch if the last operation that has
            changed the watch has the specified primary term
        :param if_seq_no: only update the watch if the last operation that has changed
            the watch has the specified sequence number
        :param input:
        :param metadata:
        :param throttle_period:
        :param transform:
        :param trigger:
        :param version: Explicit version number for concurrency control
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_watcher/watch/{_quote(id)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if actions is not None:
            __body["actions"] = actions
        if active is not None:
            __query["active"] = active
        if condition is not None:
            __body["condition"] = condition
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if if_primary_term is not None:
            __query["if_primary_term"] = if_primary_term
        if if_seq_no is not None:
            __query["if_seq_no"] = if_seq_no
        if input is not None:
            __body["input"] = input
        if metadata is not None:
            __body["metadata"] = metadata
        if pretty is not None:
            __query["pretty"] = pretty
        if throttle_period is not None:
            __body["throttle_period"] = throttle_period
        if transform is not None:
            __body["transform"] = transform
        if trigger is not None:
            __body["trigger"] = trigger
        if version is not None:
            __query["version"] = version
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"from": "from_"},
    )
    def query_watches(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        from_: Optional[int] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        query: Optional[Any] = None,
        search_after: Optional[Any] = None,
        size: Optional[int] = None,
        sort: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves stored watches.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-query-watches.html>`_

        :param from_: The offset from the first result to fetch. Needs to be non-negative.
        :param query: Optional, query filter watches to be returned.
        :param search_after: Optional search After to do pagination using last hit’s
            sort values.
        :param size: The number of hits to return. Needs to be non-negative.
        :param sort: Optional sort definition.
        """
        __path = "/_watcher/_query/watches"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if from_ is not None:
            __body["from"] = from_
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if query is not None:
            __body["query"] = query
        if search_after is not None:
            __body["search_after"] = search_after
        if size is not None:
            __body["size"] = size
        if sort is not None:
            __body["sort"] = sort
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def start(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Starts Watcher if it is not already running.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-start.html>`_
        """
        __path = "/_watcher/_start"
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
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def stats(
        self,
        *,
        metric: Optional[Union[Any, List[Any]]] = None,
        emit_stacktraces: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves the current Watcher metrics.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-stats.html>`_

        :param metric: Defines which additional metrics are included in the response.
        :param emit_stacktraces: Defines whether stack traces are generated for each
            watch that is running.
        """
        if metric not in SKIP_IN_PATH:
            __path = f"/_watcher/stats/{_quote(metric)}"
        else:
            __path = "/_watcher/stats"
        __query: Dict[str, Any] = {}
        if emit_stacktraces is not None:
            __query["emit_stacktraces"] = emit_stacktraces
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
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def stop(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Stops Watcher if it is running.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-stop.html>`_
        """
        __path = "/_watcher/_stop"
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
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

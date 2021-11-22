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


class TasksClient(NamespacedClient):
    @_rewrite_parameters()
    async def cancel(
        self,
        *,
        task_id: Optional[Any] = None,
        actions: Optional[Union[List[str], str]] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        nodes: Optional[List[str]] = None,
        parent_task_id: Optional[str] = None,
        pretty: Optional[bool] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Cancels a task, if it can be cancelled through an API.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/tasks.html>`_

        :param task_id: Cancel the task with specified task id (node_id:task_number)
        :param actions: A comma-separated list of actions that should be cancelled. Leave
            empty to cancel all.
        :param nodes: A comma-separated list of node IDs or names to limit the returned
            information; use `_local` to return information from the node you're connecting
            to, leave empty to get information from all nodes
        :param parent_task_id: Cancel tasks with specified parent task id (node_id:task_number).
            Set to -1 to cancel all.
        :param wait_for_completion: Should the request block until the cancellation of
            the task and its descendant tasks is completed. Defaults to false
        """
        if task_id not in SKIP_IN_PATH:
            __path = f"/_tasks/{_quote(task_id)}/_cancel"
        else:
            __path = "/_tasks/_cancel"
        __query: Dict[str, Any] = {}
        if actions is not None:
            __query["actions"] = actions
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if nodes is not None:
            __query["nodes"] = nodes
        if parent_task_id is not None:
            __query["parent_task_id"] = parent_task_id
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get(
        self,
        *,
        task_id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns information about a task.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/tasks.html>`_

        :param task_id: Return the task with specified id (node_id:task_number)
        :param timeout: Explicit operation timeout
        :param wait_for_completion: Wait for the matching tasks to complete (default:
            false)
        """
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'task_id'")
        __path = f"/_tasks/{_quote(task_id)}"
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
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def list(
        self,
        *,
        actions: Optional[Union[List[str], str]] = None,
        detailed: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        group_by: Optional[Any] = None,
        human: Optional[bool] = None,
        nodes: Optional[List[str]] = None,
        parent_task_id: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns a list of tasks.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/tasks.html>`_

        :param actions: A comma-separated list of actions that should be returned. Leave
            empty to return all.
        :param detailed: Return detailed task information (default: false)
        :param group_by: Group tasks by nodes or parent/child relationships
        :param nodes: A comma-separated list of node IDs or names to limit the returned
            information; use `_local` to return information from the node you're connecting
            to, leave empty to get information from all nodes
        :param parent_task_id: Return tasks with specified parent task id (node_id:task_number).
            Set to -1 to return all.
        :param timeout: Explicit operation timeout
        :param wait_for_completion: Wait for the matching tasks to complete (default:
            false)
        """
        __path = "/_tasks"
        __query: Dict[str, Any] = {}
        if actions is not None:
            __query["actions"] = actions
        if detailed is not None:
            __query["detailed"] = detailed
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if group_by is not None:
            __query["group_by"] = group_by
        if human is not None:
            __query["human"] = human
        if nodes is not None:
            __query["nodes"] = nodes
        if parent_task_id is not None:
            __query["parent_task_id"] = parent_task_id
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
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

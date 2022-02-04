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
from .utils import SKIP_IN_PATH, _quote, _rewrite_parameters


class TasksClient(NamespacedClient):
    @_rewrite_parameters()
    async def cancel(
        self,
        *,
        task_id: t.Optional[t.Union[int, str]] = None,
        actions: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        nodes: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        parent_task_id: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        wait_for_completion: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Cancels a task, if it can be cancelled through an API.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.0/tasks.html>`_

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
        __query: t.Dict[str, t.Any] = {}
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get(
        self,
        *,
        task_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[int, str]] = None,
        wait_for_completion: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns information about a task.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.0/tasks.html>`_

        :param task_id: Return the task with specified id (node_id:task_number)
        :param timeout: Explicit operation timeout
        :param wait_for_completion: Wait for the matching tasks to complete (default:
            false)
        """
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'task_id'")
        __path = f"/_tasks/{_quote(task_id)}"
        __query: t.Dict[str, t.Any] = {}
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
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def list(
        self,
        *,
        actions: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        detailed: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        group_by: t.Optional[
            t.Union["t.Literal['nodes', 'none', 'parents']", str]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[int, str]] = None,
        node_id: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        parent_task_id: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[int, str]] = None,
        wait_for_completion: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns a list of tasks.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.0/tasks.html>`_

        :param actions: Comma-separated list or wildcard expression of actions used to
            limit the request.
        :param detailed: If `true`, the response includes detailed information about
            shard recoveries.
        :param group_by: Key used to group tasks in the response.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param node_id: Comma-separated list of node IDs or names used to limit returned
            information.
        :param parent_task_id: Parent task ID used to limit returned information. To
            return all tasks, omit this parameter or use a value of `-1`.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        :param wait_for_completion: If `true`, the request blocks until the operation
            is complete.
        """
        __path = "/_tasks"
        __query: t.Dict[str, t.Any] = {}
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
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if node_id is not None:
            __query["node_id"] = node_id
        if parent_task_id is not None:
            __query["parent_task_id"] = parent_task_id
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

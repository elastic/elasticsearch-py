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


class SlmClient(NamespacedClient):

    @_rewrite_parameters()
    async def delete_lifecycle(
        self,
        *,
        policy_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Delete a policy. Delete a snapshot lifecycle policy definition. This operation
        prevents any future snapshots from being taken but does not cancel in-progress
        snapshots or remove previously-taken snapshots.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-delete-policy.html>`_

        :param policy_id: The id of the snapshot lifecycle policy to remove
        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error.
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'policy_id'")
        __path_parts: t.Dict[str, str] = {"policy_id": _quote(policy_id)}
        __path = f'/_slm/policy/{__path_parts["policy_id"]}'
        __query: t.Dict[str, t.Any] = {}
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
            "DELETE",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.delete_lifecycle",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def execute_lifecycle(
        self,
        *,
        policy_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Run a policy. Immediately create a snapshot according to the snapshot lifecycle
        policy without waiting for the scheduled time. The snapshot policy is normally
        applied according to its schedule, but you might want to manually run a policy
        before performing an upgrade or other maintenance.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-execute-lifecycle.html>`_

        :param policy_id: The id of the snapshot lifecycle policy to be executed
        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error.
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'policy_id'")
        __path_parts: t.Dict[str, str] = {"policy_id": _quote(policy_id)}
        __path = f'/_slm/policy/{__path_parts["policy_id"]}/_execute'
        __query: t.Dict[str, t.Any] = {}
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
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.execute_lifecycle",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def execute_retention(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Run a retention policy. Manually apply the retention policy to force immediate
        removal of snapshots that are expired according to the snapshot lifecycle policy
        retention rules. The retention policy is normally applied according to its schedule.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-execute-retention.html>`_

        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_slm/_execute_retention"
        __query: t.Dict[str, t.Any] = {}
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
            "POST",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.execute_retention",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def get_lifecycle(
        self,
        *,
        policy_id: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Get policy information. Get snapshot lifecycle policy definitions and information
        about the latest snapshot attempts.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-get-policy.html>`_

        :param policy_id: Comma-separated list of snapshot lifecycle policies to retrieve
        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error.
        """
        __path_parts: t.Dict[str, str]
        if policy_id not in SKIP_IN_PATH:
            __path_parts = {"policy_id": _quote(policy_id)}
            __path = f'/_slm/policy/{__path_parts["policy_id"]}'
        else:
            __path_parts = {}
            __path = "/_slm/policy"
        __query: t.Dict[str, t.Any] = {}
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
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.get_lifecycle",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def get_stats(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Get snapshot lifecycle management statistics. Get global and policy-level statistics
        about actions taken by snapshot lifecycle management.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-get-stats.html>`_

        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_slm/stats"
        __query: t.Dict[str, t.Any] = {}
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
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.get_stats",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def get_status(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Get the snapshot lifecycle management status.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-get-status.html>`_

        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error. To indicate that the request should never timeout,
            set it to `-1`.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error. To indicate
            that the request should never timeout, set it to `-1`.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_slm/status"
        __query: t.Dict[str, t.Any] = {}
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
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.get_status",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("config", "name", "repository", "retention", "schedule"),
    )
    async def put_lifecycle(
        self,
        *,
        policy_id: str,
        config: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        name: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        repository: t.Optional[str] = None,
        retention: t.Optional[t.Mapping[str, t.Any]] = None,
        schedule: t.Optional[str] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Create or update a policy. Create or update a snapshot lifecycle policy. If the
        policy already exists, this request increments the policy version. Only the latest
        version of a policy is stored.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-put-policy.html>`_

        :param policy_id: The identifier for the snapshot lifecycle policy you want to
            create or update.
        :param config: Configuration for each snapshot created by the policy.
        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error. To indicate that the request should never timeout,
            set it to `-1`.
        :param name: Name automatically assigned to each snapshot created by the policy.
            Date math is supported. To prevent conflicting snapshot names, a UUID is
            automatically appended to each snapshot name.
        :param repository: Repository used to store snapshots created by this policy.
            This repository must exist prior to the policy’s creation. You can create
            a repository using the snapshot repository API.
        :param retention: Retention rules used to retain and delete snapshots created
            by the policy.
        :param schedule: Periodic or absolute schedule at which the policy creates snapshots.
            SLM applies schedule changes immediately.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error. To indicate
            that the request should never timeout, set it to `-1`.
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'policy_id'")
        __path_parts: t.Dict[str, str] = {"policy_id": _quote(policy_id)}
        __path = f'/_slm/policy/{__path_parts["policy_id"]}'
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = body if body is not None else {}
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
        if not __body:
            if config is not None:
                __body["config"] = config
            if name is not None:
                __body["name"] = name
            if repository is not None:
                __body["repository"] = repository
            if retention is not None:
                __body["retention"] = retention
            if schedule is not None:
                __body["schedule"] = schedule
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return await self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="slm.put_lifecycle",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def start(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Start snapshot lifecycle management. Snapshot lifecycle management (SLM) starts
        automatically when a cluster is formed. Manually starting SLM is necessary only
        if it has been stopped using the stop SLM API.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-start.html>`_

        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error. To indicate that the request should never timeout,
            set it to `-1`.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error. To indicate
            that the request should never timeout, set it to `-1`.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_slm/start"
        __query: t.Dict[str, t.Any] = {}
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
            "POST",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.start",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def stop(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Stop snapshot lifecycle management. Stop all snapshot lifecycle management (SLM)
        operations and the SLM plugin. This API is useful when you are performing maintenance
        on a cluster and need to prevent SLM from performing any actions on your data
        streams or indices. Stopping SLM does not stop any snapshots that are in progress.
        You can manually trigger snapshots with the run snapshot lifecycle policy API
        even if SLM is stopped. The API returns a response as soon as the request is
        acknowledged, but the plugin might continue to run until in-progress operations
        complete and it can be safely stopped. Use the get snapshot lifecycle management
        status API to see if SLM is running.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.16/slm-api-stop.html>`_

        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error. To indicate that the request should never timeout,
            set it to `-1`.
        :param timeout: The period to wait for a response. If no response is received
            before the timeout expires, the request fails and returns an error. To indicate
            that the request should never timeout, set it to `-1`.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_slm/stop"
        __query: t.Dict[str, t.Any] = {}
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
            "POST",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="slm.stop",
            path_parts=__path_parts,
        )

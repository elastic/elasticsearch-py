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
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes an existing snapshot lifecycle policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-delete-policy.html>`_

        :param policy_id: The id of the snapshot lifecycle policy to remove
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'policy_id'")
        __path = f"/_slm/policy/{_quote(policy_id)}"
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
        return await self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def execute_lifecycle(
        self,
        *,
        policy_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Immediately creates a snapshot according to the lifecycle policy, without waiting
        for the scheduled time.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-execute-lifecycle.html>`_

        :param policy_id: The id of the snapshot lifecycle policy to be executed
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'policy_id'")
        __path = f"/_slm/policy/{_quote(policy_id)}/_execute"
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
        return await self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def execute_retention(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes any snapshots that are expired according to the policy's retention rules.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-execute-retention.html>`_
        """
        __path = "/_slm/_execute_retention"
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
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_lifecycle(
        self,
        *,
        policy_id: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves one or more snapshot lifecycle policy definitions and information about
        the latest snapshot attempts.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-get-policy.html>`_

        :param policy_id: Comma-separated list of snapshot lifecycle policies to retrieve
        """
        if policy_id not in SKIP_IN_PATH:
            __path = f"/_slm/policy/{_quote(policy_id)}"
        else:
            __path = "/_slm/policy"
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
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_stats(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns global and policy-level statistics about actions taken by snapshot lifecycle
        management.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-get-stats.html>`_
        """
        __path = "/_slm/stats"
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
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_status(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves the status of snapshot lifecycle management (SLM).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-get-status.html>`_
        """
        __path = "/_slm/status"
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
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    async def put_lifecycle(
        self,
        *,
        policy_id: str,
        config: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        name: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        repository: t.Optional[str] = None,
        retention: t.Optional[t.Mapping[str, t.Any]] = None,
        schedule: t.Optional[str] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates or updates a snapshot lifecycle policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-put-policy.html>`_

        :param policy_id: ID for the snapshot lifecycle policy you want to create or
            update.
        :param config: Configuration for each snapshot created by the policy.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
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
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'policy_id'")
        __path = f"/_slm/policy/{_quote(policy_id)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if config is not None:
            __body["config"] = config
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if name is not None:
            __body["name"] = name
        if pretty is not None:
            __query["pretty"] = pretty
        if repository is not None:
            __body["repository"] = repository
        if retention is not None:
            __body["retention"] = retention
        if schedule is not None:
            __body["schedule"] = schedule
        if timeout is not None:
            __query["timeout"] = timeout
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return await self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    async def start(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Turns on snapshot lifecycle management (SLM).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-start.html>`_
        """
        __path = "/_slm/start"
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
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def stop(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Turns off snapshot lifecycle management (SLM).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.10/slm-api-stop.html>`_
        """
        __path = "/_slm/stop"
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
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

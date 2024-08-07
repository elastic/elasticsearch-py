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


class ConnectorClient(NamespacedClient):

    @_rewrite_parameters()
    def check_in(
        self,
        *,
        connector_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the last_seen field in the connector, and sets it to current timestamp

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/check-in-connector-api.html>`_

        :param connector_id: The unique identifier of the connector to be checked in
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_check_in'
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
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="connector.check_in",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    def delete(
        self,
        *,
        connector_id: str,
        delete_sync_jobs: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a connector.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/delete-connector-api.html>`_

        :param connector_id: The unique identifier of the connector to be deleted
        :param delete_sync_jobs: A flag indicating if associated sync jobs should be
            also removed. Defaults to false.
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}'
        __query: t.Dict[str, t.Any] = {}
        if delete_sync_jobs is not None:
            __query["delete_sync_jobs"] = delete_sync_jobs
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
            "DELETE",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="connector.delete",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    def get(
        self,
        *,
        connector_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a connector.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/get-connector-api.html>`_

        :param connector_id: The unique identifier of the connector
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}'
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
            endpoint_id="connector.get",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=(
            "last_access_control_sync_error",
            "last_access_control_sync_scheduled_at",
            "last_access_control_sync_status",
            "last_deleted_document_count",
            "last_incremental_sync_scheduled_at",
            "last_indexed_document_count",
            "last_seen",
            "last_sync_error",
            "last_sync_scheduled_at",
            "last_sync_status",
            "last_synced",
            "sync_cursor",
        ),
    )
    def last_sync(
        self,
        *,
        connector_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        last_access_control_sync_error: t.Optional[str] = None,
        last_access_control_sync_scheduled_at: t.Optional[t.Union[str, t.Any]] = None,
        last_access_control_sync_status: t.Optional[
            t.Union[
                str,
                t.Literal[
                    "canceled",
                    "canceling",
                    "completed",
                    "error",
                    "in_progress",
                    "pending",
                    "suspended",
                ],
            ]
        ] = None,
        last_deleted_document_count: t.Optional[int] = None,
        last_incremental_sync_scheduled_at: t.Optional[t.Union[str, t.Any]] = None,
        last_indexed_document_count: t.Optional[int] = None,
        last_seen: t.Optional[t.Union[str, t.Any]] = None,
        last_sync_error: t.Optional[str] = None,
        last_sync_scheduled_at: t.Optional[t.Union[str, t.Any]] = None,
        last_sync_status: t.Optional[
            t.Union[
                str,
                t.Literal[
                    "canceled",
                    "canceling",
                    "completed",
                    "error",
                    "in_progress",
                    "pending",
                    "suspended",
                ],
            ]
        ] = None,
        last_synced: t.Optional[t.Union[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        sync_cursor: t.Optional[t.Any] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates last sync stats in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-last-sync-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param last_access_control_sync_error:
        :param last_access_control_sync_scheduled_at:
        :param last_access_control_sync_status:
        :param last_deleted_document_count:
        :param last_incremental_sync_scheduled_at:
        :param last_indexed_document_count:
        :param last_seen:
        :param last_sync_error:
        :param last_sync_scheduled_at:
        :param last_sync_status:
        :param last_synced:
        :param sync_cursor:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_last_sync'
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
        if not __body:
            if last_access_control_sync_error is not None:
                __body["last_access_control_sync_error"] = (
                    last_access_control_sync_error
                )
            if last_access_control_sync_scheduled_at is not None:
                __body["last_access_control_sync_scheduled_at"] = (
                    last_access_control_sync_scheduled_at
                )
            if last_access_control_sync_status is not None:
                __body["last_access_control_sync_status"] = (
                    last_access_control_sync_status
                )
            if last_deleted_document_count is not None:
                __body["last_deleted_document_count"] = last_deleted_document_count
            if last_incremental_sync_scheduled_at is not None:
                __body["last_incremental_sync_scheduled_at"] = (
                    last_incremental_sync_scheduled_at
                )
            if last_indexed_document_count is not None:
                __body["last_indexed_document_count"] = last_indexed_document_count
            if last_seen is not None:
                __body["last_seen"] = last_seen
            if last_sync_error is not None:
                __body["last_sync_error"] = last_sync_error
            if last_sync_scheduled_at is not None:
                __body["last_sync_scheduled_at"] = last_sync_scheduled_at
            if last_sync_status is not None:
                __body["last_sync_status"] = last_sync_status
            if last_synced is not None:
                __body["last_synced"] = last_synced
            if sync_cursor is not None:
                __body["sync_cursor"] = sync_cursor
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.last_sync",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        parameter_aliases={"from": "from_"},
    )
    def list(
        self,
        *,
        connector_name: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        from_: t.Optional[int] = None,
        human: t.Optional[bool] = None,
        index_name: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        pretty: t.Optional[bool] = None,
        query: t.Optional[str] = None,
        service_type: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns existing connectors.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/list-connector-api.html>`_

        :param connector_name: A comma-separated list of connector names to fetch connector
            documents for
        :param from_: Starting offset (default: 0)
        :param index_name: A comma-separated list of connector index names to fetch connector
            documents for
        :param query: A wildcard query string that filters connectors with matching name,
            description or index name
        :param service_type: A comma-separated list of connector service types to fetch
            connector documents for
        :param size: Specifies a max number of results to get
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_connector"
        __query: t.Dict[str, t.Any] = {}
        if connector_name is not None:
            __query["connector_name"] = connector_name
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if from_ is not None:
            __query["from"] = from_
        if human is not None:
            __query["human"] = human
        if index_name is not None:
            __query["index_name"] = index_name
        if pretty is not None:
            __query["pretty"] = pretty
        if query is not None:
            __query["query"] = query
        if service_type is not None:
            __query["service_type"] = service_type
        if size is not None:
            __query["size"] = size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="connector.list",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=(
            "description",
            "index_name",
            "is_native",
            "language",
            "name",
            "service_type",
        ),
    )
    def post(
        self,
        *,
        description: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        index_name: t.Optional[str] = None,
        is_native: t.Optional[bool] = None,
        language: t.Optional[str] = None,
        name: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        service_type: t.Optional[str] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a connector.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/create-connector-api.html>`_

        :param description:
        :param index_name:
        :param is_native:
        :param language:
        :param name:
        :param service_type:
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_connector"
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
        if not __body:
            if description is not None:
                __body["description"] = description
            if index_name is not None:
                __body["index_name"] = index_name
            if is_native is not None:
                __body["is_native"] = is_native
            if language is not None:
                __body["language"] = language
            if name is not None:
                __body["name"] = name
            if service_type is not None:
                __body["service_type"] = service_type
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
            endpoint_id="connector.post",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=(
            "description",
            "index_name",
            "is_native",
            "language",
            "name",
            "service_type",
        ),
    )
    def put(
        self,
        *,
        connector_id: t.Optional[str] = None,
        description: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        index_name: t.Optional[str] = None,
        is_native: t.Optional[bool] = None,
        language: t.Optional[str] = None,
        name: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        service_type: t.Optional[str] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates or updates a connector.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/create-connector-api.html>`_

        :param connector_id: The unique identifier of the connector to be created or
            updated. ID is auto-generated if not provided.
        :param description:
        :param index_name:
        :param is_native:
        :param language:
        :param name:
        :param service_type:
        """
        __path_parts: t.Dict[str, str]
        if connector_id not in SKIP_IN_PATH:
            __path_parts = {"connector_id": _quote(connector_id)}
            __path = f'/_connector/{__path_parts["connector_id"]}'
        else:
            __path_parts = {}
            __path = "/_connector"
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
        if not __body:
            if description is not None:
                __body["description"] = description
            if index_name is not None:
                __body["index_name"] = index_name
            if is_native is not None:
                __body["is_native"] = is_native
            if language is not None:
                __body["language"] = language
            if name is not None:
                __body["name"] = name
            if service_type is not None:
                __body["service_type"] = service_type
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.put",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    def sync_job_cancel(
        self,
        *,
        connector_sync_job_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Cancels a connector sync job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/cancel-connector-sync-job-api.html>`_

        :param connector_sync_job_id: The unique identifier of the connector sync job
        """
        if connector_sync_job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_sync_job_id'")
        __path_parts: t.Dict[str, str] = {
            "connector_sync_job_id": _quote(connector_sync_job_id)
        }
        __path = (
            f'/_connector/_sync_job/{__path_parts["connector_sync_job_id"]}/_cancel'
        )
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
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="connector.sync_job_cancel",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    def sync_job_delete(
        self,
        *,
        connector_sync_job_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a connector sync job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/delete-connector-sync-job-api.html>`_

        :param connector_sync_job_id: The unique identifier of the connector sync job
            to be deleted
        """
        if connector_sync_job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_sync_job_id'")
        __path_parts: t.Dict[str, str] = {
            "connector_sync_job_id": _quote(connector_sync_job_id)
        }
        __path = f'/_connector/_sync_job/{__path_parts["connector_sync_job_id"]}'
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
            "DELETE",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="connector.sync_job_delete",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    def sync_job_get(
        self,
        *,
        connector_sync_job_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves a connector sync job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/get-connector-sync-job-api.html>`_

        :param connector_sync_job_id: The unique identifier of the connector sync job
        """
        if connector_sync_job_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_sync_job_id'")
        __path_parts: t.Dict[str, str] = {
            "connector_sync_job_id": _quote(connector_sync_job_id)
        }
        __path = f'/_connector/_sync_job/{__path_parts["connector_sync_job_id"]}'
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
            endpoint_id="connector.sync_job_get",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        parameter_aliases={"from": "from_"},
    )
    def sync_job_list(
        self,
        *,
        connector_id: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        from_: t.Optional[int] = None,
        human: t.Optional[bool] = None,
        job_type: t.Optional[
            t.Union[
                t.Sequence[
                    t.Union[str, t.Literal["access_control", "full", "incremental"]]
                ],
                t.Union[str, t.Literal["access_control", "full", "incremental"]],
            ]
        ] = None,
        pretty: t.Optional[bool] = None,
        size: t.Optional[int] = None,
        status: t.Optional[
            t.Union[
                str,
                t.Literal[
                    "canceled",
                    "canceling",
                    "completed",
                    "error",
                    "in_progress",
                    "pending",
                    "suspended",
                ],
            ]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Lists connector sync jobs.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/list-connector-sync-jobs-api.html>`_

        :param connector_id: A connector id to fetch connector sync jobs for
        :param from_: Starting offset (default: 0)
        :param job_type: A comma-separated list of job types to fetch the sync jobs for
        :param size: Specifies a max number of results to get
        :param status: A sync job status to fetch connector sync jobs for
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_connector/_sync_job"
        __query: t.Dict[str, t.Any] = {}
        if connector_id is not None:
            __query["connector_id"] = connector_id
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if from_ is not None:
            __query["from"] = from_
        if human is not None:
            __query["human"] = human
        if job_type is not None:
            __query["job_type"] = job_type
        if pretty is not None:
            __query["pretty"] = pretty
        if size is not None:
            __query["size"] = size
        if status is not None:
            __query["status"] = status
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="connector.sync_job_list",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("id", "job_type", "trigger_method"),
    )
    def sync_job_post(
        self,
        *,
        id: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        job_type: t.Optional[
            t.Union[str, t.Literal["access_control", "full", "incremental"]]
        ] = None,
        pretty: t.Optional[bool] = None,
        trigger_method: t.Optional[
            t.Union[str, t.Literal["on_demand", "scheduled"]]
        ] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a connector sync job.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/create-connector-sync-job-api.html>`_

        :param id: The id of the associated connector
        :param job_type:
        :param trigger_method:
        """
        if id is None and body is None:
            raise ValueError("Empty value passed for parameter 'id'")
        __path_parts: t.Dict[str, str] = {}
        __path = "/_connector/_sync_job"
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
        if not __body:
            if id is not None:
                __body["id"] = id
            if job_type is not None:
                __body["job_type"] = job_type
            if trigger_method is not None:
                __body["trigger_method"] = trigger_method
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.sync_job_post",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    def update_active_filtering(
        self,
        *,
        connector_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Activates the valid draft filtering for a connector.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-filtering-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_filtering/_activate'
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
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="connector.update_active_filtering",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("api_key_id", "api_key_secret_id"),
    )
    def update_api_key_id(
        self,
        *,
        connector_id: str,
        api_key_id: t.Optional[str] = None,
        api_key_secret_id: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the API key id in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-api-key-id-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param api_key_id:
        :param api_key_secret_id:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_api_key_id'
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
        if not __body:
            if api_key_id is not None:
                __body["api_key_id"] = api_key_id
            if api_key_secret_id is not None:
                __body["api_key_secret_id"] = api_key_secret_id
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_api_key_id",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("configuration", "values"),
    )
    def update_configuration(
        self,
        *,
        connector_id: str,
        configuration: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        values: t.Optional[t.Mapping[str, t.Any]] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the configuration field in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-configuration-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param configuration:
        :param values:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_configuration'
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
        if not __body:
            if configuration is not None:
                __body["configuration"] = configuration
            if values is not None:
                __body["values"] = values
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_configuration",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("error",),
    )
    def update_error(
        self,
        *,
        connector_id: str,
        error: t.Optional[t.Union[None, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the filtering field in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-error-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param error:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if error is None and body is None:
            raise ValueError("Empty value passed for parameter 'error'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_error'
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
        if not __body:
            if error is not None:
                __body["error"] = error
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_error",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("advanced_snippet", "filtering", "rules"),
    )
    def update_filtering(
        self,
        *,
        connector_id: str,
        advanced_snippet: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        filtering: t.Optional[t.Sequence[t.Mapping[str, t.Any]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        rules: t.Optional[t.Sequence[t.Mapping[str, t.Any]]] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the filtering field in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-filtering-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param advanced_snippet:
        :param filtering:
        :param rules:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_filtering'
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
        if not __body:
            if advanced_snippet is not None:
                __body["advanced_snippet"] = advanced_snippet
            if filtering is not None:
                __body["filtering"] = filtering
            if rules is not None:
                __body["rules"] = rules
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_filtering",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("validation",),
    )
    def update_filtering_validation(
        self,
        *,
        connector_id: str,
        validation: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the draft filtering validation info for a connector.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-filtering-validation-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param validation:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if validation is None and body is None:
            raise ValueError("Empty value passed for parameter 'validation'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_filtering/_validation'
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
        if not __body:
            if validation is not None:
                __body["validation"] = validation
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_filtering_validation",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("index_name",),
    )
    def update_index_name(
        self,
        *,
        connector_id: str,
        index_name: t.Optional[t.Union[None, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the index_name in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-index-name-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param index_name:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if index_name is None and body is None:
            raise ValueError("Empty value passed for parameter 'index_name'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_index_name'
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
        if not __body:
            if index_name is not None:
                __body["index_name"] = index_name
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_index_name",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("description", "name"),
    )
    def update_name(
        self,
        *,
        connector_id: str,
        description: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        name: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the name and description fields in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-name-description-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param description:
        :param name:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_name'
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
        if not __body:
            if description is not None:
                __body["description"] = description
            if name is not None:
                __body["name"] = name
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_name",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("is_native",),
    )
    def update_native(
        self,
        *,
        connector_id: str,
        is_native: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the is_native flag in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-native-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param is_native:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if is_native is None and body is None:
            raise ValueError("Empty value passed for parameter 'is_native'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_native'
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
        if not __body:
            if is_native is not None:
                __body["is_native"] = is_native
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_native",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("pipeline",),
    )
    def update_pipeline(
        self,
        *,
        connector_id: str,
        pipeline: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the pipeline field in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-pipeline-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param pipeline:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if pipeline is None and body is None:
            raise ValueError("Empty value passed for parameter 'pipeline'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_pipeline'
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
        if not __body:
            if pipeline is not None:
                __body["pipeline"] = pipeline
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_pipeline",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("scheduling",),
    )
    def update_scheduling(
        self,
        *,
        connector_id: str,
        scheduling: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the scheduling field in the connector document

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-scheduling-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param scheduling:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if scheduling is None and body is None:
            raise ValueError("Empty value passed for parameter 'scheduling'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_scheduling'
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
        if not __body:
            if scheduling is not None:
                __body["scheduling"] = scheduling
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_scheduling",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("service_type",),
    )
    def update_service_type(
        self,
        *,
        connector_id: str,
        service_type: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the service type of the connector

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-service-type-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param service_type:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if service_type is None and body is None:
            raise ValueError("Empty value passed for parameter 'service_type'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_service_type'
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
        if not __body:
            if service_type is not None:
                __body["service_type"] = service_type
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_service_type",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=("status",),
    )
    def update_status(
        self,
        *,
        connector_id: str,
        status: t.Optional[
            t.Union[
                str,
                t.Literal[
                    "configured", "connected", "created", "error", "needs_configuration"
                ],
            ]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the status of the connector

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.15/update-connector-status-api.html>`_

        :param connector_id: The unique identifier of the connector to be updated
        :param status:
        """
        if connector_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'connector_id'")
        if status is None and body is None:
            raise ValueError("Empty value passed for parameter 'status'")
        __path_parts: t.Dict[str, str] = {"connector_id": _quote(connector_id)}
        __path = f'/_connector/{__path_parts["connector_id"]}/_status'
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
        if not __body:
            if status is not None:
                __body["status"] = status
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="connector.update_status",
            path_parts=__path_parts,
        )

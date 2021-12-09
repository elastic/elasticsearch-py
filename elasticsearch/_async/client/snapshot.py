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


class SnapshotClient(NamespacedClient):
    @_rewrite_parameters()
    async def cleanup_repository(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes stale data from repository.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/clean-up-snapshot-repo-api.html>`_

        :param name: Snapshot repository to clean up.
        :param master_timeout: Period to wait for a connection to the master node.
        :param timeout: Period to wait for a response.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_snapshot/{_quote(name)}/_cleanup"
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def clone(
        self,
        *,
        repository: Any,
        snapshot: Any,
        target_snapshot: Any,
        indices: str,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Clones indices from one snapshot into another snapshot in the same repository.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param repository: A repository name
        :param snapshot: The name of the snapshot to clone from
        :param target_snapshot: The name of the cloned snapshot to create
        :param indices:
        :param master_timeout: Explicit operation timeout for connection to master node
        :param timeout:
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'repository'")
        if snapshot in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'snapshot'")
        if target_snapshot in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'target_snapshot'")
        if indices is None:
            raise ValueError("Empty value passed for parameter 'indices'")
        __path = f"/_snapshot/{_quote(repository)}/{_quote(snapshot)}/_clone/{_quote(target_snapshot)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if indices is not None:
            __body["indices"] = indices
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def create(
        self,
        *,
        repository: Any,
        snapshot: Any,
        error_trace: Optional[bool] = None,
        feature_states: Optional[List[str]] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_unavailable: Optional[bool] = None,
        include_global_state: Optional[bool] = None,
        indices: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        metadata: Optional[Any] = None,
        partial: Optional[bool] = None,
        pretty: Optional[bool] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a snapshot in a repository.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param repository: Repository for the snapshot.
        :param snapshot: Name of the snapshot. Must be unique in the repository.
        :param feature_states: Feature states to include in the snapshot. Each feature
            state includes one or more system indices containing related data. You can
            view a list of eligible features using the get features API. If `include_global_state`
            is `true`, all current feature states are included by default. If `include_global_state`
            is `false`, no feature states are included by default.
        :param ignore_unavailable: If `true`, the request ignores data streams and indices
            in `indices` that are missing or closed. If `false`, the request returns
            an error for any data stream or index that is missing or closed.
        :param include_global_state: If `true`, the current cluster state is included
            in the snapshot. The cluster state includes persistent cluster settings,
            composable index templates, legacy index templates, ingest pipelines, and
            ILM policies. It also includes data stored in system indices, such as Watches
            and task records (configurable via `feature_states`).
        :param indices: Data streams and indices to include in the snapshot. Supports
            multi-target syntax. Includes all data streams and indices by default.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param metadata: Optional metadata for the snapshot. May have any contents. Must
            be less than 1024 bytes. This map is not automatically generated by Elasticsearch.
        :param partial: If `true`, allows restoring a partial snapshot of indices with
            unavailable shards. Only shards that were successfully included in the snapshot
            will be restored. All missing shards will be recreated as empty. If `false`,
            the entire restore operation will fail if one or more indices included in
            the snapshot do not have all primary shards available.
        :param wait_for_completion: If `true`, the request returns a response when the
            snapshot is complete. If `false`, the request returns a response when the
            snapshot initializes.
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'repository'")
        if snapshot in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'snapshot'")
        __path = f"/_snapshot/{_quote(repository)}/{_quote(snapshot)}"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if feature_states is not None:
            __body["feature_states"] = feature_states
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __body["ignore_unavailable"] = ignore_unavailable
        if include_global_state is not None:
            __body["include_global_state"] = include_global_state
        if indices is not None:
            __body["indices"] = indices
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if metadata is not None:
            __body["metadata"] = metadata
        if partial is not None:
            __body["partial"] = partial
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        if not __body:
            __body = None  # type: ignore[assignment]
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def create_repository(
        self,
        *,
        name: Any,
        settings: Any,
        type: str,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        repository: Optional[Any] = None,
        timeout: Optional[Any] = None,
        verify: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a repository.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param name: A repository name
        :param settings:
        :param type:
        :param master_timeout: Explicit operation timeout for connection to master node
        :param repository:
        :param timeout: Explicit operation timeout
        :param verify: Whether to verify the repository after creation
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        if settings is None:
            raise ValueError("Empty value passed for parameter 'settings'")
        if type is None:
            raise ValueError("Empty value passed for parameter 'type'")
        __path = f"/_snapshot/{_quote(name)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if settings is not None:
            __body["settings"] = settings
        if type is not None:
            __body["type"] = type
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
        if repository is not None:
            __body["repository"] = repository
        if timeout is not None:
            __query["timeout"] = timeout
        if verify is not None:
            __query["verify"] = verify
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def delete(
        self,
        *,
        repository: Any,
        snapshot: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes one or more snapshots.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param repository: A repository name
        :param snapshot: A comma-separated list of snapshot names
        :param master_timeout: Explicit operation timeout for connection to master node
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'repository'")
        if snapshot in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'snapshot'")
        __path = f"/_snapshot/{_quote(repository)}/{_quote(snapshot)}"
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def delete_repository(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes a repository.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param name: Name of the snapshot repository to unregister. Wildcard (`*`) patterns
            are supported.
        :param master_timeout: Explicit operation timeout for connection to master node
        :param timeout: Explicit operation timeout
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_snapshot/{_quote(name)}"
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get(
        self,
        *,
        repository: Any,
        snapshot: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_unavailable: Optional[bool] = None,
        include_repository: Optional[bool] = None,
        index_details: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        verbose: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns information about a snapshot.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param repository: Comma-separated list of snapshot repository names used to
            limit the request. Wildcard (*) expressions are supported.
        :param snapshot: Comma-separated list of snapshot names to retrieve. Also accepts
            wildcards (*). - To get information about all snapshots in a registered repository,
            use a wildcard (*) or _all. - To get information about any snapshots that
            are currently running, use _current.
        :param ignore_unavailable: If false, the request returns an error for any snapshots
            that are unavailable.
        :param include_repository: Whether to include the repository name in the snapshot
            info. Defaults to true.
        :param index_details: If true, returns additional information about each index
            in the snapshot comprising the number of shards in the index, the total size
            of the index in bytes, and the maximum number of segments per shard in the
            index. Defaults to false, meaning that this information is omitted.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param verbose: If true, returns additional information about each snapshot such
            as the version of Elasticsearch which took the snapshot, the start and end
            times of the snapshot, and the number of shards snapshotted.
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'repository'")
        if snapshot in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'snapshot'")
        __path = f"/_snapshot/{_quote(repository)}/{_quote(snapshot)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if include_repository is not None:
            __query["include_repository"] = include_repository
        if index_details is not None:
            __query["index_details"] = index_details
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if verbose is not None:
            __query["verbose"] = verbose
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_repository(
        self,
        *,
        name: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        local: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns information about a repository.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param name: A comma-separated list of repository names
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Explicit operation timeout for connection to master node
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_snapshot/{_quote(name)}"
        else:
            __path = "/_snapshot"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if local is not None:
            __query["local"] = local
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    async def restore(
        self,
        *,
        repository: Any,
        snapshot: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_index_settings: Optional[List[str]] = None,
        ignore_unavailable: Optional[bool] = None,
        include_aliases: Optional[bool] = None,
        include_global_state: Optional[bool] = None,
        index_settings: Optional[Any] = None,
        indices: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        partial: Optional[bool] = None,
        pretty: Optional[bool] = None,
        rename_pattern: Optional[str] = None,
        rename_replacement: Optional[str] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Restores a snapshot.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param repository: A repository name
        :param snapshot: A snapshot name
        :param ignore_index_settings:
        :param ignore_unavailable:
        :param include_aliases:
        :param include_global_state:
        :param index_settings:
        :param indices:
        :param master_timeout: Explicit operation timeout for connection to master node
        :param partial:
        :param rename_pattern:
        :param rename_replacement:
        :param wait_for_completion: Should this request wait until the operation has
            completed before returning
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'repository'")
        if snapshot in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'snapshot'")
        __path = f"/_snapshot/{_quote(repository)}/{_quote(snapshot)}/_restore"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_index_settings is not None:
            __body["ignore_index_settings"] = ignore_index_settings
        if ignore_unavailable is not None:
            __body["ignore_unavailable"] = ignore_unavailable
        if include_aliases is not None:
            __body["include_aliases"] = include_aliases
        if include_global_state is not None:
            __body["include_global_state"] = include_global_state
        if index_settings is not None:
            __body["index_settings"] = index_settings
        if indices is not None:
            __body["indices"] = indices
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if partial is not None:
            __body["partial"] = partial
        if pretty is not None:
            __query["pretty"] = pretty
        if rename_pattern is not None:
            __body["rename_pattern"] = rename_pattern
        if rename_replacement is not None:
            __body["rename_replacement"] = rename_replacement
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        if not __body:
            __body = None  # type: ignore[assignment]
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return await self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def status(
        self,
        *,
        repository: Optional[Any] = None,
        snapshot: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_unavailable: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns information about the status of a snapshot.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param repository: A repository name
        :param snapshot: A comma-separated list of snapshot names
        :param ignore_unavailable: Whether to ignore unavailable snapshots, defaults
            to false which means a SnapshotMissingException is thrown
        :param master_timeout: Explicit operation timeout for connection to master node
        """
        if repository not in SKIP_IN_PATH and snapshot not in SKIP_IN_PATH:
            __path = f"/_snapshot/{_quote(repository)}/{_quote(snapshot)}/_status"
        elif repository not in SKIP_IN_PATH:
            __path = f"/_snapshot/{_quote(repository)}/_status"
        else:
            __path = "/_snapshot/_status"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def verify_repository(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Verifies a repository.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :param name: A repository name
        :param master_timeout: Explicit operation timeout for connection to master node
        :param timeout: Explicit operation timeout
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_snapshot/{_quote(name)}/_verify"
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

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


class SearchableSnapshotsClient(NamespacedClient):
    @_rewrite_parameters()
    def clear_cache(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        expand_wildcards: Optional[Any] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_unavailable: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Clear the cache of searchable snapshots.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/searchable-snapshots-apis.html>`_

        :param index: A comma-separated list of index names
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_searchable_snapshots/cache/clear"
        else:
            __path = "/_searchable_snapshots/cache/clear"
        __query: Dict[str, Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def mount(
        self,
        *,
        repository: Any,
        snapshot: Any,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_index_settings: Optional[List[str]] = None,
        index_settings: Optional[Dict[str, Any]] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        renamed_index: Optional[Any] = None,
        storage: Optional[str] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Mount a snapshot as a searchable index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/searchable-snapshots-api-mount-snapshot.html>`_

        :param repository: The name of the repository containing the snapshot of the
            index to mount
        :param snapshot: The name of the snapshot of the index to mount
        :param index:
        :param ignore_index_settings:
        :param index_settings:
        :param master_timeout: Explicit operation timeout for connection to master node
        :param renamed_index:
        :param storage: Selects the kind of local storage used to accelerate searches.
            Experimental, and defaults to `full_copy`
        :param wait_for_completion: Should this request wait until the operation has
            completed before returning
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'repository'")
        if snapshot in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'snapshot'")
        if index is None:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/_snapshot/{_quote(repository)}/{_quote(snapshot)}/_mount"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if index is not None:
            __body["index"] = index
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_index_settings is not None:
            __body["ignore_index_settings"] = ignore_index_settings
        if index_settings is not None:
            __body["index_settings"] = index_settings
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if renamed_index is not None:
            __body["renamed_index"] = renamed_index
        if storage is not None:
            __query["storage"] = storage
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def stats(
        self,
        *,
        index: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        level: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieve shard-level statistics about searchable snapshots.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/searchable-snapshots-apis.html>`_

        :param index: A comma-separated list of index names
        :param level: Return stats aggregated at cluster, index or shard level
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_searchable_snapshots/stats"
        else:
            __path = "/_searchable_snapshots/stats"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if level is not None:
            __query["level"] = level
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

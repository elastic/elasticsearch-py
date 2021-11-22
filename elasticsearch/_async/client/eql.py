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


class EqlClient(NamespacedClient):
    @_rewrite_parameters()
    async def delete(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes an async EQL search by ID. If the search is still running, the search
        request will be cancelled. Otherwise, the saved search results are deleted.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/eql-search-api.html>`_

        :param id: Identifier for the search to delete.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_eql/search/{_quote(id)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
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
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        keep_alive: Optional[Any] = None,
        pretty: Optional[bool] = None,
        wait_for_completion_timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns async results from previously executed Event Query Language (EQL) search

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/eql-search-api.html>`_

        :param id: Identifier for the search.
        :param keep_alive: Period for which the search and its results are stored on
            the cluster. Defaults to the keep_alive value set by the search’s EQL search
            API request.
        :param wait_for_completion_timeout: Timeout duration to wait for the request
            to finish. Defaults to no timeout, meaning the request waits for complete
            search results.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_eql/search/{_quote(id)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if keep_alive is not None:
            __query["keep_alive"] = keep_alive
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_for_completion_timeout is not None:
            __query["wait_for_completion_timeout"] = wait_for_completion_timeout
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def get_status(
        self,
        *,
        id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns the status of a previously submitted async or stored Event Query Language
        (EQL) search

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/eql-search-api.html>`_

        :param id: Identifier for the search.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path = f"/_eql/search/status/{_quote(id)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
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
    async def search(
        self,
        *,
        index: Any,
        query: str,
        allow_no_indices: Optional[bool] = None,
        case_sensitive: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        event_category_field: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        fetch_size: Optional[int] = None,
        fields: Optional[Any] = None,
        filter: Optional[Union[Any, List[Any]]] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        ignore_unavailable: Optional[bool] = None,
        keep_alive: Optional[Any] = None,
        keep_on_completion: Optional[bool] = None,
        pretty: Optional[bool] = None,
        result_position: Optional[Any] = None,
        size: Optional[int] = None,
        tiebreaker_field: Optional[Any] = None,
        timestamp_field: Optional[Any] = None,
        wait_for_completion_timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns results matching a query expressed in Event Query Language (EQL)

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/eql-search-api.html>`_

        :param index: The name of the index to scope the operation
        :param query: EQL query you wish to run.
        :param allow_no_indices:
        :param case_sensitive:
        :param event_category_field: Field containing the event classification, such
            as process, file, or network.
        :param expand_wildcards:
        :param fetch_size: Maximum number of events to search at a time for sequence
            queries.
        :param fields: Array of wildcard (*) patterns. The response returns values for
            field names matching these patterns in the fields property of each hit.
        :param filter: Query, written in Query DSL, used to filter the events on which
            the EQL query runs.
        :param ignore_unavailable: If true, missing or closed indices are not included
            in the response.
        :param keep_alive:
        :param keep_on_completion:
        :param result_position:
        :param size: For basic queries, the maximum number of matching events to return.
            Defaults to 10
        :param tiebreaker_field: Field used to sort hits with the same timestamp in ascending
            order
        :param timestamp_field: Field containing event timestamp. Default "@timestamp"
        :param wait_for_completion_timeout:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if query is None:
            raise ValueError("Empty value passed for parameter 'query'")
        __path = f"/{_quote(index)}/_eql/search"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if query is not None:
            __body["query"] = query
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if case_sensitive is not None:
            __body["case_sensitive"] = case_sensitive
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if event_category_field is not None:
            __body["event_category_field"] = event_category_field
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if fetch_size is not None:
            __body["fetch_size"] = fetch_size
        if fields is not None:
            __body["fields"] = fields
        if filter is not None:
            __body["filter"] = filter
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if keep_alive is not None:
            __body["keep_alive"] = keep_alive
        if keep_on_completion is not None:
            __body["keep_on_completion"] = keep_on_completion
        if pretty is not None:
            __query["pretty"] = pretty
        if result_position is not None:
            __body["result_position"] = result_position
        if size is not None:
            __body["size"] = size
        if tiebreaker_field is not None:
            __body["tiebreaker_field"] = tiebreaker_field
        if timestamp_field is not None:
            __body["timestamp_field"] = timestamp_field
        if wait_for_completion_timeout is not None:
            __body["wait_for_completion_timeout"] = wait_for_completion_timeout
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

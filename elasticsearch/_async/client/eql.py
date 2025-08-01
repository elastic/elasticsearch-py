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


class EqlClient(NamespacedClient):

    @_rewrite_parameters()
    async def delete(
        self,
        *,
        id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Delete an async EQL search.
          Delete an async EQL search or a stored synchronous EQL search.
          The API also deletes results for the search.</p>


        `<https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-delete>`_

        :param id: Identifier for the search to delete. A search ID is provided in the
            EQL search API's response for an async search. A search ID is also provided
            if the request’s `keep_on_completion` parameter is `true`.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path_parts: t.Dict[str, str] = {"id": _quote(id)}
        __path = f'/_eql/search/{__path_parts["id"]}'
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
            "DELETE",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="eql.delete",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def get(
        self,
        *,
        id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        keep_alive: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        wait_for_completion_timeout: t.Optional[
            t.Union[str, t.Literal[-1], t.Literal[0]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get async EQL search results.
          Get the current status and available results for an async EQL search or a stored synchronous EQL search.</p>


        `<https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-get>`_

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
        __path_parts: t.Dict[str, str] = {"id": _quote(id)}
        __path = f'/_eql/search/{__path_parts["id"]}'
        __query: t.Dict[str, t.Any] = {}
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
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="eql.get",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    async def get_status(
        self,
        *,
        id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get the async EQL status.
          Get the current status for an async EQL search or a stored synchronous EQL search without returning results.</p>


        `<https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-get-status>`_

        :param id: Identifier for the search.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'id'")
        __path_parts: t.Dict[str, str] = {"id": _quote(id)}
        __path = f'/_eql/search/status/{__path_parts["id"]}'
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
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="eql.get_status",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=(
            "query",
            "allow_partial_search_results",
            "allow_partial_sequence_results",
            "case_sensitive",
            "event_category_field",
            "fetch_size",
            "fields",
            "filter",
            "keep_alive",
            "keep_on_completion",
            "max_samples_per_key",
            "result_position",
            "runtime_mappings",
            "size",
            "tiebreaker_field",
            "timestamp_field",
            "wait_for_completion_timeout",
        ),
    )
    async def search(
        self,
        *,
        index: t.Union[str, t.Sequence[str]],
        query: t.Optional[str] = None,
        allow_no_indices: t.Optional[bool] = None,
        allow_partial_search_results: t.Optional[bool] = None,
        allow_partial_sequence_results: t.Optional[bool] = None,
        case_sensitive: t.Optional[bool] = None,
        ccs_minimize_roundtrips: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        event_category_field: t.Optional[str] = None,
        expand_wildcards: t.Optional[
            t.Union[
                t.Sequence[
                    t.Union[str, t.Literal["all", "closed", "hidden", "none", "open"]]
                ],
                t.Union[str, t.Literal["all", "closed", "hidden", "none", "open"]],
            ]
        ] = None,
        fetch_size: t.Optional[int] = None,
        fields: t.Optional[
            t.Union[t.Mapping[str, t.Any], t.Sequence[t.Mapping[str, t.Any]]]
        ] = None,
        filter: t.Optional[
            t.Union[t.Mapping[str, t.Any], t.Sequence[t.Mapping[str, t.Any]]]
        ] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        keep_alive: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        keep_on_completion: t.Optional[bool] = None,
        max_samples_per_key: t.Optional[int] = None,
        pretty: t.Optional[bool] = None,
        result_position: t.Optional[t.Union[str, t.Literal["head", "tail"]]] = None,
        runtime_mappings: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        size: t.Optional[int] = None,
        tiebreaker_field: t.Optional[str] = None,
        timestamp_field: t.Optional[str] = None,
        wait_for_completion_timeout: t.Optional[
            t.Union[str, t.Literal[-1], t.Literal[0]]
        ] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get EQL search results.
          Returns search results for an Event Query Language (EQL) query.
          EQL assumes each document in a data stream or index corresponds to an event.</p>


        `<https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search>`_

        :param index: The name of the index to scope the operation
        :param query: EQL query you wish to run.
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param allow_partial_search_results: Allow query execution also in case of shard
            failures. If true, the query will keep running and will return results based
            on the available shards. For sequences, the behavior can be further refined
            using allow_partial_sequence_results
        :param allow_partial_sequence_results: This flag applies only to sequences and
            has effect only if allow_partial_search_results=true. If true, the sequence
            query will return results based on the available shards, ignoring the others.
            If false, the sequence query will return successfully, but will always have
            empty results.
        :param case_sensitive:
        :param ccs_minimize_roundtrips: Indicates whether network round-trips should
            be minimized as part of cross-cluster search requests execution
        :param event_category_field: Field containing the event classification, such
            as process, file, or network.
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
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
        :param max_samples_per_key: By default, the response of a sample query contains
            up to `10` samples, with one sample per unique set of join keys. Use the
            `size` parameter to get a smaller or larger set of samples. To retrieve more
            than one sample per set of join keys, use the `max_samples_per_key` parameter.
            Pipes are not supported for sample queries.
        :param result_position:
        :param runtime_mappings:
        :param size: For basic queries, the maximum number of matching events to return.
            Defaults to 10
        :param tiebreaker_field: Field used to sort hits with the same timestamp in ascending
            order
        :param timestamp_field: Field containing event timestamp. Default "@timestamp"
        :param wait_for_completion_timeout:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if query is None and body is None:
            raise ValueError("Empty value passed for parameter 'query'")
        __path_parts: t.Dict[str, str] = {"index": _quote(index)}
        __path = f'/{__path_parts["index"]}/_eql/search'
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = body if body is not None else {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if ccs_minimize_roundtrips is not None:
            __query["ccs_minimize_roundtrips"] = ccs_minimize_roundtrips
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
        if not __body:
            if query is not None:
                __body["query"] = query
            if allow_partial_search_results is not None:
                __body["allow_partial_search_results"] = allow_partial_search_results
            if allow_partial_sequence_results is not None:
                __body["allow_partial_sequence_results"] = (
                    allow_partial_sequence_results
                )
            if case_sensitive is not None:
                __body["case_sensitive"] = case_sensitive
            if event_category_field is not None:
                __body["event_category_field"] = event_category_field
            if fetch_size is not None:
                __body["fetch_size"] = fetch_size
            if fields is not None:
                __body["fields"] = fields
            if filter is not None:
                __body["filter"] = filter
            if keep_alive is not None:
                __body["keep_alive"] = keep_alive
            if keep_on_completion is not None:
                __body["keep_on_completion"] = keep_on_completion
            if max_samples_per_key is not None:
                __body["max_samples_per_key"] = max_samples_per_key
            if result_position is not None:
                __body["result_position"] = result_position
            if runtime_mappings is not None:
                __body["runtime_mappings"] = runtime_mappings
            if size is not None:
                __body["size"] = size
            if tiebreaker_field is not None:
                __body["tiebreaker_field"] = tiebreaker_field
            if timestamp_field is not None:
                __body["timestamp_field"] = timestamp_field
            if wait_for_completion_timeout is not None:
                __body["wait_for_completion_timeout"] = wait_for_completion_timeout
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="eql.search",
            path_parts=__path_parts,
        )

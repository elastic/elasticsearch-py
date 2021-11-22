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


class CcrClient(NamespacedClient):
    @_rewrite_parameters()
    def delete_auto_follow_pattern(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes auto-follow patterns.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-delete-auto-follow-pattern.html>`_

        :param name: The name of the auto follow pattern.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_ccr/auto_follow/{_quote(name)}"
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
        return self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def follow(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        leader_index: Optional[Any] = None,
        max_outstanding_read_requests: Optional[int] = None,
        max_outstanding_write_requests: Optional[int] = None,
        max_read_request_operation_count: Optional[int] = None,
        max_read_request_size: Optional[str] = None,
        max_retry_delay: Optional[Any] = None,
        max_write_buffer_count: Optional[int] = None,
        max_write_buffer_size: Optional[str] = None,
        max_write_request_operation_count: Optional[int] = None,
        max_write_request_size: Optional[str] = None,
        pretty: Optional[bool] = None,
        read_poll_timeout: Optional[Any] = None,
        remote_cluster: Optional[str] = None,
        wait_for_active_shards: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a new follower index configured to follow the referenced leader index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-put-follow.html>`_

        :param index: The name of the follower index
        :param leader_index:
        :param max_outstanding_read_requests:
        :param max_outstanding_write_requests:
        :param max_read_request_operation_count:
        :param max_read_request_size:
        :param max_retry_delay:
        :param max_write_buffer_count:
        :param max_write_buffer_size:
        :param max_write_request_operation_count:
        :param max_write_request_size:
        :param read_poll_timeout:
        :param remote_cluster:
        :param wait_for_active_shards: Sets the number of shard copies that must be active
            before returning. Defaults to 0. Set to `all` for all shard copies, otherwise
            set to any non-negative value less than or equal to the total number of copies
            for the shard (number of replicas + 1)
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ccr/follow"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if leader_index is not None:
            __body["leader_index"] = leader_index
        if max_outstanding_read_requests is not None:
            __body["max_outstanding_read_requests"] = max_outstanding_read_requests
        if max_outstanding_write_requests is not None:
            __body["max_outstanding_write_requests"] = max_outstanding_write_requests
        if max_read_request_operation_count is not None:
            __body[
                "max_read_request_operation_count"
            ] = max_read_request_operation_count
        if max_read_request_size is not None:
            __body["max_read_request_size"] = max_read_request_size
        if max_retry_delay is not None:
            __body["max_retry_delay"] = max_retry_delay
        if max_write_buffer_count is not None:
            __body["max_write_buffer_count"] = max_write_buffer_count
        if max_write_buffer_size is not None:
            __body["max_write_buffer_size"] = max_write_buffer_size
        if max_write_request_operation_count is not None:
            __body[
                "max_write_request_operation_count"
            ] = max_write_request_operation_count
        if max_write_request_size is not None:
            __body["max_write_request_size"] = max_write_request_size
        if pretty is not None:
            __query["pretty"] = pretty
        if read_poll_timeout is not None:
            __body["read_poll_timeout"] = read_poll_timeout
        if remote_cluster is not None:
            __body["remote_cluster"] = remote_cluster
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def follow_info(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information about all follower indices, including parameters and status
        for each follower index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-follow-info.html>`_

        :param index: A comma-separated list of index patterns; use `_all` to perform
            the operation on all indices
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ccr/info"
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
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def follow_stats(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves follower stats. return shard-level stats about the following tasks
        associated with each shard for the specified indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-follow-stats.html>`_

        :param index: A comma-separated list of index patterns; use `_all` to perform
            the operation on all indices
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ccr/stats"
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
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def forget_follower(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        follower_cluster: Optional[str] = None,
        follower_index: Optional[Any] = None,
        follower_index_uuid: Optional[Any] = None,
        human: Optional[bool] = None,
        leader_remote_cluster: Optional[str] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes the follower retention leases from the leader.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-forget-follower.html>`_

        :param index: the name of the leader index for which specified follower retention
            leases should be removed
        :param follower_cluster:
        :param follower_index:
        :param follower_index_uuid:
        :param leader_remote_cluster:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ccr/forget_follower"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if follower_cluster is not None:
            __body["follower_cluster"] = follower_cluster
        if follower_index is not None:
            __body["follower_index"] = follower_index
        if follower_index_uuid is not None:
            __body["follower_index_uuid"] = follower_index_uuid
        if human is not None:
            __query["human"] = human
        if leader_remote_cluster is not None:
            __body["leader_remote_cluster"] = leader_remote_cluster
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def get_auto_follow_pattern(
        self,
        *,
        name: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Gets configured auto-follow patterns. Returns the specified auto-follow pattern
        collection.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-auto-follow-pattern.html>`_

        :param name: Specifies the auto-follow pattern collection that you want to retrieve.
            If you do not specify a name, the API returns information for all collections.
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_ccr/auto_follow/{_quote(name)}"
        else:
            __path = "/_ccr/auto_follow"
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
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def pause_auto_follow_pattern(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Pauses an auto-follow pattern

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-pause-auto-follow-pattern.html>`_

        :param name: The name of the auto follow pattern that should pause discovering
            new indices to follow.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_ccr/auto_follow/{_quote(name)}/pause"
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def pause_follow(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Pauses a follower index. The follower index will not fetch any additional operations
        from the leader index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-pause-follow.html>`_

        :param index: The name of the follower index that should pause following its
            leader index.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ccr/pause_follow"
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_auto_follow_pattern(
        self,
        *,
        name: Any,
        remote_cluster: str,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        follow_index_pattern: Optional[Any] = None,
        human: Optional[bool] = None,
        leader_index_exclusion_patterns: Optional[Any] = None,
        leader_index_patterns: Optional[Any] = None,
        max_outstanding_read_requests: Optional[int] = None,
        max_outstanding_write_requests: Optional[int] = None,
        max_read_request_operation_count: Optional[int] = None,
        max_read_request_size: Optional[Any] = None,
        max_retry_delay: Optional[Any] = None,
        max_write_buffer_count: Optional[int] = None,
        max_write_buffer_size: Optional[Any] = None,
        max_write_request_operation_count: Optional[int] = None,
        max_write_request_size: Optional[Any] = None,
        pretty: Optional[bool] = None,
        read_poll_timeout: Optional[Any] = None,
        settings: Optional[Dict[str, Any]] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a new named collection of auto-follow patterns against a specified remote
        cluster. Newly created indices on the remote cluster matching any of the specified
        patterns will be automatically configured as follower indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-put-auto-follow-pattern.html>`_

        :param name: The name of the collection of auto-follow patterns.
        :param remote_cluster: The remote cluster containing the leader indices to match
            against.
        :param follow_index_pattern: The name of follower index. The template {{leader_index}}
            can be used to derive the name of the follower index from the name of the
            leader index. When following a data stream, use {{leader_index}}; CCR does
            not support changes to the names of a follower data stream’s backing indices.
        :param leader_index_exclusion_patterns: An array of simple index patterns that
            can be used to exclude indices from being auto-followed. Indices in the remote
            cluster whose names are matching one or more leader_index_patterns and one
            or more leader_index_exclusion_patterns won’t be followed.
        :param leader_index_patterns: An array of simple index patterns to match against
            indices in the remote cluster specified by the remote_cluster field.
        :param max_outstanding_read_requests: The maximum number of outstanding reads
            requests from the remote cluster.
        :param max_outstanding_write_requests: The maximum number of outstanding reads
            requests from the remote cluster.
        :param max_read_request_operation_count: The maximum number of operations to
            pull per read from the remote cluster.
        :param max_read_request_size: The maximum size in bytes of per read of a batch
            of operations pulled from the remote cluster.
        :param max_retry_delay: The maximum time to wait before retrying an operation
            that failed exceptionally. An exponential backoff strategy is employed when
            retrying.
        :param max_write_buffer_count: The maximum number of operations that can be queued
            for writing. When this limit is reached, reads from the remote cluster will
            be deferred until the number of queued operations goes below the limit.
        :param max_write_buffer_size: The maximum total bytes of operations that can
            be queued for writing. When this limit is reached, reads from the remote
            cluster will be deferred until the total bytes of queued operations goes
            below the limit.
        :param max_write_request_operation_count: The maximum number of operations per
            bulk write request executed on the follower.
        :param max_write_request_size: The maximum total bytes of operations per bulk
            write request executed on the follower.
        :param read_poll_timeout: The maximum time to wait for new operations on the
            remote cluster when the follower index is synchronized with the leader index.
            When the timeout has elapsed, the poll for operations will return to the
            follower so that it can update some statistics. Then the follower will immediately
            attempt to read from the leader again.
        :param settings: Settings to override from the leader index. Note that certain
            settings can not be overrode (e.g., index.number_of_shards).
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        if remote_cluster is None:
            raise ValueError("Empty value passed for parameter 'remote_cluster'")
        __path = f"/_ccr/auto_follow/{_quote(name)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if remote_cluster is not None:
            __body["remote_cluster"] = remote_cluster
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if follow_index_pattern is not None:
            __body["follow_index_pattern"] = follow_index_pattern
        if human is not None:
            __query["human"] = human
        if leader_index_exclusion_patterns is not None:
            __body["leader_index_exclusion_patterns"] = leader_index_exclusion_patterns
        if leader_index_patterns is not None:
            __body["leader_index_patterns"] = leader_index_patterns
        if max_outstanding_read_requests is not None:
            __body["max_outstanding_read_requests"] = max_outstanding_read_requests
        if max_outstanding_write_requests is not None:
            __body["max_outstanding_write_requests"] = max_outstanding_write_requests
        if max_read_request_operation_count is not None:
            __body[
                "max_read_request_operation_count"
            ] = max_read_request_operation_count
        if max_read_request_size is not None:
            __body["max_read_request_size"] = max_read_request_size
        if max_retry_delay is not None:
            __body["max_retry_delay"] = max_retry_delay
        if max_write_buffer_count is not None:
            __body["max_write_buffer_count"] = max_write_buffer_count
        if max_write_buffer_size is not None:
            __body["max_write_buffer_size"] = max_write_buffer_size
        if max_write_request_operation_count is not None:
            __body[
                "max_write_request_operation_count"
            ] = max_write_request_operation_count
        if max_write_request_size is not None:
            __body["max_write_request_size"] = max_write_request_size
        if pretty is not None:
            __query["pretty"] = pretty
        if read_poll_timeout is not None:
            __body["read_poll_timeout"] = read_poll_timeout
        if settings is not None:
            __body["settings"] = settings
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def resume_auto_follow_pattern(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Resumes an auto-follow pattern that has been paused

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-resume-auto-follow-pattern.html>`_

        :param name: The name of the auto follow pattern to resume discovering new indices
            to follow.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_ccr/auto_follow/{_quote(name)}/resume"
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def resume_follow(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        max_outstanding_read_requests: Optional[int] = None,
        max_outstanding_write_requests: Optional[int] = None,
        max_read_request_operation_count: Optional[int] = None,
        max_read_request_size: Optional[str] = None,
        max_retry_delay: Optional[Any] = None,
        max_write_buffer_count: Optional[int] = None,
        max_write_buffer_size: Optional[str] = None,
        max_write_request_operation_count: Optional[int] = None,
        max_write_request_size: Optional[str] = None,
        pretty: Optional[bool] = None,
        read_poll_timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Resumes a follower index that has been paused

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-resume-follow.html>`_

        :param index: The name of the follow index to resume following.
        :param max_outstanding_read_requests:
        :param max_outstanding_write_requests:
        :param max_read_request_operation_count:
        :param max_read_request_size:
        :param max_retry_delay:
        :param max_write_buffer_count:
        :param max_write_buffer_size:
        :param max_write_request_operation_count:
        :param max_write_request_size:
        :param read_poll_timeout:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ccr/resume_follow"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if max_outstanding_read_requests is not None:
            __body["max_outstanding_read_requests"] = max_outstanding_read_requests
        if max_outstanding_write_requests is not None:
            __body["max_outstanding_write_requests"] = max_outstanding_write_requests
        if max_read_request_operation_count is not None:
            __body[
                "max_read_request_operation_count"
            ] = max_read_request_operation_count
        if max_read_request_size is not None:
            __body["max_read_request_size"] = max_read_request_size
        if max_retry_delay is not None:
            __body["max_retry_delay"] = max_retry_delay
        if max_write_buffer_count is not None:
            __body["max_write_buffer_count"] = max_write_buffer_count
        if max_write_buffer_size is not None:
            __body["max_write_buffer_size"] = max_write_buffer_size
        if max_write_request_operation_count is not None:
            __body[
                "max_write_request_operation_count"
            ] = max_write_request_operation_count
        if max_write_request_size is not None:
            __body["max_write_request_size"] = max_write_request_size
        if pretty is not None:
            __query["pretty"] = pretty
        if read_poll_timeout is not None:
            __body["read_poll_timeout"] = read_poll_timeout
        if not __body:
            __body = None  # type: ignore[assignment]
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def stats(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Gets all stats related to cross-cluster replication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-stats.html>`_
        """
        __path = "/_ccr/stats"
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
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def unfollow(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Stops the following task associated with a follower index and removes index metadata
        and settings associated with cross-cluster replication.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-unfollow.html>`_

        :param index: The name of the follower index that should be turned into a regular
            index.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ccr/unfollow"
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

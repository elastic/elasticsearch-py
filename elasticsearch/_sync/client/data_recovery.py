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


class C:

    @_rewrite_parameters()
    @_availability_warning(Stability.STABLE, Visibility.PRIVATE)
    def get_recovery(
        self,
        *,
        recovery_id: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get a recovery.</p>
          <p>Get the status and details of a recovery that was started with the start recovery API.
          This API is intended for internal operator use.
          The progress of a running recovery is reported as a percentage, and the repository and audit details of the recovery are not exposed.</p>


        :param recovery_id: The identifier of the recovery, as returned when the recovery
            was started.
        """
        if recovery_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'recovery_id'")
        __path_parts: t.Dict[str, str] = {"recovery_id": _quote(recovery_id)}
        __path = f'/_data_recovery/recoveries/{__path_parts["recovery_id"]}'
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
            endpoint_id="data_recovery.get_recovery",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_availability_warning(Stability.STABLE, Visibility.PRIVATE)
    def get_recovery_points(
        self,
        *,
        end_time_before: t.Optional[t.Union[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get recovery points.</p>
          <p>Get recovery points from the platform-managed data recovery repository.
          This API is intended for internal operator use.
          Recovery points are returned in descending order by end time. Repository,
          snapshot, and policy identifiers are not exposed.</p>


        :param end_time_before: Return only recovery points whose end time is earlier
            than this value. The boundary is exclusive and can be set to the last recovery
            point's end time to retrieve the next page.
        :param master_timeout: The period to wait for the master node. If the master
            node is not available before the timeout expires, the request fails and returns
            an error. To indicate that the request should never timeout, set it to `-1`.
        :param size: The maximum number of recovery points to return. The value must
            be between 1 and 1000.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_data_recovery/points"
        __query: t.Dict[str, t.Any] = {}
        if end_time_before is not None:
            __query["end_time_before"] = end_time_before
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
        if size is not None:
            __query["size"] = size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="data_recovery.get_recovery_points",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_availability_warning(Stability.STABLE, Visibility.PRIVATE)
    def get_recovery_sources(
        self,
        *,
        expression: t.Union[str, t.Sequence[str]],
        recovery_point_end_time: t.Union[str, t.Any],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        include_incomplete_sources: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        size: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get recovery sources.</p>
          <p>Get the logical sources captured at an exact recovery point in the platform-managed data recovery repository.
          This API is intended for internal operator use. Repository, snapshot, and policy identifiers are not exposed.</p>


        :param expression: A comma-separated list of source expressions to match. Wildcards
            and exclusions prefixed with `-` are supported.
        :param recovery_point_end_time: The exact end time of the recovery point.
        :param include_incomplete_sources: If `true`, include logical sources that were
            not completely captured in the recovery point.
        :param master_timeout: The period to wait for the master node. If the master
            node is not available before the timeout expires, the request fails and returns
            an error. To indicate that the request should never timeout, set it to `-1`.
        :param size: The maximum number of matching sources to return. The value must
            be between 1 and 1000.
        """
        if expression is None:
            raise ValueError("Empty value passed for parameter 'expression'")
        if recovery_point_end_time is None:
            raise ValueError(
                "Empty value passed for parameter 'recovery_point_end_time'"
            )
        __path_parts: t.Dict[str, str] = {}
        __path = "/_data_recovery/sources"
        __query: t.Dict[str, t.Any] = {}
        if expression is not None:
            __query["expression"] = expression
        if recovery_point_end_time is not None:
            __query["recovery_point_end_time"] = recovery_point_end_time
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if include_incomplete_sources is not None:
            __query["include_incomplete_sources"] = include_incomplete_sources
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if size is not None:
            __query["size"] = size
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="data_recovery.get_recovery_sources",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_availability_warning(Stability.STABLE, Visibility.PRIVATE)
    def get_rpo_series(
        self,
        *,
        bucket_duration: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        end: t.Optional[t.Union[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        start: t.Optional[t.Union[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get the recovery point objective series.</p>
          <p>Get, for each bucket in the half-open range <code>[start, end)</code>, the maximum age
          that the newest recoverable state reached during that bucket.
          This API is intended for internal operator use.
          The range is divided into at most 1,000 buckets. A bucket has no value if
          no retained recovery point covers its start.</p>


        :param bucket_duration: The duration of each bucket. It must be greater than
            zero, and the range must divide into at most 1,000 buckets.
        :param end: The exclusive end of the range, as a date or epoch milliseconds.
        :param master_timeout: The period to wait for the master node. If the master
            node is not available before the timeout expires, the request fails and returns
            an error. To indicate that the request should never timeout, set it to `-1`.
        :param start: The inclusive start of the range, as a date or epoch milliseconds.
            When omitted, it is seven days before `end`, rounded down to a whole multiple
            of `bucket_duration`, so that repeated requests with default parameters return
            the same bucket boundaries.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_data_recovery/rpo"
        __query: t.Dict[str, t.Any] = {}
        if bucket_duration is not None:
            __query["bucket_duration"] = bucket_duration
        if end is not None:
            __query["end"] = end
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
        if start is not None:
            __query["start"] = start
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="data_recovery.get_rpo_series",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_availability_warning(Stability.STABLE, Visibility.PRIVATE)
    def list_recoveries(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        order: t.Optional[t.Union[str, t.Literal["asc", "desc"]]] = None,
        pretty: t.Optional[bool] = None,
        search_after_recovery_id: t.Optional[str] = None,
        search_after_started_at: t.Optional[t.Union[str, t.Any]] = None,
        size: t.Optional[int] = None,
        started_at_gte: t.Optional[t.Union[str, t.Any]] = None,
        started_at_lt: t.Optional[t.Union[str, t.Any]] = None,
        status: t.Optional[
            t.Union[
                t.Sequence[t.Union[str, t.Literal["completed", "failed", "running"]]],
                t.Union[str, t.Literal["completed", "failed", "running"]],
            ]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>List recoveries.</p>
          <p>List the recoveries that were started with the start recovery API, including those that have finished.
          This API is intended for internal operator use.
          Recoveries are ordered by start time, and the most recent are returned first by default.
          To retrieve further pages, pass the start time and identifier of the last recovery of a page as <code>search_after_started_at</code> and <code>search_after_recovery_id</code>.</p>


        :param order: The order of the recoveries by start time.
        :param search_after_recovery_id: Return only recoveries after this identifier
            in the sort order for recoveries with the same start time, to retrieve the
            next page. It must be provided together with `search_after_started_at`.
        :param search_after_started_at: Return only recoveries after this start time
            in the sort order, to retrieve the next page. It must be provided together
            with `search_after_recovery_id`.
        :param size: The maximum number of recoveries to return. The value must be between
            1 and 1000.
        :param started_at_gte: Return only recoveries that started at or after this time,
            as an ISO-8601 timestamp.
        :param started_at_lt: Return only recoveries that started before this time, as
            an ISO-8601 timestamp. It must not be earlier than `started_at_gte`.
        :param status: A comma-separated list of statuses. Return only recoveries with
            one of these statuses. By default, recoveries with any status are returned.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_data_recovery/recoveries"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if order is not None:
            __query["order"] = order
        if pretty is not None:
            __query["pretty"] = pretty
        if search_after_recovery_id is not None:
            __query["search_after_recovery_id"] = search_after_recovery_id
        if search_after_started_at is not None:
            __query["search_after_started_at"] = search_after_started_at
        if size is not None:
            __query["size"] = size
        if started_at_gte is not None:
            __query["started_at_gte"] = started_at_gte
        if started_at_lt is not None:
            __query["started_at_lt"] = started_at_lt
        if status is not None:
            __query["status"] = status
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="data_recovery.list_recoveries",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_fields=(
            "mode",
            "recovery_point_end_time",
            "sources",
            "metadata",
            "rename_strategy",
        ),
    )
    @_availability_warning(Stability.STABLE, Visibility.PRIVATE)
    def start_recovery(
        self,
        *,
        mode: t.Optional[t.Union[str, t.Literal["rename", "replace"]]] = None,
        recovery_point_end_time: t.Optional[t.Union[str, t.Any]] = None,
        sources: t.Optional[t.Sequence[str]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        metadata: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        rename_strategy: t.Optional[t.Mapping[str, t.Any]] = None,
        body: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Start a recovery.</p>
          <p>Start recovering indices and data streams from a recovery point.
          This API is intended for internal operator use.
          Depending on the mode, the sources are either replaced with their state at the recovery point, over the data that currently exists,
          or recovered under new names.
          The recovery runs in the background, so the API returns with a <code>202 Accepted</code> status once it has started.</p>


        :param mode: How to recover the sources: `replace` recovers them in place, over
            the data that currently exists, and `rename` recovers them under new names.
        :param recovery_point_end_time: The exact end time of the recovery point to recover
            from, as a date or epoch milliseconds. An `end_time` returned when listing
            recovery points can be passed back as it is.
        :param sources: The sources to recover. Each value is an index or data stream
            expression. Wildcards and exclusions prefixed with `-` are supported. The
            list must not be empty and must not contain blank values.
        :param master_timeout: The period to wait for the master node. If the master
            node is not available before the timeout expires, the request fails and returns
            an error. To indicate that the request should never timeout, set it to `-1`.
        :param metadata: Custom metadata for the recovery.
        :param rename_strategy: How to derive the new name of each recovered source from
            its name. Required when `mode` is `rename`, and not allowed when `mode` is
            `replace`.
        """
        if mode is None and body is None:
            raise ValueError("Empty value passed for parameter 'mode'")
        if recovery_point_end_time is None and body is None:
            raise ValueError(
                "Empty value passed for parameter 'recovery_point_end_time'"
            )
        if sources is None and body is None:
            raise ValueError("Empty value passed for parameter 'sources'")
        __path_parts: t.Dict[str, str] = {}
        __path = "/_data_recovery/recoveries"
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
        if not __body:
            if mode is not None:
                __body["mode"] = mode
            if recovery_point_end_time is not None:
                __body["recovery_point_end_time"] = recovery_point_end_time
            if sources is not None:
                __body["sources"] = sources
            if metadata is not None:
                __body["metadata"] = metadata
            if rename_strategy is not None:
                __body["rename_strategy"] = rename_strategy
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="data_recovery.start_recovery",
            path_parts=__path_parts,
        )

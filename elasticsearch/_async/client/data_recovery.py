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
    async def get_recovery_points(
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
        :param master_timeout: The period to wait for a connection to the master node.
            If no response is received before the timeout expires, the request fails
            and returns an error.
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
        return await self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="data_recovery.get_recovery_points",
            path_parts=__path_parts,
        )

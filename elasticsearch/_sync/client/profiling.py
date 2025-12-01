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

    @_rewrite_parameters(
        body_name="conditions",
    )
    def flamegraph(
        self,
        *,
        conditions: t.Optional[t.Any] = None,
        body: t.Optional[t.Any] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Returns basic information about the status of Universal Profiling.</p>


        `<https://www.elastic.co/guide/en/observability/8.19/universal-profiling.html>`_

        :param conditions:
        """
        if conditions is None and body is None:
            raise ValueError(
                "Empty value passed for parameters 'conditions' and 'body', one of them should be set."
            )
        elif conditions is not None and body is not None:
            raise ValueError("Cannot set both 'conditions' and 'body'")
        __path_parts: t.Dict[str, str] = {}
        __path = "/_profiling/flamegraph"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __body = conditions if conditions is not None else body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="profiling.flamegraph",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_name="conditions",
    )
    def stacktraces(
        self,
        *,
        conditions: t.Optional[t.Any] = None,
        body: t.Optional[t.Any] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Extracts raw stacktrace information from Universal Profiling.</p>


        `<https://www.elastic.co/guide/en/observability/8.19/universal-profiling.html>`_

        :param conditions:
        """
        if conditions is None and body is None:
            raise ValueError(
                "Empty value passed for parameters 'conditions' and 'body', one of them should be set."
            )
        elif conditions is not None and body is not None:
            raise ValueError("Cannot set both 'conditions' and 'body'")
        __path_parts: t.Dict[str, str] = {}
        __path = "/_profiling/stacktraces"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __body = conditions if conditions is not None else body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="profiling.stacktraces",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    def status(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        wait_for_resources_created: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Returns basic information about the status of Universal Profiling.</p>


        `<https://www.elastic.co/guide/en/observability/8.19/universal-profiling.html>`_

        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        :param wait_for_resources_created: Whether to return immediately or wait until
            resources have been created
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_profiling/status"
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
        if wait_for_resources_created is not None:
            __query["wait_for_resources_created"] = wait_for_resources_created
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="profiling.status",
            path_parts=__path_parts,
        )

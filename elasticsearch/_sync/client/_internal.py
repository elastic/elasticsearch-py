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
    @_stability_warning(Stability.EXPERIMENTAL)
    def delete_desired_balance(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>This API is a diagnostics API and the output should not be relied upon for building applications.</p>


        :param master_timeout: Period to wait for a connection to the master node.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_internal/desired_balance"
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
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="_internal.delete_desired_balance",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_stability_warning(Stability.EXPERIMENTAL)
    def delete_desired_nodes(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Designed for indirect use by ECE/ESS and ECK, direct use is not supported.</p>


        :param master_timeout: Period to wait for a connection to the master node.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_internal/desired_nodes"
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
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="_internal.delete_desired_nodes",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_stability_warning(Stability.EXPERIMENTAL)
    def get_desired_balance(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>This API is a diagnostics API and the output should not be relied upon for building applications.</p>


        :param master_timeout: Period to wait for a connection to the master node.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_internal/desired_balance"
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
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="_internal.get_desired_balance",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_stability_warning(Stability.EXPERIMENTAL)
    def get_desired_nodes(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Gets the latest desired nodes.</p>


        :param master_timeout: Period to wait for a connection to the master node.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_internal/desired_nodes/_latest"
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
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="_internal.get_desired_nodes",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_stability_warning(Stability.EXPERIMENTAL)
    def prevalidate_node_removal(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        external_ids: t.Optional[t.Sequence[str]] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        ids: t.Optional[t.Sequence[str]] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        names: t.Optional[t.Sequence[str]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Prevalidates node removal from the cluster.</p>


        :param external_ids: A comma-separated list of node external IDs to prevalidate
        :param ids: A comma-separated list of node IDs to prevalidate
        :param master_timeout: Period to wait for a connection to the master node.
        :param names: A comma-separated list of node names to prevalidate
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_internal/prevalidate_node_removal"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if external_ids is not None:
            __query["external_ids"] = external_ids
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ids is not None:
            __query["ids"] = ids
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if names is not None:
            __query["names"] = names
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="_internal.prevalidate_node_removal",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_name="body",
        ignore_deprecated_options={"body"},
    )
    @_stability_warning(Stability.EXPERIMENTAL)
    def update_desired_nodes(
        self,
        *,
        history_id: str,
        version: int,
        body: t.Optional[t.Any] = None,
        body: t.Optional[t.Any] = None,
        dry_run: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union[str, t.Literal[-1], t.Literal[0]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Designed for indirect use by ECE/ESS and ECK, direct use is not supported.</p>


        :param history_id: The history ID
        :param version: The version number
        :param body:
        :param dry_run: Simulate the update
        :param master_timeout: Period to wait for a connection to the master node.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        if history_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'history_id'")
        if version in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'version'")
        if body is None and body is None:
            raise ValueError(
                "Empty value passed for parameters 'body' and 'body', one of them should be set."
            )
        elif body is not None and body is not None:
            raise ValueError("Cannot set both 'body' and 'body'")
        __path_parts: t.Dict[str, str] = {
            "history_id": _quote(history_id),
            "version": _quote(version),
        }
        __path = f'/_internal/desired_nodes/{__path_parts["history_id"]}/{__path_parts["version"]}'
        __query: t.Dict[str, t.Any] = {}
        if dry_run is not None:
            __query["dry_run"] = dry_run
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
        __body = body if body is not None else body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="_internal.update_desired_nodes",
            path_parts=__path_parts,
        )

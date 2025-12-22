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
from .utils import (
    SKIP_IN_PATH,
    Stability,
    _availability_warning,
    _quote,
    _rewrite_parameters,
)


class ProjectRoutingClient(NamespacedClient):

    @_rewrite_parameters(
        body_name="expressions",
    )
    @_availability_warning(Stability.EXPERIMENTAL)
    def create(
        self,
        *,
        name: str,
        expressions: t.Optional[t.Mapping[str, t.Any]] = None,
        body: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Create of update a single named project routing expression.</p>
          <p>Create of update a single named project routing expression.</p>


        :param name: The name of project routing expression
        :param expressions:
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        if expressions is None and body is None:
            raise ValueError(
                "Empty value passed for parameters 'expressions' and 'body', one of them should be set."
            )
        elif expressions is not None and body is not None:
            raise ValueError("Cannot set both 'expressions' and 'body'")
        __path_parts: t.Dict[str, str] = {"name": _quote(name)}
        __path = f'/_project_routing/{__path_parts["name"]}'
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __body = expressions if expressions is not None else body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="project_routing.create",
            path_parts=__path_parts,
        )

    @_rewrite_parameters(
        body_name="expressions",
    )
    @_availability_warning(Stability.EXPERIMENTAL)
    def create_many(
        self,
        *,
        expressions: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        body: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Create of update named project routing expressions.</p>
          <p>Create or update named project routing expressions.</p>


        :param expressions:
        """
        if expressions is None and body is None:
            raise ValueError(
                "Empty value passed for parameters 'expressions' and 'body', one of them should be set."
            )
        elif expressions is not None and body is not None:
            raise ValueError("Cannot set both 'expressions' and 'body'")
        __path_parts: t.Dict[str, str] = {}
        __path = "/_project_routing"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __body = expressions if expressions is not None else body
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT",
            __path,
            params=__query,
            headers=__headers,
            body=__body,
            endpoint_id="project_routing.create_many",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_availability_warning(Stability.EXPERIMENTAL)
    def delete(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Delete named project routing expressions.</p>
          <p>Delete named project routing expressions.</p>


        :param name: The name of project routing expression
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path_parts: t.Dict[str, str] = {"name": _quote(name)}
        __path = f'/_project_routing/{__path_parts["name"]}'
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
            endpoint_id="project_routing.delete",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_availability_warning(Stability.EXPERIMENTAL)
    def get(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get named project routing expressions.</p>
          <p>Get named project routing expressions.</p>


        :param name: The name of project routing expression
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path_parts: t.Dict[str, str] = {"name": _quote(name)}
        __path = f'/_project_routing/{__path_parts["name"]}'
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
            endpoint_id="project_routing.get",
            path_parts=__path_parts,
        )

    @_rewrite_parameters()
    @_availability_warning(Stability.EXPERIMENTAL)
    def get_many(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get named project routing expressions.</p>
          <p>Get named project routing expressions.</p>

        """
        __path_parts: t.Dict[str, str] = {}
        __path = "/_project_routing"
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
            endpoint_id="project_routing.get_many",
            path_parts=__path_parts,
        )

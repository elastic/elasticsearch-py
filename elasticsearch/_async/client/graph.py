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


class GraphClient(NamespacedClient):
    @_rewrite_parameters(
        body_fields=True,
    )
    async def explore(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        connections: t.Optional[t.Mapping[str, t.Any]] = None,
        controls: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        query: t.Optional[t.Mapping[str, t.Any]] = None,
        routing: t.Optional[str] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        vertices: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Explore extracted and summarized information about the documents and terms in
        an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/graph-explore-api.html>`_

        :param index: A comma-separated list of index names to search; use `_all` or
            empty string to perform the operation on all indices
        :param connections:
        :param controls:
        :param query:
        :param routing: Specific routing value
        :param timeout: Explicit operation timeout
        :param vertices:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_graph/explore"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if connections is not None:
            __body["connections"] = connections
        if controls is not None:
            __body["controls"] = controls
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if query is not None:
            __body["query"] = query
        if routing is not None:
            __query["routing"] = routing
        if timeout is not None:
            __query["timeout"] = timeout
        if vertices is not None:
            __body["vertices"] = vertices
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

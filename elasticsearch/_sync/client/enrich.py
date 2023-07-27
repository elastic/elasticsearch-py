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


class EnrichClient(NamespacedClient):
    @_rewrite_parameters()
    def delete_policy(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes an existing enrich policy and its enrich index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/delete-enrich-policy-api.html>`_

        :param name: The name of the enrich policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_enrich/policy/{_quote(name)}"
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
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def execute_policy(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        wait_for_completion: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates the enrich index for an existing enrich policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/execute-enrich-policy-api.html>`_

        :param name: The name of the enrich policy
        :param wait_for_completion: Should the request should block until the execution
            is complete.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_enrich/policy/{_quote(name)}/_execute"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_policy(
        self,
        *,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Gets information about an enrich policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/get-enrich-policy-api.html>`_

        :param name: A comma-separated list of enrich policy names
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_enrich/policy/{_quote(name)}"
        else:
            __path = "/_enrich/policy"
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
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_policy(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        geo_match: t.Optional[t.Mapping[str, t.Any]] = None,
        human: t.Optional[bool] = None,
        match: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        range: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a new enrich policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/put-enrich-policy-api.html>`_

        :param name: The name of the enrich policy
        :param geo_match:
        :param match:
        :param range:
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_enrich/policy/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if geo_match is not None:
            __body["geo_match"] = geo_match
        if human is not None:
            __query["human"] = human
        if match is not None:
            __body["match"] = match
        if pretty is not None:
            __query["pretty"] = pretty
        if range is not None:
            __body["range"] = range
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def stats(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Gets enrich coordinator statistics and information about enrich policies that
        are currently executing.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/enrich-stats-api.html>`_
        """
        __path = "/_enrich/_stats"
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
            "GET", __path, params=__query, headers=__headers
        )

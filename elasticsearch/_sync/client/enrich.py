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


class EnrichClient(NamespacedClient):
    @_rewrite_parameters()
    def delete_policy(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes an existing enrich policy and its enrich index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-enrich-policy-api.html>`_

        :param name: The name of the enrich policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_enrich/policy/{_quote(name)}"
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

    @_rewrite_parameters()
    def execute_policy(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates the enrich index for an existing enrich policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/execute-enrich-policy-api.html>`_

        :param name: The name of the enrich policy
        :param wait_for_completion: Should the request should block until the execution
            is complete.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_enrich/policy/{_quote(name)}/_execute"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("PUT", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def get_policy(
        self,
        *,
        name: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Gets information about an enrich policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/get-enrich-policy-api.html>`_

        :param name: A comma-separated list of enrich policy names
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_enrich/policy/{_quote(name)}"
        else:
            __path = "/_enrich/policy"
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
    def put_policy(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        geo_match: Optional[Any] = None,
        human: Optional[bool] = None,
        match: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a new enrich policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/put-enrich-policy-api.html>`_

        :param name: The name of the enrich policy
        :param geo_match:
        :param match:
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_enrich/policy/{_quote(name)}"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

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
        Gets enrich coordinator statistics and information about enrich policies that
        are currently executing.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-stats-api.html>`_
        """
        __path = "/_enrich/_stats"
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

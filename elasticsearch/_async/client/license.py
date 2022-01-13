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
from .utils import _rewrite_parameters


class LicenseClient(NamespacedClient):
    @_rewrite_parameters()
    async def delete(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes licensing information for the cluster

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/delete-license.html>`_
        """
        __path = "/_license"
        __query: Dict[str, Any] = {}
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
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get(
        self,
        *,
        accept_enterprise: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        local: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves licensing information for the cluster

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/get-license.html>`_

        :param accept_enterprise: If `true`, this parameter returns enterprise for Enterprise
            license types. If `false`, this parameter returns platinum for both platinum
            and enterprise license types. This behavior is maintained for backwards compatibility.
            This parameter is deprecated and will always be set to true in 8.x.
        :param local: Specifies whether to retrieve local information. The default value
            is `false`, which means the information is retrieved from the master node.
        """
        __path = "/_license"
        __query: Dict[str, Any] = {}
        if accept_enterprise is not None:
            __query["accept_enterprise"] = accept_enterprise
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if local is not None:
            __query["local"] = local
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_basic_status(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information about the status of the basic license.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/get-basic-status.html>`_
        """
        __path = "/_license/basic_status"
        __query: Dict[str, Any] = {}
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
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def get_trial_status(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information about the status of the trial license.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/get-trial-status.html>`_
        """
        __path = "/_license/trial_status"
        __query: Dict[str, Any] = {}
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
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    async def post(
        self,
        *,
        licenses: List[Any],
        acknowledge: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        license: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Updates the license for the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/update-license.html>`_

        :param licenses: A sequence of one or more JSON documents containing the license
            information.
        :param acknowledge: Specifies whether you acknowledge the license changes.
        :param license:
        """
        if licenses is None:
            raise ValueError("Empty value passed for parameter 'licenses'")
        __path = "/_license"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if licenses is not None:
            __body["licenses"] = licenses
        if acknowledge is not None:
            __query["acknowledge"] = acknowledge
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if license is not None:
            __body["license"] = license
        if pretty is not None:
            __query["pretty"] = pretty
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return await self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    async def post_start_basic(
        self,
        *,
        acknowledge: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Starts an indefinite basic license.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/start-basic.html>`_

        :param acknowledge: whether the user has acknowledged acknowledge messages (default:
            false)
        """
        __path = "/_license/start_basic"
        __query: Dict[str, Any] = {}
        if acknowledge is not None:
            __query["acknowledge"] = acknowledge
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
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    async def post_start_trial(
        self,
        *,
        acknowledge: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        type_query_string: Optional[str] = None,
    ) -> ObjectApiResponse[Any]:
        """
        starts a limited time trial license.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/start-trial.html>`_

        :param acknowledge: whether the user has acknowledged acknowledge messages (default:
            false)
        :param type_query_string:
        """
        __path = "/_license/start_trial"
        __query: Dict[str, Any] = {}
        if acknowledge is not None:
            __query["acknowledge"] = acknowledge
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if type_query_string is not None:
            __query["type_query_string"] = type_query_string
        __headers = {"accept": "application/json"}
        return await self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

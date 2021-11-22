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


class DanglingIndicesClient(NamespacedClient):
    @_rewrite_parameters()
    async def delete_dangling_index(
        self,
        *,
        index_uuid: Any,
        accept_data_loss: bool,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes the specified dangling index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-gateway-dangling-indices.html>`_

        :param index_uuid: The UUID of the dangling index
        :param accept_data_loss: Must be set to true in order to delete the dangling
            index
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        """
        if index_uuid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index_uuid'")
        if accept_data_loss is None:
            raise ValueError("Empty value passed for parameter 'accept_data_loss'")
        __path = f"/_dangling/{_quote(index_uuid)}"
        __query: Dict[str, Any] = {}
        if accept_data_loss is not None:
            __query["accept_data_loss"] = accept_data_loss
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("DELETE", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def import_dangling_index(
        self,
        *,
        index_uuid: Any,
        accept_data_loss: bool,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Imports the specified dangling index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-gateway-dangling-indices.html>`_

        :param index_uuid: The UUID of the dangling index
        :param accept_data_loss: Must be set to true in order to import the dangling
            index
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        """
        if index_uuid in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index_uuid'")
        if accept_data_loss is None:
            raise ValueError("Empty value passed for parameter 'accept_data_loss'")
        __path = f"/_dangling/{_quote(index_uuid)}"
        __query: Dict[str, Any] = {}
        if accept_data_loss is not None:
            __query["accept_data_loss"] = accept_data_loss
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return await self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    async def list_dangling_indices(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns all dangling indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-gateway-dangling-indices.html>`_
        """
        __path = "/_dangling"
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
        return await self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

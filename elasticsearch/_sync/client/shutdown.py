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


class ShutdownClient(NamespacedClient):
    @_rewrite_parameters()
    def delete_node(
        self,
        *,
        node_id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes a node from the shutdown list. Designed for indirect use by ECE/ESS and
        ECK. Direct use is not supported.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        :param node_id: The node id of node to be removed from the shutdown state
        """
        if node_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'node_id'")
        __path = f"/_nodes/{_quote(node_id)}/shutdown"
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
    def get_node(
        self,
        *,
        node_id: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieve status of a node or nodes that are currently marked as shutting down.
        Designed for indirect use by ECE/ESS and ECK. Direct use is not supported.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        :param node_id: Which node for which to retrieve the shutdown status
        """
        if node_id not in SKIP_IN_PATH:
            __path = f"/_nodes/{_quote(node_id)}/shutdown"
        else:
            __path = "/_nodes/shutdown"
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

    @_rewrite_parameters()
    def put_node(
        self,
        *,
        node_id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Adds a node to be shut down. Designed for indirect use by ECE/ESS and ECK. Direct
        use is not supported.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        :param node_id: The node id of node to be shut down
        """
        if node_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'node_id'")
        __path = f"/_nodes/{_quote(node_id)}/shutdown"
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
        return self._perform_request("PUT", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

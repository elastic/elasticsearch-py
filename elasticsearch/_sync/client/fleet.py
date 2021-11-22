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


class FleetClient(NamespacedClient):
    @_rewrite_parameters()
    def global_checkpoints(
        self,
        *,
        index: Any,
        checkpoints: Optional[List[Any]] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
        wait_for_advance: Optional[bool] = None,
        wait_for_index: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns the current global checkpoints for an index. This API is design for internal
        use by the fleet server project.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/get-global-checkpoints.html>`_

        :param index: A single index or index alias that resolves to a single index.
        :param checkpoints: A comma separated list of previous global checkpoints. When
            used in combination with `wait_for_advance`, the API will only return once
            the global checkpoints advances past the checkpoints. Providing an empty
            list will cause Elasticsearch to immediately return the current global checkpoints.
        :param timeout: Period to wait for a global checkpoints to advance past `checkpoints`.
        :param wait_for_advance: A boolean value which controls whether to wait (until
            the timeout) for the global checkpoints to advance past the provided `checkpoints`.
        :param wait_for_index: A boolean value which controls whether to wait (until
            the timeout) for the target index to exist and all primary shards be active.
            Can only be true when `wait_for_advance` is true.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_fleet/global_checkpoints"
        __query: Dict[str, Any] = {}
        if checkpoints is not None:
            __query["checkpoints"] = checkpoints
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_advance is not None:
            __query["wait_for_advance"] = wait_for_advance
        if wait_for_index is not None:
            __query["wait_for_index"] = wait_for_index
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

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


class IlmClient(NamespacedClient):
    @_rewrite_parameters()
    def delete_lifecycle(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes the specified lifecycle policy definition. A currently used policy cannot
        be deleted.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-delete-lifecycle.html>`_

        :param name: The name of the index lifecycle policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_ilm/policy/{_quote(name)}"
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
    def explain_lifecycle(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        only_errors: Optional[bool] = None,
        only_managed: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves information about the index's current lifecycle state, such as the
        currently executing phase, action, and step.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-explain-lifecycle.html>`_

        :param index: The name of the index to explain
        :param only_errors: filters the indices included in the response to ones in an
            ILM error state, implies only_managed
        :param only_managed: filters the indices included in the response to ones managed
            by ILM
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ilm/explain"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if only_errors is not None:
            __query["only_errors"] = only_errors
        if only_managed is not None:
            __query["only_managed"] = only_managed
        if pretty is not None:
            __query["pretty"] = pretty
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def get_lifecycle(
        self,
        *,
        name: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Returns the specified policy definition. Includes the policy version and last
        modified date.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-get-lifecycle.html>`_

        :param name: The name of the index lifecycle policy
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_ilm/policy/{_quote(name)}"
        else:
            __path = "/_ilm/policy"
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
    def get_status(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves the current index lifecycle management (ILM) status.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-get-status.html>`_
        """
        __path = "/_ilm/status"
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
    def move_to_step(
        self,
        *,
        index: Any,
        current_step: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        next_step: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Manually moves an index into the specified step and executes that step.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-move-to-step.html>`_

        :param index: The name of the index whose lifecycle step is to change
        :param current_step:
        :param next_step:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/_ilm/move/{_quote(index)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if current_step is not None:
            __body["current_step"] = current_step
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if next_step is not None:
            __body["next_step"] = next_step
        if pretty is not None:
            __query["pretty"] = pretty
        if not __body:
            __body = None  # type: ignore[assignment]
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_lifecycle(
        self,
        *,
        name: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        policy: Optional[Any] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Creates a lifecycle policy

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-put-lifecycle.html>`_

        :param name: The name of the index lifecycle policy
        :param policy:
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_ilm/policy/{_quote(name)}"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if policy is not None:
            __body["policy"] = policy
        if pretty is not None:
            __query["pretty"] = pretty
        if not __body:
            __body = None  # type: ignore[assignment]
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def remove_policy(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Removes the assigned lifecycle policy and stops managing the specified index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-remove-policy.html>`_

        :param index: The name of the index to remove policy on
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ilm/remove"
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def retry(
        self,
        *,
        index: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retries executing the policy for an index that is in the ERROR step.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-retry-policy.html>`_

        :param index: The name of the indices (comma-separated) whose failed lifecycle
            step is to be retry
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_ilm/retry"
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def start(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Start the index lifecycle management (ILM) plugin.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-start.html>`_

        :param master_timeout:
        :param timeout:
        """
        __path = "/_ilm/start"
        __query: Dict[str, Any] = {}
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def stop(
        self,
        *,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        master_timeout: Optional[Any] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Halts all lifecycle management operations and stops the index lifecycle management
        (ILM) plugin

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-stop.html>`_

        :param master_timeout:
        :param timeout:
        """
        __path = "/_ilm/stop"
        __query: Dict[str, Any] = {}
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
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

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


class TransformClient(NamespacedClient):
    @_rewrite_parameters()
    def delete_transform(
        self,
        *,
        transform_id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        force: Optional[bool] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Deletes an existing transform.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-transform.html>`_

        :param transform_id: The id of the transform to delete
        :param force: When `true`, the transform is deleted regardless of its current
            state. The default value is `false`, meaning that the transform must be `stopped`
            before it can be deleted.
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'transform_id'")
        __path = f"/_transform/{_quote(transform_id)}"
        __query: Dict[str, Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if force is not None:
            __query["force"] = force
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

    @_rewrite_parameters(
        parameter_aliases={"from": "from_"},
    )
    def get_transform(
        self,
        *,
        transform_id: Optional[Any] = None,
        allow_no_match: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        exclude_generated: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        from_: Optional[int] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        size: Optional[int] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves configuration information for transforms.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/get-transform.html>`_

        :param transform_id: The id or comma delimited list of id expressions of the
            transforms to get, '_all' or '*' implies get all transforms
        :param allow_no_match: Whether to ignore if a wildcard expression matches no
            transforms. (This includes `_all` string or when no transforms have been
            specified)
        :param exclude_generated: Omits fields that are illegal to set on transform PUT
        :param from_: skips a number of transform configs, defaults to 0
        :param size: specifies a max number of transforms to get, defaults to 100
        """
        if transform_id not in SKIP_IN_PATH:
            __path = f"/_transform/{_quote(transform_id)}"
        else:
            __path = "/_transform"
        __query: Dict[str, Any] = {}
        if allow_no_match is not None:
            __query["allow_no_match"] = allow_no_match
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if exclude_generated is not None:
            __query["exclude_generated"] = exclude_generated
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if from_ is not None:
            __query["from"] = from_
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if size is not None:
            __query["size"] = size
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        parameter_aliases={"from": "from_"},
    )
    def get_transform_stats(
        self,
        *,
        transform_id: Any,
        allow_no_match: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        from_: Optional[int] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        size: Optional[int] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Retrieves usage information for transforms.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/get-transform-stats.html>`_

        :param transform_id: The id of the transform for which to get stats. '_all' or
            '*' implies all transforms
        :param allow_no_match: Whether to ignore if a wildcard expression matches no
            transforms. (This includes `_all` string or when no transforms have been
            specified)
        :param from_: skips a number of transform stats, defaults to 0
        :param size: specifies a max number of transform stats to get, defaults to 100
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'transform_id'")
        __path = f"/_transform/{_quote(transform_id)}/_stats"
        __query: Dict[str, Any] = {}
        if allow_no_match is not None:
            __query["allow_no_match"] = allow_no_match
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if from_ is not None:
            __query["from"] = from_
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if size is not None:
            __query["size"] = size
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("GET", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def preview_transform(
        self,
        *,
        transform_id: Optional[Any] = None,
        description: Optional[str] = None,
        dest: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        frequency: Optional[Any] = None,
        human: Optional[bool] = None,
        latest: Optional[Any] = None,
        pivot: Optional[Any] = None,
        pretty: Optional[bool] = None,
        retention_policy: Optional[Any] = None,
        settings: Optional[Any] = None,
        source: Optional[Any] = None,
        sync: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Previews a transform.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/preview-transform.html>`_

        :param transform_id: The id of the transform to preview.
        :param description: Free text description of the transform.
        :param dest: The destination for the transform.
        :param frequency: The interval between checks for changes in the source indices
            when the transform is running continuously. Also determines the retry interval
            in the event of transient failures while the transform is searching or indexing.
            The minimum value is 1s and the maximum is 1h.
        :param latest: The latest method transforms the data by finding the latest document
            for each unique key.
        :param pivot: The pivot method transforms the data by aggregating and grouping
            it. These objects define the group by fields and the aggregation to reduce
            the data.
        :param retention_policy: Defines a retention policy for the transform. Data that
            meets the defined criteria is deleted from the destination index.
        :param settings: Defines optional transform settings.
        :param source: The source of the data for the transform.
        :param sync: Defines the properties transforms require to run continuously.
        """
        if transform_id not in SKIP_IN_PATH:
            __path = f"/_transform/{_quote(transform_id)}/_preview"
        else:
            __path = "/_transform/_preview"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if description is not None:
            __body["description"] = description
        if dest is not None:
            __body["dest"] = dest
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if frequency is not None:
            __body["frequency"] = frequency
        if human is not None:
            __query["human"] = human
        if latest is not None:
            __body["latest"] = latest
        if pivot is not None:
            __body["pivot"] = pivot
        if pretty is not None:
            __query["pretty"] = pretty
        if retention_policy is not None:
            __body["retention_policy"] = retention_policy
        if settings is not None:
            __body["settings"] = settings
        if source is not None:
            __body["source"] = source
        if sync is not None:
            __body["sync"] = sync
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
    def put_transform(
        self,
        *,
        transform_id: Any,
        dest: Any,
        source: Any,
        defer_validation: Optional[bool] = None,
        description: Optional[str] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        frequency: Optional[Any] = None,
        human: Optional[bool] = None,
        latest: Optional[Any] = None,
        pivot: Optional[Any] = None,
        pretty: Optional[bool] = None,
        retention_policy: Optional[Any] = None,
        settings: Optional[Any] = None,
        sync: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Instantiates a transform.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/put-transform.html>`_

        :param transform_id: Identifier for the transform. This identifier can contain
            lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores.
            It must start and end with alphanumeric characters.
        :param dest: The destination for the transform.
        :param source: The source of the data for the transform.
        :param defer_validation: When true, deferrable validations are not run. This
            behavior may be desired if the source index does not exist until after the
            transform is created.
        :param description: Free text description of the transform.
        :param frequency: The interval between checks for changes in the source indices
            when the transform is running continuously. Also determines the retry interval
            in the event of transient failures while the transform is searching or indexing.
            The minimum value is 1s and the maximum is 1h.
        :param latest: The latest method transforms the data by finding the latest document
            for each unique key.
        :param pivot: The pivot method transforms the data by aggregating and grouping
            it. These objects define the group by fields and the aggregation to reduce
            the data.
        :param retention_policy: Defines a retention policy for the transform. Data that
            meets the defined criteria is deleted from the destination index.
        :param settings: Defines optional transform settings.
        :param sync: Defines the properties transforms require to run continuously.
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'transform_id'")
        if dest is None:
            raise ValueError("Empty value passed for parameter 'dest'")
        if source is None:
            raise ValueError("Empty value passed for parameter 'source'")
        __path = f"/_transform/{_quote(transform_id)}"
        __body: Dict[str, Any] = {}
        __query: Dict[str, Any] = {}
        if dest is not None:
            __body["dest"] = dest
        if source is not None:
            __body["source"] = source
        if defer_validation is not None:
            __query["defer_validation"] = defer_validation
        if description is not None:
            __body["description"] = description
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if frequency is not None:
            __body["frequency"] = frequency
        if human is not None:
            __query["human"] = human
        if latest is not None:
            __body["latest"] = latest
        if pivot is not None:
            __body["pivot"] = pivot
        if pretty is not None:
            __query["pretty"] = pretty
        if retention_policy is not None:
            __body["retention_policy"] = retention_policy
        if settings is not None:
            __body["settings"] = settings
        if sync is not None:
            __body["sync"] = sync
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("PUT", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def start_transform(
        self,
        *,
        transform_id: Any,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Starts one or more transforms.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/start-transform.html>`_

        :param transform_id: The id of the transform to start
        :param timeout: Controls the time to wait for the transform to start
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'transform_id'")
        __path = f"/_transform/{_quote(transform_id)}/_start"
        __query: Dict[str, Any] = {}
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
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters()
    def stop_transform(
        self,
        *,
        transform_id: Any,
        allow_no_match: Optional[bool] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        force: Optional[bool] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        timeout: Optional[Any] = None,
        wait_for_checkpoint: Optional[bool] = None,
        wait_for_completion: Optional[bool] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Stops one or more transforms.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/stop-transform.html>`_

        :param transform_id: The id of the transform to stop
        :param allow_no_match: Whether to ignore if a wildcard expression matches no
            transforms. (This includes `_all` string or when no transforms have been
            specified)
        :param force: Whether to force stop a failed transform or not. Default to false
        :param timeout: Controls the time to wait until the transform has stopped. Default
            to 30 seconds
        :param wait_for_checkpoint: Whether to wait for the transform to reach a checkpoint
            before stopping. Default to false
        :param wait_for_completion: Whether to wait for the transform to fully stop before
            returning or not. Default to false
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'transform_id'")
        __path = f"/_transform/{_quote(transform_id)}/_stop"
        __query: Dict[str, Any] = {}
        if allow_no_match is not None:
            __query["allow_no_match"] = allow_no_match
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if force is not None:
            __query["force"] = force
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_checkpoint is not None:
            __query["wait_for_checkpoint"] = wait_for_checkpoint
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json"}
        return self._perform_request("POST", __target, headers=__headers)  # type: ignore[no-any-return,return-value]

    @_rewrite_parameters(
        body_fields=True,
    )
    def update_transform(
        self,
        *,
        transform_id: Any,
        defer_validation: Optional[bool] = None,
        description: Optional[str] = None,
        dest: Optional[Any] = None,
        error_trace: Optional[bool] = None,
        filter_path: Optional[Union[List[str], str]] = None,
        frequency: Optional[Any] = None,
        human: Optional[bool] = None,
        pretty: Optional[bool] = None,
        retention_policy: Optional[Any] = None,
        settings: Optional[Any] = None,
        source: Optional[Any] = None,
        sync: Optional[Any] = None,
    ) -> ObjectApiResponse[Any]:
        """
        Updates certain properties of a transform.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/update-transform.html>`_

        :param transform_id: Identifier for the transform. This identifier can contain
            lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores.
            It must start and end with alphanumeric characters.
        :param defer_validation: When true, deferrable validations are not run. This
            behavior may be desired if the source index does not exist until after the
            transform is created.
        :param description: Free text description of the transform.
        :param dest: The destination for the transform.
        :param frequency: The interval between checks for changes in the source indices
            when the transform is running continuously. Also determines the retry interval
            in the event of transient failures while the transform is searching or indexing.
            The minimum value is 1s and the maximum is 1h.
        :param retention_policy: Defines a retention policy for the transform. Data that
            meets the defined criteria is deleted from the destination index.
        :param settings: Defines optional transform settings.
        :param source: The source of the data for the transform.
        :param sync: Defines the properties transforms require to run continuously.
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'transform_id'")
        __path = f"/_transform/{_quote(transform_id)}/_update"
        __query: Dict[str, Any] = {}
        __body: Dict[str, Any] = {}
        if defer_validation is not None:
            __query["defer_validation"] = defer_validation
        if description is not None:
            __body["description"] = description
        if dest is not None:
            __body["dest"] = dest
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if frequency is not None:
            __body["frequency"] = frequency
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if retention_policy is not None:
            __body["retention_policy"] = retention_policy
        if settings is not None:
            __body["settings"] = settings
        if source is not None:
            __body["source"] = source
        if sync is not None:
            __body["sync"] = sync
        if __query:
            __target = f"{__path}?{_quote_query(__query)}"
        else:
            __target = __path
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self._perform_request("POST", __target, headers=__headers, body=__body)  # type: ignore[no-any-return,return-value]

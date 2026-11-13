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


class PrometheusClient(NamespacedClient):

    @_rewrite_parameters()
    @_availability_warning(Stability.EXPERIMENTAL)
    async def status_buildinfo(
        self,
        *,
        index: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[t.Union[str, t.Sequence[str]]] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        .. raw:: html

          <p>Get Prometheus build information.</p>
          <p>Get Elasticsearch build information in the format of the Prometheus <code>/api/v1/status/buildinfo</code> endpoint.
          Prometheus-compatible clients, such as Grafana, call this endpoint to identify the backend and the features it supports.</p>


        `<https://www.elastic.co/docs/api/doc/elasticsearch#TODO>`_

        :param index: An index pattern, accepted for consistency with the other Prometheus
            endpoints. The response doesn't depend on it.
        """
        __path_parts: t.Dict[str, str]
        if index not in SKIP_IN_PATH:
            __path_parts = {"index": _quote(index)}
            __path = f'/_prometheus/{__path_parts["index"]}/api/v1/status/buildinfo'
        else:
            __path_parts = {}
            __path = "/_prometheus/api/v1/status/buildinfo"
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
        return await self.perform_request(  # type: ignore[return-value]
            "GET",
            __path,
            params=__query,
            headers=__headers,
            endpoint_id="prometheus.status_buildinfo",
            path_parts=__path_parts,
        )

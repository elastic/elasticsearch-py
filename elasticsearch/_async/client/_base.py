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

import urllib.parse
from typing import Any

from elastic_transport import AsyncTransport, HttpHeaders
from elastic_transport.client_utils import DEFAULT
from ..exceptions import UnsupportedProductError


class BaseClient:
    transport: AsyncTransport

    def __init__(self):
        self._headers = HttpHeaders({"content-type": "application/json"})
        self._request_timeout = DEFAULT
        self._ignore_status = DEFAULT
        self._max_retries = DEFAULT
        self._retry_on_timeout = DEFAULT
        self._retry_on_status = DEFAULT

    async def _perform_request(
        self, method: str, target: str, headers=None, params=None, body=None
    ) -> Any:
        # Handle the passing of 'params' as additional query parameters.
        # This behavior is deprecated and should be removed in 9.0.0.
        if params:
            if "?" in target:
                raise ValueError("Can't add query to a target that already has a query")
            target = f"{target}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"

        if headers:
            request_headers = self._headers.copy()
            request_headers.update(headers)
        else:
            request_headers = self._headers

        meta, response = await self.transport.perform_request(
            method, target, headers=request_headers, body=body
        )

        # 'X-Elastic-Product: Elasticsearch' should be on every response.
        if meta.headers.get("x-elastic-product", "") != "Elasticsearch":
            raise UnsupportedProductError(
                "The client noticed that the server is not Elasticsearch "
                "and we do not support this unknown product"
            )

        return response

    def options(
        self,
        *,
        opaque_id=DEFAULT,
        api_key=DEFAULT,
        basic_auth=DEFAULT,
        bearer_auth=DEFAULT,
        headers=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=DEFAULT,
        max_retries=DEFAULT,
        retry_on_status=DEFAULT,
        retry_on_timeout=DEFAULT,
    ):
        client = type(self)(_transport=self.transport)

        new_headers = self._headers.copy()
        if headers is not DEFAULT:
            new_headers.update(headers)
        if opaque_id is not DEFAULT:
            new_headers["x-opaque-id"] = opaque_id
        if (
            api_key is not DEFAULT
            or basic_auth is not DEFAULT
            or bearer_auth is not DEFAULT
        ):
            pass  # TODO

        if request_timeout is not DEFAULT:
            client._request_timeout = DEFAULT
        if ignore_status is not DEFAULT:
            client._ignore_status = DEFAULT
        if max_retries is not DEFAULT:
            client._max_retries = DEFAULT
        if retry_on_timeout is not DEFAULT:
            client._retry_on_timeout = DEFAULT
        if retry_on_status is not DEFAULT:
            client._retry_on_status = DEFAULT
        return client


class NamespacedClient:
    def __init__(self, client: "BaseClient") -> None:
        self._client = client

    async def _perform_request(
        self, method: str, target: str, headers=None, params=None, body=None
    ) -> Any:
        # Use the internal clients .perform_request() implementation
        # so we take advantage of their transport options.
        return await self._client._perform_request(
            method, target, headers=headers, params=params, body=body
        )

    @property
    def transport(self) -> AsyncTransport:
        return self._client.transport

    def options(
        self,
        *,
        opaque_id=DEFAULT,
        api_key=DEFAULT,
        basic_auth=DEFAULT,
        bearer_auth=DEFAULT,
        headers=DEFAULT,
        request_timeout=DEFAULT,
        ignore_status=DEFAULT,
        max_retries=DEFAULT,
        retry_on_status=DEFAULT,
        retry_on_timeout=DEFAULT,
    ) -> "NamespacedClient":
        return type(self)(
            self._client.options(
                opaque_id=opaque_id,
                api_key=api_key,
                basic_auth=basic_auth,
                bearer_auth=bearer_auth,
                headers=headers,
                request_timeout=request_timeout,
                ignore_status=ignore_status,
                max_retries=max_retries,
                retry_on_status=retry_on_status,
                retry_on_timeout=retry_on_timeout,
            )
        )

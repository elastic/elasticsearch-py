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

import re
import warnings
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

from elastic_transport import AsyncTransport, HttpHeaders, NodeConfig, SniffOptions
from elastic_transport.client_utils import DEFAULT, DefaultType, resolve_default

from ...compat import urlencode, warn_stacklevel
from ...exceptions import (
    HTTP_EXCEPTIONS,
    ApiError,
    ConnectionError,
    ElasticsearchWarning,
    SerializationError,
    UnsupportedProductError,
)
from .utils import _TYPE_ASYNC_SNIFF_CALLBACK, _base64_auth_header

SelfType = TypeVar("SelfType", bound="BaseClient")
SelfNamespacedType = TypeVar("SelfNamespacedType", bound="NamespacedClient")

_WARNING_RE = re.compile(r"\"([^\"]*)\"")


def resolve_auth_headers(
    headers: Optional[Mapping[str, str]],
    api_key: Union[DefaultType, None, Tuple[str, str], str] = DEFAULT,
    basic_auth: Union[DefaultType, None, Tuple[str, str], str] = DEFAULT,
    bearer_auth: Union[DefaultType, None, str] = DEFAULT,
) -> HttpHeaders:

    if headers is None:
        headers = HttpHeaders()
    elif not isinstance(headers, HttpHeaders):
        headers = HttpHeaders(headers)

    resolved_api_key = resolve_default(api_key, None)
    resolved_basic_auth = resolve_default(basic_auth, None)
    resolved_bearer_auth = resolve_default(bearer_auth, None)
    if resolved_api_key or resolved_basic_auth or resolved_bearer_auth:
        if (
            sum(
                x is not None
                for x in (
                    resolved_api_key,
                    resolved_basic_auth,
                    resolved_bearer_auth,
                )
            )
            > 1
        ):
            raise ValueError(
                "Can only set one of 'api_key', 'basic_auth', and 'bearer_auth'"
            )
        if headers and headers.get("authorization", None) is not None:
            raise ValueError(
                "Can't set 'Authorization' HTTP header with other authentication options"
            )
        if resolved_api_key:
            headers["authorization"] = f"ApiKey {_base64_auth_header(resolved_api_key)}"
        if resolved_basic_auth:
            headers[
                "authorization"
            ] = f"Basic {_base64_auth_header(resolved_basic_auth)}"
        if resolved_bearer_auth:
            headers["authorization"] = f"Bearer {resolved_bearer_auth}"

    return headers


def create_sniff_callback(
    host_info_callback: Optional[
        Callable[[Dict[str, Any], Dict[str, Any]], Optional[Dict[str, Any]]]
    ] = None,
    sniffed_node_callback: Optional[
        Callable[[Dict[str, Any], NodeConfig], Optional[NodeConfig]]
    ] = None,
) -> _TYPE_ASYNC_SNIFF_CALLBACK:
    assert (host_info_callback is None) != (sniffed_node_callback is None)

    # Wrap the deprecated 'host_info_callback' into 'sniffed_node_callback'
    if host_info_callback is not None:

        def _sniffed_node_callback(
            node_info: Dict[str, Any], node_config: NodeConfig
        ) -> Optional[NodeConfig]:
            assert host_info_callback is not None
            if (
                host_info_callback(  # type ignore[misc]
                    node_info, {"host": node_config.host, "port": node_config.port}
                )
                is None
            ):
                return None
            return node_config

        sniffed_node_callback = _sniffed_node_callback

    async def sniff_callback(
        transport: AsyncTransport, sniff_options: SniffOptions
    ) -> List[NodeConfig]:
        for _ in transport.node_pool.all():
            try:
                meta, node_infos = await transport.perform_request(
                    "GET",
                    "/_nodes/_all/http",
                    headers={"accept": "application/json"},
                    request_timeout=(
                        sniff_options.sniff_timeout
                        if not sniff_options.is_initial_sniff
                        else None
                    ),
                )
            except (SerializationError, ConnectionError):
                continue

            if not 200 <= meta.status <= 299:
                continue

            node_configs = []
            for node_info in node_infos.get("nodes", {}).values():
                address = node_info.get("http", {}).get("publish_address")
                if not address or ":" not in address:
                    continue

                if "/" in address:
                    # Support 7.x host/ip:port behavior where http.publish_host has been set.
                    fqdn, ipaddress = address.split("/", 1)
                    host = fqdn
                    _, port_str = ipaddress.rsplit(":", 1)
                    port = int(port_str)
                else:
                    host, port_str = address.rsplit(":", 1)
                    port = int(port_str)

                assert sniffed_node_callback is not None
                sniffed_node = sniffed_node_callback(
                    node_info, meta.node.replace(host=host, port=port)
                )
                if sniffed_node is None:
                    continue

                # Use the node which was able to make the request as a base.
                node_configs.append(sniffed_node)

            if node_configs:
                return node_configs

        return []

    return sniff_callback


def _default_sniffed_node_callback(
    node_info: Dict[str, Any], node_config: NodeConfig
) -> Optional[NodeConfig]:
    if node_info.get("roles", []) == ["master"]:
        return None
    return node_config


default_sniff_callback = create_sniff_callback(
    sniffed_node_callback=_default_sniffed_node_callback
)


class BaseClient:
    def __init__(self, _transport: AsyncTransport) -> None:
        self._transport = _transport
        self._headers = HttpHeaders({"content-type": "application/json"})
        self._request_timeout: Union[DefaultType, Optional[float]] = DEFAULT
        self._ignore_status: Union[DefaultType, Collection[int]] = DEFAULT
        self._max_retries: Union[DefaultType, int] = DEFAULT
        self._retry_on_timeout: Union[DefaultType, bool] = DEFAULT
        self._retry_on_status: Union[DefaultType, Collection[int]] = DEFAULT

    @property
    def transport(self) -> AsyncTransport:
        return self._transport

    async def _perform_request(
        self,
        method: str,
        target: str,
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[Mapping[str, str]] = None,
        body: Optional[Any] = None,
    ) -> Any:
        # Handle the passing of 'params' as additional query parameters.
        # This behavior is deprecated and should be removed in 9.0.0.
        if params:
            if "?" in target:
                raise ValueError("Can't add query to a target that already has a query")
            target = f"{target}?{urlencode(params)}"

        if headers:
            request_headers = self._headers.copy()
            request_headers.update(headers)
        else:
            request_headers = self._headers

        meta, response = await self.transport.perform_request(
            method,
            target,
            headers=request_headers,
            body=body,
            request_timeout=self._request_timeout,
            max_retries=self._max_retries,
            retry_on_status=self._retry_on_status,
            retry_on_timeout=self._retry_on_timeout,
        )

        if not 200 <= meta.status < 299 and (
            self._ignore_status is DEFAULT
            or self._ignore_status is None
            or meta.status not in self._ignore_status
        ):
            message = str(response)

            # If the response is an error response try parsing
            # the raw Elasticsearch error before raising.
            if isinstance(response, dict):
                try:
                    error = response.get("error", message)
                    if isinstance(error, dict) and "type" in error:
                        error = error["type"]
                    message = error
                except (ValueError, KeyError, TypeError):
                    pass

            raise HTTP_EXCEPTIONS.get(meta.status, ApiError)(
                message=message, meta=meta, body=response
            )

        # 'X-Elastic-Product: Elasticsearch' should be on every response.
        if meta.headers.get("x-elastic-product", "") != "Elasticsearch":
            raise UnsupportedProductError(
                message=(
                    "The client noticed that the server is not Elasticsearch "
                    "and we do not support this unknown product"
                ),
                meta=meta,
                body=response,
            )

        # 'Warning' headers should be reraised as 'ElasticsearchWarning'
        warning_header = (meta.headers.get("warning") or "").strip()
        if warning_header:
            warning_messages: Iterable[str] = _WARNING_RE.findall(warning_header) or (
                warning_header,
            )
            for warning_message in warning_messages:
                warnings.warn(
                    warning_message,
                    category=ElasticsearchWarning,
                    stacklevel=warn_stacklevel(),
                )

        return response

    def options(
        self: SelfType,
        *,
        opaque_id: Union[DefaultType, str] = DEFAULT,
        api_key: Union[DefaultType, str, Tuple[str, str]] = DEFAULT,
        basic_auth: Union[DefaultType, str, Tuple[str, str]] = DEFAULT,
        bearer_auth: Union[DefaultType, str] = DEFAULT,
        headers: Union[DefaultType, Mapping[str, str]] = DEFAULT,
        request_timeout: Union[DefaultType, Optional[float]] = DEFAULT,
        ignore_status: Union[DefaultType, int, Collection[int]] = DEFAULT,
        max_retries: Union[DefaultType, int] = DEFAULT,
        retry_on_status: Union[DefaultType, int, Collection[int]] = DEFAULT,
        retry_on_timeout: Union[DefaultType, bool] = DEFAULT,
    ) -> SelfType:
        client = type(self)(_transport=self.transport)

        resolved_headers = resolve_default(headers, None)
        resolved_headers = resolve_auth_headers(
            headers=resolved_headers,
            api_key=api_key,
            basic_auth=basic_auth,
            bearer_auth=bearer_auth,
        )
        resolved_opaque_id = resolve_default(opaque_id, None)
        if resolved_opaque_id:
            resolved_headers["x-opaque-id"] = resolved_opaque_id

        if resolved_headers:
            new_headers = self._headers.copy()
            new_headers.update(resolved_headers)
            client._headers = new_headers
        else:
            client._headers = self._headers.copy()

        if request_timeout is not DEFAULT:
            client._request_timeout = request_timeout

        if ignore_status is not DEFAULT:
            if isinstance(ignore_status, int):
                ignore_status = (ignore_status,)
            client._ignore_status = ignore_status

        if max_retries is not DEFAULT:
            if not isinstance(max_retries, int):
                raise TypeError("'max_retries' must be of type 'int'")
            client._max_retries = max_retries

        if retry_on_status is not DEFAULT:
            if isinstance(retry_on_status, int):
                retry_on_status = (retry_on_status,)
            client._retry_on_status = retry_on_status

        if retry_on_timeout is not DEFAULT:
            if not isinstance(retry_on_timeout, bool):
                raise TypeError("'retry_on_timeout' must be of type 'bool'")
            client._retry_on_timeout = retry_on_timeout

        return client


class NamespacedClient(BaseClient):
    def __init__(self, client: "BaseClient") -> None:
        self._client = client
        super().__init__(self._client.transport)

    async def _perform_request(
        self,
        method: str,
        target: str,
        headers: Optional[Mapping[str, str]] = None,
        params: Optional[Mapping[str, str]] = None,
        body: Optional[Any] = None,
    ) -> Any:
        # Use the internal clients .perform_request() implementation
        # so we take advantage of their transport options.
        return await self._client._perform_request(
            method, target, headers=headers, params=params, body=body
        )

    def options(
        self: SelfNamespacedType,
        *,
        opaque_id: Union[DefaultType, str] = DEFAULT,
        api_key: Union[DefaultType, str, Tuple[str, str]] = DEFAULT,
        basic_auth: Union[DefaultType, str, Tuple[str, str]] = DEFAULT,
        bearer_auth: Union[DefaultType, str] = DEFAULT,
        headers: Union[DefaultType, Mapping[str, str]] = DEFAULT,
        request_timeout: Union[DefaultType, Optional[float]] = DEFAULT,
        ignore_status: Union[DefaultType, int, Collection[int]] = DEFAULT,
        max_retries: Union[DefaultType, int] = DEFAULT,
        retry_on_status: Union[DefaultType, int, Collection[int]] = DEFAULT,
        retry_on_timeout: Union[DefaultType, bool] = DEFAULT,
    ) -> SelfNamespacedType:
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

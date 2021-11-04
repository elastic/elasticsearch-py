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


import base64
import warnings
from datetime import date, datetime
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Collection,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from elastic_transport import AsyncTransport, NodeConfig, SniffOptions, Transport
from elastic_transport.client_utils import (
    DEFAULT,
    client_meta_version,
    parse_cloud_id,
    url_to_node_config,
)

from ..._version import __versionstr__
from ...compat import quote, string_types, to_bytes, to_str, warn_stacklevel
from ...serializer import Serializer

if TYPE_CHECKING:
    from ... import Elasticsearch
    from ._base import NamespacedClient

# parts of URL to be omitted
SKIP_IN_PATH: Collection[Any] = (None, "", b"", [], ())

# To be passed to 'client_meta_service' on the Transport
CLIENT_META_SERVICE = ("es", client_meta_version(__versionstr__))

_TYPE_HOSTS = Union[str, List[Union[str, Mapping[str, Union[str, int]], NodeConfig]]]

_TYPE_ASYNC_SNIFF_CALLBACK = Callable[
    [AsyncTransport, SniffOptions], Awaitable[List[NodeConfig]]
]
_TYPE_SYNC_SNIFF_CALLBACK = Callable[[Transport, SniffOptions], List[NodeConfig]]


def client_node_configs(
    hosts: _TYPE_HOSTS, cloud_id: str, **kwargs: Any
) -> List[NodeConfig]:
    if cloud_id is not None:
        if hosts is not None:
            raise ValueError(
                "The 'cloud_id' and 'hosts' parameters are mutually exclusive"
            )
        node_configs = cloud_id_to_node_configs(cloud_id)
    else:
        node_configs = hosts_to_node_configs(hosts)

    # Remove all values which are 'DEFAULT' to avoid overwriting actual defaults.
    node_options = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    return [node_config.replace(**node_options) for node_config in node_configs]


def hosts_to_node_configs(hosts: _TYPE_HOSTS) -> List[NodeConfig]:
    """Transforms the many formats of 'hosts' into NodeConfigs"""

    # To make the logic here simpler we reroute everything to be List[X]
    if not isinstance(hosts, (tuple, list)):
        return hosts_to_node_configs([hosts])

    node_configs: List[NodeConfig] = []
    for host in hosts:
        if isinstance(host, NodeConfig):
            node_configs.append(host)

        elif isinstance(host, str):
            node_configs.append(url_to_node_config(host))

        elif isinstance(host, Mapping):
            node_configs.append(host_mapping_to_node_config(host))
        else:
            raise ValueError(
                "'hosts' must be a list of URLs, NodeConfigs, or dictionaries"
            )

    return node_configs


def host_mapping_to_node_config(host: Mapping[str, Union[str, int]]) -> NodeConfig:
    """Converts an old-style dictionary host specification to a NodeConfig"""

    allow_hosts_keys = {
        "scheme",
        "host",
        "port",
        "path_prefix",
        "url_prefix",
        "use_ssl",
    }
    disallowed_keys = set(host.keys()).difference(allow_hosts_keys)
    if disallowed_keys:
        bad_keys_used = "', '".join(sorted(disallowed_keys))
        allowed_keys = "', '".join(sorted(allow_hosts_keys))
        raise ValueError(
            f"Can't specify the options '{bad_keys_used}' via a "
            f"dictionary in 'hosts', only '{allowed_keys}' options "
            "are allowed"
        )

    options = dict(host)

    # Handle the deprecated option 'use_ssl'
    if "use_ssl" in options:
        use_ssl = options.pop("use_ssl")
        if not isinstance(use_ssl, bool):
            raise TypeError("'use_ssl' must be of type 'bool'")

        # Ensure the user isn't specifying scheme=http use_ssl=True or vice-versa
        if "scheme" in options and (options["scheme"] == "https") != use_ssl:
            raise ValueError(
                f"Cannot specify conflicting options 'scheme={options['scheme']}' "
                f"and 'use_ssl={use_ssl}'. Use 'scheme' only instead"
            )

        warnings.warn(
            "The 'use_ssl' option is no longer needed as specifying a 'scheme' is now required",
            category=DeprecationWarning,
            stacklevel=warn_stacklevel(),
        )
        options.setdefault("scheme", "https" if use_ssl else "http")

    # Handle the deprecated option 'url_prefix'
    if "url_prefix" in options:
        if "path_prefix" in options:
            raise ValueError(
                "Cannot specify conflicting options 'url_prefix' and "
                "'path_prefix'. Use 'path_prefix' only instead"
            )

        warnings.warn(
            "The 'url_prefix' option is deprecated in favor of 'path_prefix'",
            category=DeprecationWarning,
            stacklevel=warn_stacklevel(),
        )
        options["path_prefix"] = options.pop("url_prefix")

    return NodeConfig(**options)  # type: ignore


def cloud_id_to_node_configs(cloud_id: str) -> List[NodeConfig]:
    """Transforms an Elastic Cloud ID into a NodeConfig"""
    es_addr = parse_cloud_id(cloud_id).es_address
    if es_addr is None or not all(es_addr):
        raise ValueError("Cloud ID missing host and port information for Elasticsearch")
    host, port = es_addr
    return [
        NodeConfig(
            scheme="https",
            host=host,
            port=port,
            http_compress=True,
        )
    ]


def _escape(value: Any) -> Union[bytes, str]:
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = ",".join(value)

    # dates and datetimes into isoformat
    elif isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    elif isinstance(value, bytes):
        return value

    # encode strings to utf-8
    if not isinstance(value, str):
        return str(value).encode("utf-8")
    return value.encode("utf-8")


def _make_path(*parts: Any) -> str:
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists and tuples to comma separated values.
    """
    # TODO: maybe only allow some parts to be lists/tuples ?
    return "/" + "/".join(
        # preserve ',' and '*' in url for nicer URLs in logs
        quote(_escape(p), b",*")
        for p in parts
        if p not in SKIP_IN_PATH
    )


# parameters that apply to all methods
GLOBAL_PARAMS: Tuple[str, ...] = (
    "pretty",
    "human",
    "error_trace",
    "format",
    "filter_path",
)
T = TypeVar("T")


def query_params(
    *es_query_params: str,
) -> Callable[[T], T]:
    """
    Decorator that pops all accepted parameters from method's kwargs and puts
    them in the params argument.
    """

    def _wrapper(func: Any) -> Any:
        @wraps(func)
        def _wrapped(*args: Any, **kwargs: Any) -> Any:
            params = (kwargs.pop("params", None) or {}).copy()
            headers = {
                k.lower(): v
                for k, v in (kwargs.pop("headers", None) or {}).copy().items()
            }

            if "opaque_id" in kwargs:
                headers["x-opaque-id"] = kwargs.pop("opaque_id")

            http_auth = kwargs.pop("http_auth", None)
            api_key = kwargs.pop("api_key", None)

            if http_auth is not None and api_key is not None:
                raise ValueError(
                    "Only one of 'http_auth' and 'api_key' may be passed at a time"
                )
            elif http_auth is not None:
                headers["authorization"] = f"Basic {_base64_auth_header(http_auth)}"
            elif api_key is not None:
                headers["authorization"] = f"ApiKey {_base64_auth_header(api_key)}"

            for p in es_query_params + GLOBAL_PARAMS:
                if p in kwargs:
                    v = kwargs.pop(p)
                    if v is not None:
                        params[p] = _escape(v)

            # don't treat ignore, request_timeout, and opaque_id as other params to avoid escaping
            for p in ("ignore", "request_timeout"):
                if p in kwargs:
                    params[p] = kwargs.pop(p)
            return func(*args, params=params, headers=headers, **kwargs)

        return _wrapped

    return _wrapper


def _bulk_body(
    serializer: Serializer, body: Union[str, bytes, Collection[Any]]
) -> Union[str, bytes]:
    # if not passed in a string, serialize items and join by newline
    if not isinstance(body, string_types):
        body = b"\n".join(map(serializer.dumps, body))

    # bulk body must end with a newline
    if isinstance(body, bytes):
        if not body.endswith(b"\n"):
            body += b"\n"
    elif isinstance(body, str) and not body.endswith("\n"):
        body += "\n"

    return body


def _base64_auth_header(
    auth_value: Union[List[str], Tuple[str, ...], str, bytes]
) -> str:
    """Takes either a 2-tuple or a base64-encoded string
    and returns a base64-encoded string to be used
    as an HTTP authorization header.
    """
    if isinstance(auth_value, (list, tuple)):
        auth_value = base64.b64encode(to_bytes(":".join(auth_value)))
    return to_str(auth_value)


def _deprecated_options(
    client: Union["Elasticsearch", "NamespacedClient"],
    params: Optional[MutableMapping[str, Any]],
) -> Tuple[Union["Elasticsearch", "NamespacedClient"], Optional[Mapping[str, Any]]]:
    """Applies the deprecated logic for per-request options. When passed deprecated options
    this function will convert them into a Elasticsearch.options() or encoded params"""

    if params:
        options_kwargs = {}
        opaque_id = params.pop("opaque_id", None)
        api_key = params.pop("api_key", None)
        http_auth = params.pop("http_auth", None)
        headers = {}
        if opaque_id is not None:
            headers["x-opaque-id"] = opaque_id
        if http_auth is not None and api_key is not None:
            raise ValueError(
                "Only one of 'http_auth' and 'api_key' may be passed at a time"
            )
        elif api_key is not None:
            options_kwargs["api_key"] = api_key
        elif http_auth is not None:
            options_kwargs["basic_auth"] = http_auth
        if headers:
            options_kwargs["headers"] = headers

        request_timeout = params.pop("request_timeout", None)
        if request_timeout is not None:
            options_kwargs["request_timeout"] = request_timeout

        ignore = params.pop("ignore", None)
        if ignore is not None:
            options_kwargs["ignore_status"] = ignore

        if options_kwargs:
            warnings.warn(
                "Passing transport options in the API method is deprecated. Use 'Elasticsearch.options()' instead.",
                category=DeprecationWarning,
                stacklevel=warn_stacklevel(),
            )

            # Namespaced clients need to unwrapped.
            namespaced_client: Optional[Type["NamespacedClient"]] = None
            if hasattr(client, "_client"):
                namespaced_client = type(client)  # type: ignore[assignment]
                client = client._client  # type: ignore[attr-defined,assignment,union-attr]

            client = client.options(**options_kwargs)

            # Re-wrap the client if we unwrapped due to being namespaced.
            if namespaced_client is not None:
                client = namespaced_client(client)

        # If there are any query params left we warn about API parameters.
        if params:
            warnings.warn(
                "Passing options via 'params' is deprecated, instead use API parameters directly.",
                category=DeprecationWarning,
                stacklevel=warn_stacklevel(),
            )

    return client, params or None

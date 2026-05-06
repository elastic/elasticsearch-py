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

import inspect
from typing import (
    TYPE_CHECKING,
    Any,
)

from elastic_transport import HttpxAsyncHttpNode
from elastic_transport.client_utils import DEFAULT

from ..._sync.client.utils import (
    _TYPE_ASYNC_SNIFF_CALLBACK,
    _TYPE_HOSTS,
    CLIENT_META_SERVICE,
    SKIP_IN_PATH,
    Stability,
    Visibility,
    _availability_warning,
    _base64_auth_header,
    _quote,
    _quote_query,
    _rewrite_parameters,
    client_node_configs,
    is_requests_http_auth,
    is_requests_node_class,
)


def is_httpx_http_auth(http_auth: Any) -> bool:
    """Detect if an http_auth value is a custom Httpx auth object"""
    try:
        from httpx import Auth

        return isinstance(http_auth, Auth)
    except ImportError:
        pass
    return False


def is_httpx_node_class(node_class: Any) -> bool:
    """Detect if 'HttpxAsyncHttpNode' would be used given the setting of 'node_class'"""
    return (
        node_class is not None
        and node_class is not DEFAULT
        and (
            node_class == "httpxasync"
            or (
                inspect.isclass(node_class)
                and issubclass(node_class, HttpxAsyncHttpNode)
            )
        )
    )


__all__ = [
    "CLIENT_META_SERVICE",
    "_TYPE_ASYNC_SNIFF_CALLBACK",
    "_base64_auth_header",
    "_quote",
    "_quote_query",
    "_TYPE_HOSTS",
    "SKIP_IN_PATH",
    "Stability",
    "Visibility",
    "client_node_configs",
    "_rewrite_parameters",
    "_availability_warning",
    "is_requests_http_auth",
    "is_requests_node_class",
    "is_httpx_http_auth",
    "is_httpx_node_class",
]

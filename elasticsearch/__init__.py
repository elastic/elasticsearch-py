# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

# flake8: noqa
from __future__ import absolute_import

VERSION = (8, 0, 0)
__version__ = VERSION
__versionstr__ = ".".join(map(str, VERSION))

import sys
import logging
import warnings

logger = logging.getLogger("elasticsearch")
logger.addHandler(logging.NullHandler())

from .client import Elasticsearch
from .transport import Transport
from .connection_pool import ConnectionPool, ConnectionSelector, RoundRobinSelector
from .serializer import JSONSerializer
from .connection import Connection, RequestsHttpConnection, Urllib3HttpConnection
from .exceptions import (
    ImproperlyConfigured,
    ElasticsearchException,
    SerializationError,
    TransportError,
    NotFoundError,
    ConflictError,
    RequestError,
    ConnectionError,
    SSLError,
    ConnectionTimeout,
    AuthenticationException,
    AuthorizationException,
    ElasticsearchDeprecationWarning,
)

# Only raise one warning per deprecation message so as not
# to spam up the user if the same action is done multiple times.
warnings.simplefilter("default", category=ElasticsearchDeprecationWarning, append=True)

__all__ = [
    "Elasticsearch",
    "Transport",
    "ConnectionPool",
    "ConnectionSelector",
    "RoundRobinSelector",
    "JSONSerializer",
    "Connection",
    "RequestsHttpConnection",
    "Urllib3HttpConnection",
    "ImproperlyConfigured",
    "ElasticsearchException",
    "SerializationError",
    "TransportError",
    "NotFoundError",
    "ConflictError",
    "RequestError",
    "ConnectionError",
    "SSLError",
    "ConnectionTimeout",
    "AuthenticationException",
    "AuthorizationException",
    "ElasticsearchDeprecationWarning",
]

try:
    # Asyncio only supported on Python 3.6+
    if sys.version_info < (3, 6):
        raise ImportError

    from ._async.http_aiohttp import AIOHttpConnection
    from ._async.transport import AsyncTransport
    from ._async.client import AsyncElasticsearch

    __all__ += ["AIOHttpConnection", "AsyncTransport", "AsyncElasticsearch"]
except (ImportError, SyntaxError):
    pass

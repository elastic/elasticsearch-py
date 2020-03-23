# flake8: noqa
from __future__ import absolute_import

VERSION = (8, 0, 0)
__version__ = VERSION
__versionstr__ = ".".join(map(str, VERSION))

import logging

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
)

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
]

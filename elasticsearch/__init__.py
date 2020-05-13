# flake8: noqa
from __future__ import absolute_import

VERSION = (7, 7, 0)
__version__ = VERSION
__versionstr__ = "7.7.0"

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

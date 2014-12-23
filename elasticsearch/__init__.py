from __future__ import absolute_import

VERSION = (1, 2, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

import logging

from .client import Elasticsearch
from .transport import Transport
from .connection_pool import ConnectionPool, ConnectionSelector, \
    RoundRobinSelector
from .serializer import JSONSerializer
from .connection import Connection, RequestsHttpConnection, \
    Urllib3HttpConnection, MemcachedConnection, ThriftConnection
from .exceptions import *

logger = logging.getLogger('elasticsearch')
logger.addHandler(logging.NullHandler())
    # Install no-op handler per
    # <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>


# flake8: noqa
from __future__ import absolute_import

VERSION = (7, 6, 0)
__version__ = VERSION
__versionstr__ = ".".join(map(str, VERSION))

import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


import sys

logger = logging.getLogger("elasticsearch")
logger.addHandler(logging.NullHandler())

from .client import Elasticsearch
from .transport import Transport
from .connection_pool import ConnectionPool, ConnectionSelector, RoundRobinSelector
from .serializer import JSONSerializer
from .connection import Connection, RequestsHttpConnection, Urllib3HttpConnection
from .exceptions import *

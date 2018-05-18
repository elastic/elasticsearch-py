from __future__ import absolute_import

VERSION = (6, 2, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

import sys

if sys.version_info[:2] == (2, 7):
    # On Python 2.7, install no-op handler to silence
    # `No handlers could be found for logger "elasticsearch"` message per
    # <https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library>
    import logging
    logger = logging.getLogger('elasticsearch')
    logger.addHandler(logging.NullHandler())

from .client import Elasticsearch
from .transport import Transport
from .connection_pool import ConnectionPool, ConnectionSelector, \
    RoundRobinSelector
from .serializer import JSONSerializer
from .connection import Connection, RequestsHttpConnection, \
    Urllib3HttpConnection
from .exceptions import *


from .base import Connection
from .http_requests import RequestsHttpConnection
from .http_urllib3 import Urllib3HttpConnection
from .memcached import MemcachedConnection
from .thrift import ThriftConnection, THRIFT_AVAILABLE

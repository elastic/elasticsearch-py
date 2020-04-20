from .client import Elasticsearch
from .connection_pool import AsyncConnectionPool, AsyncDummyConnectionPool
from .transport import AsyncTransport
from .http_aiohttp import AIOHttpConnection


class AsyncElasticsearch(Elasticsearch):
    """This is only for the rename of the class"""


__all__ = [
    "AsyncElasticsearch",
    "AsyncConnectionPool",
    "AsyncDummyConnectionPool",
    "AsyncTransport",
    "AIOHttpConnection",
]

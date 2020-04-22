from .client import Elasticsearch
from .connection_pool import AsyncConnectionPool, AsyncDummyConnectionPool
from .transport import AsyncTransport
from .http_aiohttp import AIOHttpConnection


class AsyncElasticsearch(Elasticsearch):
    # This class def is for both the name 'AsyncElasticsearch'
    # and all async-only additions to the class.
    async def __aenter__(self):
        await self.transport._async_call()
        return self


__all__ = [
    "AsyncElasticsearch",
    "AsyncConnectionPool",
    "AsyncDummyConnectionPool",
    "AsyncTransport",
    "AIOHttpConnection",
]

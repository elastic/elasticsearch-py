# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

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


AsyncElasticsearch.__doc__ = Elasticsearch.__doc__


__all__ = [
    "AsyncElasticsearch",
    "AsyncConnectionPool",
    "AsyncDummyConnectionPool",
    "AsyncTransport",
    "AIOHttpConnection",
]

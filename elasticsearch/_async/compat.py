# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import asyncio
from ..compat import *  # noqa: F401,F403

# Hack supporting Python 3.6 asyncio which didn't have 'get_running_loop()'.
# Essentially we want to get away from having users pass in a loop to us.
# Instead we should call 'get_running_loop()' whenever we need
# the currently running loop.
# See: https://aiopg.readthedocs.io/en/stable/run_loop.html#implementation
try:
    from asyncio import get_running_loop
except ImportError:

    def get_running_loop():
        loop = asyncio.get_event_loop()
        if not loop.is_running():
            raise RuntimeError("no running event loop")
        return loop


def get_sleep():
    loop = get_running_loop()

    async def sleep(duration):
        await asyncio.sleep(duration, loop=loop)

    return sleep


def azip(*iterables):
    iterators = [aiter(x) for x in iterables]

    async def generator():
        while True:
            try:
                yield tuple([await i.__anext__() for i in iterators])
            except StopAsyncIteration:
                break

    return generator().__aiter__()


def aiter(x):
    """Creates an async iterator out of async or sync iterables
    and iterators. Map the 'aiter' token to 'iter'
    """
    if hasattr(x, "__aiter__"):
        return x.__aiter__()
    elif hasattr(x, "__anext__"):
        return x

    async def aiter_wrapper():
        for item in x:
            yield item

    return aiter_wrapper().__aiter__()

# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import asyncio
from ..compat import *  # noqa

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


__all__ = ["get_running_loop"]

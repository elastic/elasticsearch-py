import logging

from .compat import get_running_loop
from .http_aiohttp import AIOHttpConnection
from .connection_pool import AsyncConnectionPool, AsyncDummyConnectionPool
from ..transport import Transport
from ..exceptions import TransportError, ConnectionTimeout


logger = logging.getLogger("elasticsearch")


class AsyncTransport(Transport):
    DEFAULT_CONNECTION_CLASS = AIOHttpConnection
    DEFAULT_CONNECTION_POOL = AsyncConnectionPool
    DUMMY_CONNECTION_POOL = AsyncDummyConnectionPool

    def __init__(self, *args, **kwargs):
        self.sniffing_task = None
        self.loop = None
        self._async_started = False

        super(AsyncTransport, self).__init__(*args, **kwargs)

    async def _async_start(self):
        if self._async_started:
            return
        self._async_started = True

        # Detect the async loop we're running in and set it
        # on all already created HTTP connections.
        self.loop = get_running_loop()
        self.kwargs["loop"] = self.loop
        for connection in self.connection_pool.connections:
            connection.loop = self.loop

    async def close(self):
        if getattr(self, "sniffing_task", None):
            self.sniffing_task.cancel()
        await self.connection_pool.close()

    async def perform_request(self, method, url, headers=None, params=None, body=None):
        await self._async_start()

        params, body, ignore, timeout = self._resolve_request_args(method, params, body)

        for attempt in range(self.max_retries + 1):
            connection = self.get_connection()

            try:
                status, headers, data = await connection.perform_request(
                    method,
                    url,
                    params,
                    body,
                    headers=headers,
                    ignore=ignore,
                    timeout=timeout,
                )
            except TransportError as e:
                if method == "HEAD" and e.status_code == 404:
                    return False

                retry = False
                if isinstance(e, ConnectionTimeout):
                    retry = self.retry_on_timeout
                elif isinstance(e, ConnectionError):
                    retry = True
                elif e.status_code in self.retry_on_status:
                    retry = True

                if retry:
                    # only mark as dead if we are retrying
                    self.mark_dead(connection)
                    # raise exception on last retry
                    if attempt == self.max_retries:
                        raise
                else:
                    raise

            else:
                if method == "HEAD":
                    return 200 <= status < 300

                # connection didn't fail, confirm it's live status
                self.connection_pool.mark_live(connection)
                if data:
                    data = self.deserializer.loads(data, headers.get("content-type"))
                return data

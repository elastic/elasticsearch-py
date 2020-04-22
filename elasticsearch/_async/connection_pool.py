from ..connection_pool import ConnectionPool
from ..exceptions import ImproperlyConfigured


class AsyncConnectionPool(ConnectionPool):
    async def close(self):
        """
        Explicitly closes connections
        """
        for conn in self.connections:
            await conn.close()


class AsyncDummyConnectionPool(AsyncConnectionPool):
    def __init__(self, connections, **kwargs):
        if len(connections) != 1:
            raise ImproperlyConfigured(
                "DummyConnectionPool needs exactly one connection defined."
            )
        # we need connection opts for sniffing logic
        self.connection_opts = connections
        self.connection = connections[0][0]
        self.connections = (self.connection,)

    async def close(self):
        """
        Explicitly closes connections
        """
        await self.connection.close()

    def _noop(self, *args, **kwargs):
        pass

    mark_dead = mark_live = resurrect = _noop

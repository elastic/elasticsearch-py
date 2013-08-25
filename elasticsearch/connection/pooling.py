from .base import Connection

class PoolingConnection(Connection):
    def __init__(self, *args, **kwargs):
        self._max_pool_size = kwargs.pop('max_connection_pool_size', 50)
        self._free_connections = []
        self._in_use_connections = set()
        super(PoolingConnection, self).__init__(*args, **kwargs)

    def _get_connection(self):
        try:
            con = self._free_connections.pop()
        except IndexError:
            con = self._make_connection()

        self._in_use_connections.add(con)
        return con

    def _release_connection(self, con):
        self._in_use_connections.remove(con)
        self._free_connections.append(con)


from Queue import Queue
from .base import Connection


class PoolingConnection(Connection):
    def __init__(self, *args, **kwargs):
        self._free_connections = Queue()
        super(PoolingConnection, self).__init__(*args, **kwargs)

    def _get_connection(self):
        return self._make_connection() if self._free_connections.empty() else self._free_connections.get()

    def _release_connection(self, con):
        self._free_connections.put(con)
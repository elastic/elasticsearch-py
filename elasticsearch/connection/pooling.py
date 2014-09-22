try:
    import queue
except ImportError:
    import Queue as queue
from .base import Connection


class PoolingConnection(Connection):
    def __init__(self, *args, **kwargs):
        self._free_connections = queue.Queue()
        super(PoolingConnection, self).__init__(*args, **kwargs)

    def _get_connection(self):
        try:
            return self._free_connections.get_nowait()
        except queue.Empty:
            return self._make_connection()

    def _release_connection(self, con):
        self._free_connections.put(con)
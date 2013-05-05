import time
import random

try:
    from Queue import PriorityQueue
except ImportError:
    from queue import PriorityQueue

class ConnectionSelector(object):
    " Base class for Selectors. "
    def __init__(self, opts):
        self.connection_opts = opts


class RoundRobinSelector(ConnectionSelector):
    " Default selector using round-robin. "
    def __init__(self, opts):
        super(RoundRobinSelector, self).__init__(opts)
        self.rr = -1

    def select(self, connections):
        self.rr += 1
        self.rr %= len(connections)
        return connections[self.rr]


class ConnectionPool(object):
    def __init__(self, connections, dead_timeout=60, selector_class=RoundRobinSelector, randomize_hosts=True, **kwargs):
        self.connections = [c for (c, opts) in connections]
        self.dead = PriorityQueue(len(self.connections))
        self.dead_count = {}

        if randomize_hosts:
            # randomize the connection list to avoid all clients hitting same node
            # after startup/restart
            random.shuffle(self.connections)

        # default timeout after which to try resurrecting a connection
        self.dead_timeout = dead_timeout

        self.selector = selector_class(dict(connections))

    def mark_dead(self, connection, dead_count, now=None):
        # allow inject for testing purposes
        now = now if now else time.time()
        try:
            self.connections.remove(connection)
        except ValueError:
            # connection not alive or another thread marked it already, ignore
            return
        else:
            self.dead_count[connection] = dead_count
            self.dead.put((now + self.dead_timeout * 2 ** (dead_count - 1), connection))

    def mark_live(self, connection):
        try:
            del self.dead_count[connection]
        except KeyError:
            # race condition, safe to ignore
            pass

    def resurrect(self, force=False):
        # no dead connections
        if self.dead.empty():
            return

        # retrieve a connection to check
        timeout, connection = self.dead.get()

        if not force and timeout > time.time():
            # return it back if not eligible and not forced
            self.dead.put((timeout, connection))
            return

        # either we were forced or the connection is elligible to be retried
        self.connections.append(connection)

    def get_connection(self):
        self.resurrect()

        # no live nodes, resurrect one by force
        if not self.connections:
            self.resurrect(True)

        connection = self.selector.select(self.connections)

        return connection, self.dead_count.get(connection, 0)



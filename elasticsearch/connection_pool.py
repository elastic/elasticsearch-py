import time
import random

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
        self.dead = []

        if randomize_hosts:
            # randomize the connection list to avoid all clients hitting same node
            # after startup/restart
            random.shuffle(self.connections)

        # default timeout after which to try resurrecting a connection
        self.dead_timeout = dead_timeout

        self.selector = selector_class(dict(connections))

    def mark_dead(self, connection, now=None):
        # allow inject for testing purposes
        now = now if now else time.time()
        try:
            self.connections.remove(connection)
        except ValueError:
            # connection not alive, ignore
            return

        # TODO: detect repeated failure and extend the timeout
        self.dead.append((now + self.dead_timeout, connection))

    def resurrect(self, force=False):
        # no dead connections
        if not self.dead:
            return

        # no elligible connections to retry
        if not force and self.dead[0][0] > time.time():
            return

        # either we were forced or the node is elligible to be retried
        connection = self.dead.pop(0)[1]
        self.connections.append(connection)
        return connection

    def get_connection(self):
        connection = self.resurrect()
        if connection:
            return connection

        # no live nodes, resurrect one by force
        if not self.connections:
            return self.resurrect(True)

        return self.selector.select(self.connections)



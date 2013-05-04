import time
from unittest import TestCase

from elasticsearch.connection_pool import ConnectionPool, RoundRobinSelector

class TestConnectionPool(TestCase):
    def test_default_round_robin(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])

        connections = set()
        for _ in range(100):
            connections.add(pool.get_connection())
        self.assertEquals(connections, set(range(100)))

    def test_disable_shuffling(self):
        pool = ConnectionPool([(x, {}) for x in range(100)], randomize_hosts=False)

        connections = []
        for _ in range(100):
            connections.append(pool.get_connection())
        self.assertEquals(connections, list(range(100)))

    def test_selectors_have_access_to_connection_opts(self):
        class MySelector(RoundRobinSelector):
            def select(self, connections):
                return self.connection_opts[super(MySelector, self).select(connections)]
        pool = ConnectionPool([(x, {"number": x}) for x in range(100)], selector_class=MySelector, randomize_hosts=False)

        connections = []
        for _ in range(100):
            connections.append(pool.get_connection())
        self.assertEquals(connections, [{"number": x} for x in range(100)])

    def test_dead_nodes_are_removed_from_active_connections(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])

        now = time.time()
        pool.mark_dead(42, now=now)
        self.assertEquals(99, len(pool.connections))
        self.assertEquals(1, pool.dead.qsize())
        self.assertEquals((now + 60, 42), pool.dead.get())

    def test_connection_is_skipped_when_dead(self):
        pool = ConnectionPool([(x, {}) for x in range(2)])
        pool.mark_dead(0)

        self.assertEquals([1, 1, 1], [pool.get_connection(), pool.get_connection(), pool.get_connection(), ])

    def test_connection_is_forcibly_resurrected_when_no_live_ones_are_availible(self):
        pool = ConnectionPool([(x, {}) for x in range(2)])
        pool.mark_dead(0)
        pool.mark_dead(1)

        self.assertEquals([], pool.connections)
        self.assertEquals(0, pool.get_connection())
        self.assertEquals([0,], pool.connections)

    def test_connection_is_resurrected_after_its_timeout(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])

        now = time.time()
        pool.mark_dead(42, now=now-61)
        pool.get_connection()
        self.assertEquals(42, pool.connections[-1])
        self.assertEquals(100, len(pool.connections))


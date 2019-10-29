import time

from elasticsearch.connection_pool import (
    ConnectionPool,
    RoundRobinSelector,
    DummyConnectionPool,
)
from elasticsearch.connection import Connection
from elasticsearch.exceptions import ImproperlyConfigured

from .test_cases import TestCase


class TestConnectionPool(TestCase):
    def test_dummy_cp_raises_exception_on_more_connections(self):
        self.assertRaises(ImproperlyConfigured, DummyConnectionPool, [])
        self.assertRaises(
            ImproperlyConfigured, DummyConnectionPool, [object(), object()]
        )

    def test_raises_exception_when_no_connections_defined(self):
        self.assertRaises(ImproperlyConfigured, ConnectionPool, [])

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
                return self.connection_opts[
                    super(MySelector, self).select(connections)
                ]["actual"]

        pool = ConnectionPool(
            [(x, {"actual": x * x}) for x in range(100)],
            selector_class=MySelector,
            randomize_hosts=False,
        )

        connections = []
        for _ in range(100):
            connections.append(pool.get_connection())
        self.assertEquals(connections, [x * x for x in range(100)])

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

        self.assertEquals(
            [1, 1, 1],
            [pool.get_connection(), pool.get_connection(), pool.get_connection()],
        )

    def test_new_connection_is_not_marked_dead(self):
        # Create 10 connections
        pool = ConnectionPool([(Connection(), {}) for _ in range(10)])

        # Pass in a new connection that is not in the pool to mark as dead
        new_connection = Connection()
        pool.mark_dead(new_connection)

        # Nothing should be marked dead
        self.assertEquals(0, len(pool.dead_count))

    def test_connection_is_forcibly_resurrected_when_no_live_ones_are_availible(self):
        pool = ConnectionPool([(x, {}) for x in range(2)])
        pool.dead_count[0] = 1
        pool.mark_dead(0)  # failed twice, longer timeout
        pool.mark_dead(1)  # failed the first time, first to be resurrected

        self.assertEquals([], pool.connections)
        self.assertEquals(1, pool.get_connection())
        self.assertEquals([1], pool.connections)

    def test_connection_is_resurrected_after_its_timeout(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])

        now = time.time()
        pool.mark_dead(42, now=now - 61)
        pool.get_connection()
        self.assertEquals(42, pool.connections[-1])
        self.assertEquals(100, len(pool.connections))

    def test_force_resurrect_always_returns_a_connection(self):
        pool = ConnectionPool([(0, {})])

        pool.connections = []
        self.assertEquals(0, pool.get_connection())
        self.assertEquals([], pool.connections)
        self.assertTrue(pool.dead.empty())

    def test_already_failed_connection_has_longer_timeout(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])
        now = time.time()
        pool.dead_count[42] = 2
        pool.mark_dead(42, now=now)

        self.assertEquals(3, pool.dead_count[42])
        self.assertEquals((now + 4 * 60, 42), pool.dead.get())

    def test_timeout_for_failed_connections_is_limitted(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])
        now = time.time()
        pool.dead_count[42] = 245
        pool.mark_dead(42, now=now)

        self.assertEquals(246, pool.dead_count[42])
        self.assertEquals((now + 32 * 60, 42), pool.dead.get())

    def test_dead_count_is_wiped_clean_for_connection_if_marked_live(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])
        now = time.time()
        pool.dead_count[42] = 2
        pool.mark_dead(42, now=now)

        self.assertEquals(3, pool.dead_count[42])
        pool.mark_live(42)
        self.assertNotIn(42, pool.dead_count)

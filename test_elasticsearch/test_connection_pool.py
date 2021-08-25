#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import time

import pytest

from elasticsearch.connection import Connection
from elasticsearch.connection_pool import (
    ConnectionPool,
    DummyConnectionPool,
    RoundRobinSelector,
)
from elasticsearch.exceptions import ImproperlyConfigured


class TestConnectionPool:
    def test_dummy_cp_raises_exception_on_more_connections(self):
        with pytest.raises(ImproperlyConfigured):
            DummyConnectionPool([])
        with pytest.raises(ImproperlyConfigured):
            DummyConnectionPool([object(), object()])

    def test_raises_exception_when_no_connections_defined(self):
        with pytest.raises(ImproperlyConfigured):
            ConnectionPool([])

    def test_default_round_robin(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])

        connections = set()
        for _ in range(100):
            connections.add(pool.get_connection())
        assert connections == set(range(100))

    def test_disable_shuffling(self):
        pool = ConnectionPool([(x, {}) for x in range(100)], randomize_hosts=False)

        connections = []
        for _ in range(100):
            connections.append(pool.get_connection())
        assert connections == list(range(100))

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
        assert connections == [x * x for x in range(100)]

    def test_dead_nodes_are_removed_from_active_connections(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])

        now = time.time()
        pool.mark_dead(42, now=now)
        assert 99 == len(pool.connections)
        assert 1 == pool.dead.qsize()
        assert (now + 60, 42) == pool.dead.get()

    def test_connection_is_skipped_when_dead(self):
        pool = ConnectionPool([(x, {}) for x in range(2)])
        pool.mark_dead(0)

        assert [1, 1, 1] == [
            pool.get_connection(),
            pool.get_connection(),
            pool.get_connection(),
        ]

    def test_new_connection_is_not_marked_dead(self):
        # Create 10 connections
        pool = ConnectionPool([(Connection(), {}) for _ in range(10)])

        # Pass in a new connection that is not in the pool to mark as dead
        new_connection = Connection()
        pool.mark_dead(new_connection)

        # Nothing should be marked dead
        assert 0 == len(pool.dead_count)

    def test_connection_is_forcibly_resurrected_when_no_live_ones_are_availible(self):
        pool = ConnectionPool([(x, {}) for x in range(2)])
        pool.dead_count[0] = 1
        pool.mark_dead(0)  # failed twice, longer timeout
        pool.mark_dead(1)  # failed the first time, first to be resurrected

        assert [] == pool.connections
        assert 1 == pool.get_connection()
        assert [1] == pool.connections

    def test_connection_is_resurrected_after_its_timeout(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])

        now = time.time()
        pool.mark_dead(42, now=now - 61)
        pool.get_connection()
        assert 42 == pool.connections[-1]
        assert 100 == len(pool.connections)

    def test_force_resurrect_always_returns_a_connection(self):
        pool = ConnectionPool([(0, {})])

        pool.connections = []
        assert 0 == pool.get_connection()
        assert [] == pool.connections
        assert pool.dead.empty()

    def test_already_failed_connection_has_longer_timeout(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])
        now = time.time()
        pool.dead_count[42] = 2
        pool.mark_dead(42, now=now)

        assert 3 == pool.dead_count[42]
        assert (now + 4 * 60, 42) == pool.dead.get()

    def test_timeout_for_failed_connections_is_limitted(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])
        now = time.time()
        pool.dead_count[42] = 245
        pool.mark_dead(42, now=now)

        assert 246 == pool.dead_count[42]
        assert (now + 32 * 60, 42) == pool.dead.get()

    def test_dead_count_is_wiped_clean_for_connection_if_marked_live(self):
        pool = ConnectionPool([(x, {}) for x in range(100)])
        now = time.time()
        pool.dead_count[42] = 2
        pool.mark_dead(42, now=now)

        assert 3 == pool.dead_count[42]
        pool.mark_live(42)
        assert 42 not in pool.dead_count

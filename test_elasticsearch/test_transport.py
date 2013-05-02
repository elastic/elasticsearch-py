from unittest import TestCase

from elasticsearch.transport import Transport
from elasticsearch.connection import Connection
from elasticsearch.exceptions import TransportError

class DummyConnection(Connection):
    def __init__(self, **kwargs):
        self.exception = kwargs.pop('exception', None)
        self.status, self.data = kwargs.pop('status', 200), kwargs.pop('data', '{}')
        self.calls = []
        super(DummyConnection, self).__init__(**kwargs)

    def perform_request(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if self.exception:
            raise self.exception
        return self.status, self.data

class TestTransport(TestCase):
    def test_kwargs_passed_on_to_connections(self):
        t = Transport([{'host': 'google.com'}], port=123)
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertEquals('http://google.com:123', t.connection_pool.connections[0].host)

    def test_kwargs_passed_on_to_connection_pool(self):
        dt = object()
        t = Transport([{}], dead_timeout=dt)
        self.assertIs(dt, t.connection_pool.dead_timeout)

    def test_custom_connection_class(self):
        class MyConnection(object):
            def __init__(self, **kwargs):
                self.kwargs = kwargs
        t = Transport([{}], connection_class=MyConnection)
        self.assertEquals(1, len(t.connection_pool.connections))
        self.assertIsInstance(t.connection_pool.connections[0], MyConnection)

    def test_add_connection(self):
        t = Transport([{}], randomize_hosts=False)
        t.add_connection({"host": "google.com"})

        self.assertEquals(2, len(t.connection_pool.connections))
        self.assertEquals('http://google.com:9200', t.connection_pool.connections[1].host)

    def test_request_will_fail_after_X_retries(self):
        t = Transport([{'exception': TransportError('abandon ship')}], connection_class=DummyConnection)

        self.assertRaises(TransportError, t.perform_request, 'GET', '/')
        self.assertEquals(3, len(t.connection_pool.get_connection().calls))

    def test_failed_connection_will_be_marked_as_dead(self):
        t = Transport([{'exception': TransportError('abandon ship')}], connection_class=DummyConnection)

        self.assertRaises(TransportError, t.perform_request, 'GET', '/')
        self.assertEquals(0, len(t.connection_pool.connections))


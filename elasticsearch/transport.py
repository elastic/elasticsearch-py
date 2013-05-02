from .connection import RequestsHttpConnection
from .connection_pool import ConnectionPool
from .serializer import JSONSerializer
from .exceptions import TransportError

class Transport(object):
    def __init__(self, hosts, connection_class=RequestsHttpConnection,
        connection_pool_class=ConnectionPool, serializer=JSONSerializer(),
        max_retries=3, **kwargs):

        self.max_retries = 3

        # data serializer
        self.serializer = serializer

        # store all strategies...
        self.connection_pool_class = connection_pool_class
        self.connection_class = connection_class

        # ...save kwargs to be passed to the connections
        self.kwargs = kwargs
        self.hosts = hosts

        # ...and instantiate them
        self.set_connections(hosts)

    def add_connection(self, host):
        self.hosts.append(host)
        self.set_connections(self.hosts)

    def set_connections(self, hosts):
        # construct the connections
        def _create_connection(host):
            kwargs = self.kwargs.copy()
            kwargs.update(host)
            return self.connection_class(**kwargs)
        connections = list(map(_create_connection, hosts))

        # pass the hosts dicts to the connection pool to optionally extract parameters from
        self.connection_pool = self.connection_pool_class(zip(connections, hosts), **self.kwargs)

    def perform_request(self, method, url, params=None, body=None):
        for attempt in range(self.max_retries):
            connection = self.connection_pool.get_connection()

            if body:
                body = self.serializer.dumps(body)
            try:
                status, raw_data = connection.perform_request(method, url, params, body)
            except TransportError:
                self.connection_pool.mark_dead(connection)

                # raise exception on last retry
                if attempt + 1 == self.max_retries:
                    raise
            else:
                return status, self.serializer.loads(raw_data)


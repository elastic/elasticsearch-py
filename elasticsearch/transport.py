import re

from .connection import RequestsHttpConnection
from .connection_pool import ConnectionPool
from .serializer import JSONSerializer
from .exceptions import TransportError

# get ip/port from "inet[wind/127.0.0.1:9200]"
ADDRESS_RE = re.compile(r'/(?P<host>[^:]*):(?P<port>[0-9]+)\]')

def construct_hosts_list(nodes, transport):
    hosts = []
    address = '%s_address' % transport
    for n in nodes.values():
        match = ADDRESS_RE.search(n.get(address, ''))
        if match:
            hosts.append(match.groupdict())
    return hosts

class Transport(object):
    def __init__(self, hosts, connection_class=RequestsHttpConnection,
        connection_pool_class=ConnectionPool, nodes_to_host_callback=construct_hosts_list,
        sniff_on_start=False, sniff_after_requests=None,
        sniff_on_connection_fail=False, serializer=JSONSerializer(),
        max_retries=3, **kwargs):

        self.max_retries = max_retries

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

        # sniffing data
        self.req_counter = 0
        self.sniffs_due_to_failure = 0
        self.sniff_after_requests_original = sniff_after_requests
        self.sniff_after_requests = sniff_after_requests
        self.sniff_on_connection_fail = sniff_on_connection_fail

        # callback to construct hosts dicts from /_cluster/nodes data
        self.nodes_to_host_callback = nodes_to_host_callback

        if sniff_on_start:
            self.sniff_hosts()

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

    def get_connection(self, sniffing=False):
        if not sniffing and self.sniff_after_requests:
            if self.req_counter >= self.sniff_after_requests:
                self.sniff_hosts()
            self.req_counter += 1
        return self.connection_pool.get_connection()

    def sniff_hosts(self, failure=False):
        # set the counter to 0 first so that perform_request doesn't trigger an
        # infinite loop
        self.req_counter = 0
        _, node_info = self.perform_request('GET', '/_cluster/nodes', sniffing=True)
        hosts = self.nodes_to_host_callback(node_info['nodes'], self.connection_class.transport_schema)
        self.set_connections(hosts)

        # when sniffing due to failure, shorten the period between sniffs progressively
        if failure:
            self.sniffs_due_to_failure += 1
            if self.sniff_after_requests:
                self.sniff_after_requests = 1 + self.sniff_after_requests_original // 2**self.sniffs_due_to_failure
        else:
            self.sniffs_due_to_failure = 0
            self.sniff_after_requests = self.sniff_after_requests_original

    def mark_dead(self, connection, sniffing=False):
        if not sniffing and self.sniff_on_connection_fail:
            self.sniff_hosts(True)
        else:
            self.connection_pool.mark_dead(connection)

    def perform_request(self, method, url, params=None, body=None, sniffing=False):
        for attempt in range(self.max_retries):
            connection = self.get_connection(sniffing)

            if body:
                body = self.serializer.dumps(body)
            try:
                status, raw_data = connection.perform_request(method, url, params, body)
            except TransportError:
                self.mark_dead(connection, sniffing)

                # raise exception on last retry
                if attempt + 1 == self.max_retries:
                    raise
            else:
                return status, self.serializer.loads(raw_data)


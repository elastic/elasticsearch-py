import re

from .connection import RequestsHttpConnection
from .connection_pool import ConnectionPool
from .serializer import JSONSerializer
from .exceptions import TransportError

# get ip/port from "inet[wind/127.0.0.1:9200]"
ADDRESS_RE = re.compile(r'/(?P<host>[^:]*):(?P<port>[0-9]+)\]')

def construct_hosts_list(nodes, transport):
    """
    Simple callback that trasnforms the output of `/_cluster/nodes` to a format
    accepted by :class:`~elasticsearch.Transport`.

    :arg nodes: deserialized output of the API call
    :arg transport: the transport schema used (usually 'http'). Used to locate
        appropriate address in the node info.
    """
    hosts = []
    address = '%s_address' % transport
    for n in nodes.values():
        match = ADDRESS_RE.search(n.get(address, ''))
        if match:
            hosts.append(match.groupdict())
    return hosts

class Transport(object):
    """
    Encapsulation of transport-related to logic. Handles instantiation of the
    individual connections as well as creating a connection pool to hold them.

    Main interface is the `perform_request` method.
    """
    def __init__(self, hosts, connection_class=RequestsHttpConnection,
        connection_pool_class=ConnectionPool, nodes_to_host_callback=construct_hosts_list,
        sniff_on_start=False, sniff_after_requests=None,
        sniff_on_connection_fail=False, serializer=JSONSerializer(),
        max_retries=3, **kwargs):
        """
        :arg hosts: list of dictionaries, each containing keyword arguments to
            create a `connection_class` instance
        :arg connection_class: subclass of :class:`~elasticsearch.Connection` to use
        :arg connection_pool_class: subclass of :class:`~elasticsearch.ConnectionPool` to use
        :arg nodes_to_host_callback: callback responsible for taking the output
            of `/_cluser/nodes` and producing a list of arguments (same as `hosts`
            parameter)
        :arg sniff_on_start: flag indicating whether to obtain a list of nodes
            from the cluser at startup time
        :arg sniff_after_requests: number of requests after which a sniffing should be initialized
        :arg sniff_on_connection_fail: flasg controlling if connection failure triggers a sniff
        :arg serializer: serializer instance
        :arg max_retries: maximum number of retries before an exception is propagated

        Any extra keyword arguments will be passed to the `connection_class`
        when creating and instance unless overriden by that connection's
        options provided as part of the hosts parameter.
        """

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
        # TODO: minimal sniff interval
        self.sniffs_due_to_failure = 0
        self.sniff_after_requests_original = sniff_after_requests
        self.sniff_after_requests = sniff_after_requests
        self.sniff_on_connection_fail = sniff_on_connection_fail

        # callback to construct hosts dicts from /_cluster/nodes data
        self.nodes_to_host_callback = nodes_to_host_callback

        if sniff_on_start:
            self.sniff_hosts()

    def add_connection(self, host):
        """
        Create a new :class:`~elasticsearch.Connection` instance and add it to the pool.

        :arg host: kwargs that will be used to create the instance
        """
        self.hosts.append(host)
        self.set_connections(self.hosts)

    def set_connections(self, hosts):
        """
        Instantiate all the connections and crate new connection pool to hold them.

        :arg hosts: same as `__init__`
        """
        # construct the connections
        def _create_connection(host):
            kwargs = self.kwargs.copy()
            kwargs.update(host)
            return self.connection_class(**kwargs)
        connections = list(map(_create_connection, hosts))

        # pass the hosts dicts to the connection pool to optionally extract parameters from
        self.connection_pool = self.connection_pool_class(zip(connections, hosts), **self.kwargs)

    def get_connection(self, sniffing=False):
        """
        Retreive a :class:`~elasticsearch.Connection` instance from the
        :class:`~elasticsearch.ConnectionPool` instance.

        :arg sniffing: flag indicating that the connection will be used for
            sniffing for nodes
        """
        if not sniffing and self.sniff_after_requests:
            if self.req_counter >= self.sniff_after_requests:
                self.sniff_hosts()
            self.req_counter += 1
        return self.connection_pool.get_connection()

    def sniff_hosts(self, failure=False):
        """
        Obtain a list of nodes from the cluster and create a new connection
        pool using the information retrieved.

        To extract the node connection parameters use the `nodes_to_host_callback`.

        :arg failure: indicates whether this sniffing was initiated because of
            a connection failure
        """
        # set the counter to 0 first so that other threads won't sniff as well
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

    def mark_dead(self, connection, dead_count, sniffing=False):
        """
        Mark a connection as dead (failed) in the connection pool. If sniffing
        on failure is enabled this will initiate the sniffing process (unless
        the failure occured during that process itself).

        :arg connection: instance of :class:`~elasticsearch.Connection` that failed
        :arg dead_count: number of successive failures for this connection
        :arg sniffing: flag indicating that the failure occured during sniffing
            for nodes
        """
        if not sniffing and self.sniff_on_connection_fail:
            self.sniff_hosts(True)
        else:
            self.connection_pool.mark_dead(connection, dead_count)

    def perform_request(self, method, url, params=None, body=None, sniffing=False):
        """
        Perform the actual request. Retrieve a connection from the connection
        pool, pass all the information to it's perform_request method and
        return the data.

        If an exception was raised, mark the connection as failed and retry (up
        to `max_retries` times).

        If the operation was succesful and the connection used was previously
        marked as dead, mark it as live, resetting it's failure count.

        :arg method: HTTP method to use
        :arg url: absolute url (without host) to target
        :arg params: dictionary of query parameters, will be handed over to the
            underlying :class:`~elasticsearch.Connection` class for serialization
        :arg body: body of the request, will be serializes using serializer and
            passed to the connection
        :arg sniffing: flag indicating whether the request is done as part of
            the sniffing process
        """
        if body:
            body = self.serializer.dumps(body)

        for attempt in range(self.max_retries):
            connection, dead_count = self.get_connection(sniffing)

            try:
                status, raw_data = connection.perform_request(method, url, params, body)
            except TransportError:
                # TODO: don't retry on client errors etc
                self.mark_dead(connection, dead_count + 1, sniffing)

                # raise exception on last retry
                if attempt + 1 == self.max_retries:
                    raise
            else:
                # resurrected connection didn't fail, confirm it's live status
                if dead_count:
                    self.connection_pool.mark_live(connection)
                return status, self.serializer.loads(raw_data)


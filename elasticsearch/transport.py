import re
import time

from .connection import RequestsHttpConnection
from .connection_pool import ConnectionPool
from .serializer import JSONSerializer
from .exceptions import ConnectionError

# get ip/port from "inet[wind/127.0.0.1:9200]"
ADDRESS_RE = re.compile(r'/(?P<host>[\.:0-9a-f]*):(?P<port>[0-9]+)\]')


def get_host_info(node_info, host):
    """
    Simple callback that takes the node info from `/_cluster/nodes` and a
    parsed connection information and return the connection information. If
    `None` is returned this node will be skipped.

    Useful for filtering nodes (by proximity for example) or if additional
    information needs to be provided for the :class:`~elasticsearch.Connection`
    class.

    :arg node_info: node information from `/_cluster/nodes`
    :arg host: connection information (host, port) extracted from the node info
    """
    return host

class Transport(object):
    """
    Encapsulation of transport-related to logic. Handles instantiation of the
    individual connections as well as creating a connection pool to hold them.

    Main interface is the `perform_request` method.
    """
    def __init__(self, hosts, connection_class=RequestsHttpConnection,
        connection_pool_class=ConnectionPool, host_info_callback=get_host_info,
        sniff_on_start=False, sniffer_timeout=None,
        sniff_on_connection_fail=False, serializer=JSONSerializer(),
        max_retries=3, **kwargs):
        """
        :arg hosts: list of dictionaries, each containing keyword arguments to
            create a `connection_class` instance
        :arg connection_class: subclass of :class:`~elasticsearch.Connection` to use
        :arg connection_pool_class: subclass of :class:`~elasticsearch.ConnectionPool` to use
        :arg host_info_callback: callback responsible for taking the node information from
            `/_cluser/nodes`, along with already extracted information, and
            producing a list of arguments (same as `hosts` parameter)
        :arg sniff_on_start: flag indicating whether to obtain a list of nodes
            from the cluser at startup time
        :arg sniffer_timeout: number of seconds between automatic sniffs
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
        self.sniffer_timeout = sniffer_timeout
        self.sniff_on_connection_fail = sniff_on_connection_fail
        self.last_sniff = time.time()

        # callback to construct host dict from data in /_cluster/nodes
        self.host_info_callback = host_info_callback

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
        if not sniffing and self.sniffer_timeout:
            if time.time() >= self.last_sniff + self.sniffer_timeout:
                self.sniff_hosts()
        return self.connection_pool.get_connection()

    def sniff_hosts(self, failure=False):
        """
        Obtain a list of nodes from the cluster and create a new connection
        pool using the information retrieved.

        To extract the node connection parameters use the `nodes_to_host_callback`.

        :arg failure: indicates whether this sniffing was initiated because of
            a connection failure
        """
        previous_sniff = self.last_sniff
        try:
            # reset last_sniff timestamp
            self.last_sniff = time.time()
            _, node_info = self.perform_request('GET', '/_cluster/nodes', sniffing=True)
        except:
            # keep the previous value on error
            self.last_sniff = previous_sniff
            raise

        hosts = []
        address = self.connection_class.transport_schema + '_address'
        for n in node_info['nodes'].values():
            match = ADDRESS_RE.search(n.get(address, ''))
            if not match:
                continue

            host = match.groupdict()
            if 'port' in host:
                host['port'] = int(host['port'])
            host = self.host_info_callback(n, host)
            if host is not None:
                hosts.append(host)

        self.set_connections(hosts)

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
            except ConnectionError:
                self.mark_dead(connection, dead_count + 1, sniffing)

                # raise exception on last retry
                if attempt + 1 == self.max_retries:
                    raise
            else:
                # resurrected connection didn't fail, confirm it's live status
                if dead_count:
                    self.connection_pool.mark_live(connection)
                return status, self.serializer.loads(raw_data)


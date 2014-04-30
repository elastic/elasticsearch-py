import re
import time

from .connection import Urllib3HttpConnection
from .connection_pool import ConnectionPool
from .serializer import JSONSerializer, Deserializer, DEFAULT_SERIALIZERS
from .exceptions import ConnectionError, TransportError, SerializationError

# get ip/port from "inet[wind/127.0.0.1:9200]"
ADDRESS_RE = re.compile(r'/(?P<host>[\.:0-9a-f]*):(?P<port>[0-9]+)\]?$')


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
    def __init__(self, hosts, connection_class=Urllib3HttpConnection,
        connection_pool_class=ConnectionPool, host_info_callback=get_host_info,
        sniff_on_start=False, sniffer_timeout=None, sniff_timeout=.1,
        sniff_on_connection_fail=False, serializer=JSONSerializer(), serializers=None,
        default_mimetype='application/json', max_retries=3,
        send_get_body_as='GET', **kwargs):
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
        :arg sniff_on_connection_fail: flag controlling if connection failure triggers a sniff
        :arg sniff_timeout: timeout used for the sniff request - it should be a
            fast api call and we are talking potentially to more nodes so we want
            to fail quickly.
        :arg serializer: serializer instance
        :arg serializers: optional dict of serializer instances that will be
            used for deserializing data coming from the server. (key is the mimetype)
        :arg default_mimetype: when no mimetype is specified by the server
            response assume this mimetype, defaults to `'application/json'`
        :arg max_retries: maximum number of retries before an exception is propagated
        :arg send_get_body_as: for GET requests with body this option allows
            you to specify an alternate way of execution for environments that
            don't support passing bodies with GET requests. If you set this to
            'POST' a POST method will be used instead, if to 'source' then the body
            will be serialized and passed as a query parameter `source`.

        Any extra keyword arguments will be passed to the `connection_class`
        when creating and instance unless overriden by that connection's
        options provided as part of the hosts parameter.
        """

        # serialization config
        _serializers = DEFAULT_SERIALIZERS.copy()
        # if a serializer has been specified, use it for deserialization as well
        _serializers[serializer.mimetype] = serializer
        # if custom serializers map has been supplied, override the defaults with it
        if serializers:
            _serializers.update(serializers)
        # create a deserializer with our config
        self.deserializer = Deserializer(_serializers, default_mimetype)

        self.max_retries = max_retries
        self.send_get_body_as = send_get_body_as

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
        # retain the original connection instances for sniffing
        self.seed_connections = self.connection_pool.connections[:]

        # sniffing data
        self.sniffer_timeout = sniffer_timeout
        self.sniff_on_connection_fail = sniff_on_connection_fail
        self.last_sniff = time.time()
        self.sniff_timeout = sniff_timeout

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
        Instantiate all the connections and crate new connection pool to hold
        them. Tries to identify unchanged hosts and re-use existing
        :class:`~elasticsearch.Connection` instances.

        :arg hosts: same as `__init__`
        """
        # construct the connections
        def _create_connection(host):
            # if this is not the initial setup look at the existing connection
            # options and identify connections that haven't changed and can be
            # kept around.
            if hasattr(self, 'connection_pool'):
                for (connection, old_host) in self.connection_pool.connection_opts:
                    if old_host == host:
                        return connection

            # previously unseen params, create new connection
            kwargs = self.kwargs.copy()
            kwargs.update(host)
            return self.connection_class(**kwargs)
        connections = map(_create_connection, hosts)

        # pass the hosts dicts to the connection pool to optionally extract parameters from
        self.connection_pool = self.connection_pool_class(list(zip(connections, hosts)), **self.kwargs)

    def get_connection(self):
        """
        Retreive a :class:`~elasticsearch.Connection` instance from the
        :class:`~elasticsearch.ConnectionPool` instance.
        """
        if self.sniffer_timeout:
            if time.time() >= self.last_sniff + self.sniffer_timeout:
                self.sniff_hosts()
        return self.connection_pool.get_connection()

    def sniff_hosts(self):
        """
        Obtain a list of nodes from the cluster and create a new connection
        pool using the information retrieved.

        To extract the node connection parameters use the `nodes_to_host_callback`.
        """
        previous_sniff = self.last_sniff
        try:
            # reset last_sniff timestamp
            self.last_sniff = time.time()
            # go through all current connections as well as the
            # seed_connections for good measure
            for c in self.connection_pool.connections + self.seed_connections:
                try:
                    # use small timeout for the sniffing request, should be a fast api call
                    _, headers, node_info = c.perform_request('GET', '/_nodes/_all/clear',
                        timeout=self.sniff_timeout)
                    node_info = self.deserializer.loads(node_info, headers.get('content-type'))
                    break
                except (ConnectionError, SerializationError):
                    pass
            else:
                raise TransportError("N/A", "Unable to sniff hosts.")
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

        # we weren't able to get any nodes, maybe using an incompatible
        # transport_schema or host_info_callback blocked all - raise error.
        if not hosts:
            raise TransportError("N/A", "Unable to sniff hosts - no viable hosts found.")

        self.set_connections(hosts)

    def mark_dead(self, connection):
        """
        Mark a connection as dead (failed) in the connection pool. If sniffing
        on failure is enabled this will initiate the sniffing process.

        :arg connection: instance of :class:`~elasticsearch.Connection` that failed
        """
        # mark as dead even when sniffing to avoid hitting this host during the sniff process
        self.connection_pool.mark_dead(connection)
        if self.sniff_on_connection_fail:
            self.sniff_hosts()

    def perform_request(self, method, url, params=None, body=None):
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
        """
        if body is not None:
            body = self.serializer.dumps(body)

            # some clients or environments don't support sending GET with body
            if method == 'GET' and self.send_get_body_as != 'GET':
                # send it as post instead
                if self.send_get_body_as == 'POST':
                    method = 'POST'

                # or as source parameter
                elif self.send_get_body_as == 'source':
                    if params is None:
                        params = {}
                    params['source'] = body
                    body = None

        if body is not None:
            try:
                body = body.encode('utf-8')
            except UnicodeDecodeError:
                # Python 2 and str, no need to re-encode
                pass

        ignore = ()
        if params and 'ignore' in params:
            ignore = params.pop('ignore')
            if isinstance(ignore, int):
                ignore = (ignore, )

        for attempt in range(self.max_retries + 1):
            connection = self.get_connection()

            try:
                status, headers, data = connection.perform_request(method, url, params, body, ignore=ignore)
            except ConnectionError:
                self.mark_dead(connection)

                # raise exception on last retry
                if attempt == self.max_retries:
                    raise
            else:
                # connection didn't fail, confirm it's live status
                self.connection_pool.mark_live(connection)
                if data:
                    data = self.deserializer.loads(data, headers.get('content-type'))
                return status, data


import logging

from .http_aiohttp import AIOHttpConnection
from ..transport import Transport
from ..connection_pool import DummyConnectionPool
from ..exceptions import TransportError, ConnectionTimeout


logger = logging.getLogger("elasticsearch")


class AsyncTransport(Transport):
    DEFAULT_CONNECTION_CLASS = AIOHttpConnection

    def add_connection(self, host):
        """
        Create a new :class:`~elasticsearch.Connection` instance and add it to the pool.

        :arg host: kwargs that will be used to create the instance
        """
        self.hosts.append(host)
        self.set_connections(self.hosts)

    def set_connections(self, hosts):
        """
        Instantiate all the connections and create new connection pool to hold them.
        Tries to identify unchanged hosts and re-use existing
        :class:`~elasticsearch.Connection` instances.

        :arg hosts: same as `__init__`
        """
        # construct the connections
        def _create_connection(host):
            # if this is not the initial setup look at the existing connection
            # options and identify connections that haven't changed and can be
            # kept around.
            if hasattr(self, "connection_pool"):
                for (connection, old_host) in self.connection_pool.connection_opts:
                    if old_host == host:
                        return connection

            # previously unseen params, create new connection
            kwargs = self.kwargs.copy()
            kwargs.update(host)
            return self.connection_class(**kwargs)

        connections = map(_create_connection, hosts)

        connections = list(zip(connections, hosts))
        if len(connections) == 1:
            self.connection_pool = DummyConnectionPool(connections)
        else:
            # pass the hosts dicts to the connection pool to optionally extract parameters from
            self.connection_pool = self.connection_pool_class(
                connections, **self.kwargs
            )

    def get_connection(self):
        """
        Retrieve a :class:`~elasticsearch.Connection` instance from the
        :class:`~elasticsearch.ConnectionPool` instance.
        """
        return self.connection_pool.get_connection()

    def mark_dead(self, connection):
        """
        Mark a connection as dead (failed) in the connection pool. If sniffing
        on failure is enabled this will initiate the sniffing process.

        :arg connection: instance of :class:`~elasticsearch.Connection` that failed
        """
        self.connection_pool.mark_dead(connection)

    async def close(self):
        if getattr(self, "sniffing_task", None):
            self.sniffing_task.cancel()
        await self.connection_pool.close()

    async def perform_request(self, method, url, headers=None, params=None, body=None):
        if body is not None:
            body = self.serializer.dumps(body)

            # some clients or environments don't support sending GET with body
            if method in ("HEAD", "GET") and self.send_get_body_as != "GET":
                # send it as post instead
                if self.send_get_body_as == "POST":
                    method = "POST"

                # or as source parameter
                elif self.send_get_body_as == "source":
                    if params is None:
                        params = {}
                    params["source"] = body
                    body = None

        if body is not None:
            try:
                body = body.encode("utf-8")
            except (UnicodeDecodeError, AttributeError):
                # bytes/str - no need to re-encode
                pass

        ignore = ()
        timeout = None
        if params:
            timeout = params.pop("request_timeout", None)
            ignore = params.pop("ignore", ())
            if isinstance(ignore, int):
                ignore = (ignore,)

        for attempt in range(self.max_retries + 1):
            connection = self.get_connection()

            try:
                status, headers, data = await connection.perform_request(
                    method,
                    url,
                    params,
                    body,
                    headers=headers,
                    ignore=ignore,
                    timeout=timeout,
                )
            except TransportError as e:
                if method == "HEAD" and e.status_code == 404:
                    return False

                retry = False
                if isinstance(e, ConnectionTimeout):
                    retry = self.retry_on_timeout
                elif isinstance(e, ConnectionError):
                    retry = True
                elif e.status_code in self.retry_on_status:
                    retry = True

                if retry:
                    # only mark as dead if we are retrying
                    self.mark_dead(connection)
                    # raise exception on last retry
                    if attempt == self.max_retries:
                        raise
                else:
                    raise

            else:
                if method == "HEAD":
                    return 200 <= status < 300

                # connection didn't fail, confirm it's live status
                self.connection_pool.mark_live(connection)
                if data:
                    data = self.deserializer.loads(data, headers.get("content-type"))
                return data

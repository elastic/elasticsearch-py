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

import asyncio
import logging
from itertools import chain
import sys

from .compat import get_running_loop
from .http_aiohttp import AIOHttpConnection
from ..transport import Transport
from ..exceptions import (
    TransportError,
    ConnectionTimeout,
    ConnectionError,
    SerializationError,
)


logger = logging.getLogger("elasticsearch")


class AsyncTransport(Transport):
    """
    Encapsulation of transport-related to logic. Handles instantiation of the
    individual connections as well as creating a connection pool to hold them.

    Main interface is the `perform_request` method.
    """

    DEFAULT_CONNECTION_CLASS = AIOHttpConnection

    def __init__(self, hosts, *args, sniff_on_start=False, **kwargs):
        """
        :arg hosts: list of dictionaries, each containing keyword arguments to
            create a `connection_class` instance
        :arg connection_class: subclass of :class:`~elasticsearch.Connection` to use
        :arg connection_pool_class: subclass of :class:`~elasticsearch.ConnectionPool` to use
        :arg host_info_callback: callback responsible for taking the node information from
            `/_cluster/nodes`, along with already extracted information, and
            producing a list of arguments (same as `hosts` parameter)
        :arg sniff_on_start: flag indicating whether to obtain a list of nodes
            from the cluster at startup time
        :arg sniffer_timeout: number of seconds between automatic sniffs
        :arg sniff_on_connection_fail: flag controlling if connection failure triggers a sniff
        :arg sniff_timeout: timeout used for the sniff request - it should be a
            fast api call and we are talking potentially to more nodes so we want
            to fail quickly. Not used during initial sniffing (if
            ``sniff_on_start`` is on) when the connection still isn't
            initialized.
        :arg serializer: serializer instance
        :arg serializers: optional dict of serializer instances that will be
            used for deserializing data coming from the server. (key is the mimetype)
        :arg default_mimetype: when no mimetype is specified by the server
            response assume this mimetype, defaults to `'application/json'`
        :arg max_retries: maximum number of retries before an exception is propagated
        :arg retry_on_status: set of HTTP status codes on which we should retry
            on a different node. defaults to ``(502, 503, 504)``
        :arg retry_on_timeout: should timeout trigger a retry on different
            node? (default `False`)
        :arg send_get_body_as: for GET requests with body this option allows
            you to specify an alternate way of execution for environments that
            don't support passing bodies with GET requests. If you set this to
            'POST' a POST method will be used instead, if to 'source' then the body
            will be serialized and passed as a query parameter `source`.

        Any extra keyword arguments will be passed to the `connection_class`
        when creating and instance unless overridden by that connection's
        options provided as part of the hosts parameter.
        """
        self.sniffing_task = None
        self.loop = None
        self._async_init_called = False

        super(AsyncTransport, self).__init__(
            *args, hosts=[], sniff_on_start=False, **kwargs
        )

        # Don't enable sniffing on Cloud instances.
        if kwargs.get("cloud_id", False):
            sniff_on_start = False

        # Since we defer connections / sniffing to not occur
        # within the constructor we never want to signal to
        # our parent to 'sniff_on_start' or non-empty 'hosts'.
        self.hosts = hosts
        self.sniff_on_start = sniff_on_start

    async def _async_init(self):
        """This is our stand-in for an async constructor. Everything
        that was deferred within __init__() should be done here now.

        This method will only be called once per AsyncTransport instance
        and is called from one of AsyncElasticsearch.__aenter__(),
        AsyncTransport.perform_request() or AsyncTransport.get_connection()
        """
        # Detect the async loop we're running in and set it
        # on all already created HTTP connections.
        self.loop = get_running_loop()
        self.kwargs["loop"] = self.loop

        # Now that we have a loop we can create all our HTTP connections
        self.set_connections(self.hosts)
        self.seed_connections = list(self.connection_pool.connections[:])

        # ... and we can start sniffing in the background.
        if self.sniffing_task is None and self.sniff_on_start:
            self.last_sniff = self.loop.time()
            self.create_sniff_task(initial=True)

    async def _async_call(self):
        """This method is called within any async method of AsyncTransport
        where the transport is not closing. This will check to see if we should
        call our _async_init() or create a new sniffing task
        """
        if not self._async_init_called:
            self._async_init_called = True
            await self._async_init()

        if self.sniffer_timeout:
            if self.loop.time() >= self.last_sniff + self.sniff_timeout:
                self.create_sniff_task()

    async def _get_node_info(self, conn, initial):
        try:
            # use small timeout for the sniffing request, should be a fast api call
            _, headers, node_info = await conn.perform_request(
                "GET",
                "/_nodes/_all/http",
                timeout=self.sniff_timeout if not initial else None,
            )
            return self.deserializer.loads(node_info, headers.get("content-type"))
        except Exception:
            pass
        return None

    async def _get_sniff_data(self, initial=False):
        previous_sniff = self.last_sniff

        # reset last_sniff timestamp
        self.last_sniff = self.loop.time()

        # use small timeout for the sniffing request, should be a fast api call
        timeout = self.sniff_timeout if not initial else None

        def _sniff_request(conn):
            return self.loop.create_task(
                conn.perform_request("GET", "/_nodes/_all/http", timeout=timeout)
            )

        # Go through all current connections as well as the
        # seed_connections for good measure
        tasks = []
        for conn in self.connection_pool.connections:
            tasks.append(_sniff_request(conn))
        for conn in self.seed_connections:
            # Ensure that we don't have any duplication within seed_connections.
            if conn in self.connection_pool.connections:
                continue
            tasks.append(_sniff_request(conn))

        done = ()
        try:
            while tasks:
                # The 'loop' keyword is deprecated in 3.8+ so don't
                # pass it to asyncio.wait() unless we're on <=3.7
                wait_kwargs = {"loop": self.loop} if sys.version_info < (3, 8) else {}

                # execute sniff requests in parallel, wait for first to return
                done, tasks = await asyncio.wait(
                    tasks, return_when=asyncio.FIRST_COMPLETED, **wait_kwargs
                )
                # go through all the finished tasks
                for t in done:
                    try:
                        _, headers, node_info = t.result()
                        node_info = self.deserializer.loads(
                            node_info, headers.get("content-type")
                        )
                    except (ConnectionError, SerializationError):
                        continue
                    node_info = list(node_info["nodes"].values())
                    return node_info
            else:
                # no task has finished completely
                raise TransportError("N/A", "Unable to sniff hosts.")
        except Exception:
            # keep the previous value on error
            self.last_sniff = previous_sniff
            raise
        finally:
            # Cancel all the pending tasks
            for task in chain(done, tasks):
                task.cancel()

    async def sniff_hosts(self, initial=False):
        """Either spawns a sniffing_task which does regular sniffing
        over time or does a single sniffing session and awaits the results.
        """
        # Without a loop we can't do anything.
        if not self.loop:
            return

        node_info = await self._get_sniff_data(initial)
        hosts = list(filter(None, (self._get_host_info(n) for n in node_info)))

        # we weren't able to get any nodes, maybe using an incompatible
        # transport_schema or host_info_callback blocked all - raise error.
        if not hosts:
            raise TransportError(
                "N/A", "Unable to sniff hosts - no viable hosts found."
            )

        # remember current live connections
        orig_connections = self.connection_pool.connections[:]
        self.set_connections(hosts)
        # close those connections that are not in use any more
        for c in orig_connections:
            if c not in self.connection_pool.connections:
                await c.close()

    def create_sniff_task(self, initial=False):
        """
        Initiate a sniffing task. Make sure we only have one sniff request
        running at any given time. If a finished sniffing request is around,
        collect its result (which can raise its exception).
        """
        if self.sniffing_task and self.sniffing_task.done():
            try:
                if self.sniffing_task is not None:
                    self.sniffing_task.result()
            finally:
                self.sniffing_task = None

        if self.sniffing_task is None:
            self.sniffing_task = self.loop.create_task(self.sniff_hosts(initial))

    def mark_dead(self, connection):
        """
        Mark a connection as dead (failed) in the connection pool. If sniffing
        on failure is enabled this will initiate the sniffing process.

        :arg connection: instance of :class:`~elasticsearch.Connection` that failed
        """
        self.connection_pool.mark_dead(connection)
        if self.sniff_on_connection_fail:
            self.create_sniff_task()

    def get_connection(self):
        return self.connection_pool.get_connection()

    async def perform_request(self, method, url, headers=None, params=None, body=None):
        """
        Perform the actual request. Retrieve a connection from the connection
        pool, pass all the information to it's perform_request method and
        return the data.

        If an exception was raised, mark the connection as failed and retry (up
        to `max_retries` times).

        If the operation was successful and the connection used was previously
        marked as dead, mark it as live, resetting it's failure count.

        :arg method: HTTP method to use
        :arg url: absolute url (without host) to target
        :arg headers: dictionary of headers, will be handed over to the
            underlying :class:`~elasticsearch.Connection` class
        :arg params: dictionary of query parameters, will be handed over to the
            underlying :class:`~elasticsearch.Connection` class for serialization
        :arg body: body of the request, will be serialized using serializer and
            passed to the connection
        """
        await self._async_call()

        method, params, body, ignore, timeout = self._resolve_request_args(
            method, params, body
        )

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
                    try:
                        # only mark as dead if we are retrying
                        self.mark_dead(connection)
                    except TransportError:
                        # If sniffing on failure, it could fail too. Catch the
                        # exception not to interrupt the retries.
                        pass
                    # raise exception on last retry
                    if attempt == self.max_retries:
                        raise e
                else:
                    raise e

            else:
                # connection didn't fail, confirm it's live status
                self.connection_pool.mark_live(connection)

                if method == "HEAD":
                    return 200 <= status < 300

                if data:
                    data = self.deserializer.loads(data, headers.get("content-type"))
                return data

    async def close(self):
        """
        Explicitly closes connections
        """
        if self.sniffing_task:
            try:
                self.sniffing_task.cancel()
                await self.sniffing_task
            except asyncio.CancelledError:
                pass
            self.sniffing_task = None
        for connection in self.connection_pool.connections:
            await connection.close()

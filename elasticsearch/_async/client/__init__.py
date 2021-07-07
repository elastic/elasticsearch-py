# -*- coding: utf-8 -*-
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

from __future__ import unicode_literals

import logging

from ..transport import AsyncTransport, TransportError
from .async_search import AsyncSearchClient
from .autoscaling import AutoscalingClient
from .cat import CatClient
from .ccr import CcrClient
from .cluster import ClusterClient
from .dangling_indices import DanglingIndicesClient
from .data_frame import Data_FrameClient
from .deprecation import DeprecationClient
from .enrich import EnrichClient
from .eql import EqlClient
from .features import FeaturesClient
from .fleet import FleetClient
from .graph import GraphClient
from .ilm import IlmClient
from .indices import IndicesClient
from .ingest import IngestClient
from .license import LicenseClient
from .logstash import LogstashClient
from .migration import MigrationClient
from .ml import MlClient
from .monitoring import MonitoringClient
from .nodes import NodesClient
from .remote import RemoteClient
from .rollup import RollupClient
from .searchable_snapshots import SearchableSnapshotsClient
from .security import SecurityClient
from .shutdown import ShutdownClient
from .slm import SlmClient
from .snapshot import SnapshotClient
from .sql import SqlClient
from .ssl import SslClient
from .tasks import TasksClient
from .text_structure import TextStructureClient
from .transform import TransformClient
from .utils import SKIP_IN_PATH, _bulk_body, _make_path, _normalize_hosts, query_params
from .watcher import WatcherClient

# xpack APIs
from .xpack import XPackClient

logger = logging.getLogger("elasticsearch")


class AsyncElasticsearch(object):
    """
    Elasticsearch low-level client. Provides a straightforward mapping from
    Python to ES REST endpoints.

    The instance has attributes ``cat``, ``cluster``, ``indices``, ``ingest``,
    ``nodes``, ``snapshot`` and ``tasks`` that provide access to instances of
    :class:`~elasticsearch.client.CatClient`,
    :class:`~elasticsearch.client.ClusterClient`,
    :class:`~elasticsearch.client.IndicesClient`,
    :class:`~elasticsearch.client.IngestClient`,
    :class:`~elasticsearch.client.NodesClient`,
    :class:`~elasticsearch.client.SnapshotClient` and
    :class:`~elasticsearch.client.TasksClient` respectively. This is the
    preferred (and only supported) way to get access to those classes and their
    methods.

    You can specify your own connection class which should be used by providing
    the ``connection_class`` parameter::

        # create connection to localhost using the ThriftConnection
        es = Elasticsearch(connection_class=ThriftConnection)

    If you want to turn on :ref:`sniffing` you have several options (described
    in :class:`~elasticsearch.Transport`)::

        # create connection that will automatically inspect the cluster to get
        # the list of active nodes. Start with nodes running on 'esnode1' and
        # 'esnode2'
        es = Elasticsearch(
            ['esnode1', 'esnode2'],
            # sniff before doing anything
            sniff_on_start=True,
            # refresh nodes after a node fails to respond
            sniff_on_connection_fail=True,
            # and also every 60 seconds
            sniffer_timeout=60
        )

    Different hosts can have different parameters, use a dictionary per node to
    specify those::

        # connect to localhost directly and another node using SSL on port 443
        # and an url_prefix. Note that ``port`` needs to be an int.
        es = Elasticsearch([
            {'host': 'localhost'},
            {'host': 'othernode', 'port': 443, 'url_prefix': 'es', 'use_ssl': True},
        ])

    If using SSL, there are several parameters that control how we deal with
    certificates (see :class:`~elasticsearch.Urllib3HttpConnection` for
    detailed description of the options)::

        es = Elasticsearch(
            ['localhost:443', 'other_host:443'],
            # turn on SSL
            use_ssl=True,
            # make sure we verify SSL certificates
            verify_certs=True,
            # provide a path to CA certs on disk
            ca_certs='/path/to/CA_certs'
        )

    If using SSL, but don't verify the certs, a warning message is showed
    optionally (see :class:`~elasticsearch.Urllib3HttpConnection` for
    detailed description of the options)::

        es = Elasticsearch(
            ['localhost:443', 'other_host:443'],
            # turn on SSL
            use_ssl=True,
            # no verify SSL certificates
            verify_certs=False,
            # don't show warnings about ssl certs verification
            ssl_show_warn=False
        )

    SSL client authentication is supported
    (see :class:`~elasticsearch.Urllib3HttpConnection` for
    detailed description of the options)::

        es = Elasticsearch(
            ['localhost:443', 'other_host:443'],
            # turn on SSL
            use_ssl=True,
            # make sure we verify SSL certificates
            verify_certs=True,
            # provide a path to CA certs on disk
            ca_certs='/path/to/CA_certs',
            # PEM formatted SSL client certificate
            client_cert='/path/to/clientcert.pem',
            # PEM formatted SSL client key
            client_key='/path/to/clientkey.pem'
        )

    Alternatively you can use RFC-1738 formatted URLs, as long as they are not
    in conflict with other options::

        es = Elasticsearch(
            [
                'http://user:secret@localhost:9200/',
                'https://user:secret@other_host:443/production'
            ],
            verify_certs=True
        )

    By default, `JSONSerializer
    <https://github.com/elastic/elasticsearch-py/blob/master/elasticsearch/serializer.py#L24>`_
    is used to encode all outgoing requests.
    However, you can implement your own custom serializer::

        from elasticsearch.serializer import JSONSerializer

        class SetEncoder(JSONSerializer):
            def default(self, obj):
                if isinstance(obj, set):
                    return list(obj)
                if isinstance(obj, Something):
                    return 'CustomSomethingRepresentation'
                return JSONSerializer.default(self, obj)

        es = Elasticsearch(serializer=SetEncoder())

    """

    def __init__(self, hosts=None, transport_class=AsyncTransport, **kwargs):
        """
        :arg hosts: list of nodes, or a single node, we should connect to.
            Node should be a dictionary ({"host": "localhost", "port": 9200}),
            the entire dictionary will be passed to the :class:`~elasticsearch.Connection`
            class as kwargs, or a string in the format of ``host[:port]`` which will be
            translated to a dictionary automatically.  If no value is given the
            :class:`~elasticsearch.Connection` class defaults will be used.

        :arg transport_class: :class:`~elasticsearch.Transport` subclass to use.

        :arg kwargs: any additional arguments will be passed on to the
            :class:`~elasticsearch.Transport` class and, subsequently, to the
            :class:`~elasticsearch.Connection` instances.
        """
        self.transport = transport_class(_normalize_hosts(hosts), **kwargs)

        # namespaced clients for compatibility with API names
        self.async_search = AsyncSearchClient(self)
        self.autoscaling = AutoscalingClient(self)
        self.cat = CatClient(self)
        self.cluster = ClusterClient(self)
        self.dangling_indices = DanglingIndicesClient(self)
        self.indices = IndicesClient(self)
        self.ingest = IngestClient(self)
        self.nodes = NodesClient(self)
        self.remote = RemoteClient(self)
        self.snapshot = SnapshotClient(self)
        self.tasks = TasksClient(self)

        self.xpack = XPackClient(self)
        self.ccr = CcrClient(self)
        self.data_frame = Data_FrameClient(self)
        self.deprecation = DeprecationClient(self)
        self.enrich = EnrichClient(self)
        self.eql = EqlClient(self)
        self.features = FeaturesClient(self)
        self.fleet = FleetClient(self)
        self.graph = GraphClient(self)
        self.ilm = IlmClient(self)
        self.license = LicenseClient(self)
        self.logstash = LogstashClient(self)
        self.migration = MigrationClient(self)
        self.ml = MlClient(self)
        self.monitoring = MonitoringClient(self)
        self.rollup = RollupClient(self)
        self.searchable_snapshots = SearchableSnapshotsClient(self)
        self.security = SecurityClient(self)
        self.slm = SlmClient(self)
        self.shutdown = ShutdownClient(self)
        self.sql = SqlClient(self)
        self.ssl = SslClient(self)
        self.text_structure = TextStructureClient(self)
        self.transform = TransformClient(self)
        self.watcher = WatcherClient(self)

    def __repr__(self):
        try:
            # get a list of all connections
            cons = self.transport.hosts
            # truncate to 5 if there are too many
            if len(cons) > 5:
                cons = cons[:5] + ["..."]
            return "<{cls}({cons})>".format(cls=self.__class__.__name__, cons=cons)
        except Exception:
            # probably operating on custom transport and connection_pool, ignore
            return super(AsyncElasticsearch, self).__repr__()

    async def __aenter__(self):
        if hasattr(self.transport, "_async_call"):
            await self.transport._async_call()
        return self

    async def __aexit__(self, *_):
        await self.close()

    async def close(self):
        """Closes the Transport and all internal connections"""
        await self.transport.close()

    # AUTO-GENERATED-API-DEFINITIONS #
    @query_params()
    async def ping(self, params=None, headers=None):
        """
        Returns whether the cluster is running.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/index.html>`_
        """
        try:
            return await self.transport.perform_request(
                "HEAD", "/", params=params, headers=headers
            )
        except TransportError:
            return False

    @query_params()
    async def info(self, params=None, headers=None):
        """
        Returns basic information about the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/index.html>`_
        """
        return await self.transport.perform_request(
            "GET", "/", params=params, headers=headers
        )

    @query_params(
        "pipeline",
        "refresh",
        "routing",
        "timeout",
        "version",
        "version_type",
        "wait_for_active_shards",
    )
    async def create(self, index, id, body, doc_type=None, params=None, headers=None):
        """
        Creates a new document in the index.  Returns a 409 response when a document
        with a same ID already exists in the index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-index_.html>`_

        :arg index: The name of the index
        :arg id: Document ID
        :arg body: The document
        :arg doc_type: The type of the document
        :arg pipeline: The pipeline id to preprocess incoming documents
            with
        :arg refresh: If `true` then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh
            to make this operation visible to search, if `false` (the default) then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the index operation. Defaults
            to 1, meaning the primary shard only. Set to `all` for all shard copies,
            otherwise set to any non-negative value less than or equal to the total
            number of copies for the shard (number of replicas + 1)
        """
        for param in (index, id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_create", id)
        else:
            path = _make_path(index, doc_type, id, "_create")

        return await self.transport.perform_request(
            "PUT", path, params=params, headers=headers, body=body
        )

    @query_params(
        "if_primary_term",
        "if_seq_no",
        "op_type",
        "pipeline",
        "refresh",
        "require_alias",
        "routing",
        "timeout",
        "version",
        "version_type",
        "wait_for_active_shards",
    )
    async def index(
        self, index, body, doc_type=None, id=None, params=None, headers=None
    ):
        """
        Creates or updates a document in an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-index_.html>`_

        :arg index: The name of the index
        :arg body: The document
        :arg doc_type: The type of the document
        :arg id: Document ID
        :arg if_primary_term: only perform the index operation if the
            last operation that has changed the document has the specified primary
            term
        :arg if_seq_no: only perform the index operation if the last
            operation that has changed the document has the specified sequence
            number
        :arg op_type: Explicit operation type. Defaults to `index` for
            requests with an explicit document ID, and to `create`for requests
            without an explicit document ID  Valid choices: index, create
        :arg pipeline: The pipeline id to preprocess incoming documents
            with
        :arg refresh: If `true` then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh
            to make this operation visible to search, if `false` (the default) then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        :arg require_alias: When true, requires destination to be an
            alias. Default is false
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the index operation. Defaults
            to 1, meaning the primary shard only. Set to `all` for all shard copies,
            otherwise set to any non-negative value less than or equal to the total
            number of copies for the shard (number of replicas + 1)
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type is None:
            doc_type = "_doc"

        return await self.transport.perform_request(
            "POST" if id in SKIP_IN_PATH else "PUT",
            _make_path(index, doc_type, id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "pipeline",
        "refresh",
        "require_alias",
        "routing",
        "timeout",
        "wait_for_active_shards",
    )
    async def bulk(self, body, index=None, doc_type=None, params=None, headers=None):
        """
        Allows to perform multiple index/update/delete operations in a single request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-bulk.html>`_

        :arg body: The operation definition and data (action-data
            pairs), separated by newlines
        :arg index: Default index for items which don't provide one
        :arg doc_type: Default document type for items which don't
            provide one
        :arg _source: True or false to return the _source field or not,
            or default list of fields to return, can be overridden on each sub-
            request
        :arg _source_excludes: Default list of fields to exclude from
            the returned _source field, can be overridden on each sub-request
        :arg _source_includes: Default list of fields to extract and
            return from the _source field, can be overridden on each sub-request
        :arg pipeline: The pipeline id to preprocess incoming documents
            with
        :arg refresh: If `true` then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh
            to make this operation visible to search, if `false` (the default) then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        :arg require_alias: Sets require_alias for all incoming
            documents. Defaults to unset (false)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the bulk operation. Defaults
            to 1, meaning the primary shard only. Set to `all` for all shard copies,
            otherwise set to any non-negative value less than or equal to the total
            number of copies for the shard (number of replicas + 1)
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_bulk"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def clear_scroll(self, body=None, scroll_id=None, params=None, headers=None):
        """
        Explicitly clears the search context for a scroll.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/clear-scroll-api.html>`_

        :arg body: A comma-separated list of scroll IDs to clear if none
            was specified via the scroll_id parameter
        :arg scroll_id: A comma-separated list of scroll IDs to clear
        """
        if scroll_id in SKIP_IN_PATH and body in SKIP_IN_PATH:
            raise ValueError("You need to supply scroll_id or body.")
        elif scroll_id and not body:
            body = {"scroll_id": [scroll_id]}
        elif scroll_id:
            params["scroll_id"] = scroll_id

        return await self.transport.perform_request(
            "DELETE", "/_search/scroll", params=params, headers=headers, body=body
        )

    @query_params(
        "allow_no_indices",
        "analyze_wildcard",
        "analyzer",
        "default_operator",
        "df",
        "expand_wildcards",
        "ignore_throttled",
        "ignore_unavailable",
        "lenient",
        "min_score",
        "preference",
        "q",
        "routing",
        "terminate_after",
    )
    async def count(
        self, body=None, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Returns number of documents matching a query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-count.html>`_

        :arg body: A query to restrict the results specified with the
            Query DSL (optional)
        :arg index: A comma-separated list of indices to restrict the
            results
        :arg doc_type: A comma-separated list of types to restrict the
            results
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyze_wildcard: Specify whether wildcard and prefix
            queries should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string
            query (AND or OR)  Valid choices: AND, OR  Default: OR
        :arg df: The field to use as default where no field prefix is
            given in the query string
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_throttled: Whether specified concrete, expanded or
            aliased indices should be ignored when throttled
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such
            as providing text to a numeric field) should be ignored
        :arg min_score: Include only documents with a specific `_score`
            value in the result
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: A comma-separated list of specific routing values
        :arg terminate_after: The maximum count for each shard, upon
            reaching which the query execution will terminate early
        """
        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_count"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "if_primary_term",
        "if_seq_no",
        "refresh",
        "routing",
        "timeout",
        "version",
        "version_type",
        "wait_for_active_shards",
    )
    async def delete(self, index, id, doc_type=None, params=None, headers=None):
        """
        Removes a document from the index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-delete.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document
        :arg if_primary_term: only perform the delete operation if the
            last operation that has changed the document has the specified primary
            term
        :arg if_seq_no: only perform the delete operation if the last
            operation that has changed the document has the specified sequence
            number
        :arg refresh: If `true` then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh
            to make this operation visible to search, if `false` (the default) then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte, force
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the delete operation.
            Defaults to 1, meaning the primary shard only. Set to `all` for all
            shard copies, otherwise set to any non-negative value less than or equal
            to the total number of copies for the shard (number of replicas + 1)
        """
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            doc_type = "_doc"

        return await self.transport.perform_request(
            "DELETE", _make_path(index, doc_type, id), params=params, headers=headers
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "allow_no_indices",
        "analyze_wildcard",
        "analyzer",
        "conflicts",
        "default_operator",
        "df",
        "expand_wildcards",
        "from_",
        "ignore_unavailable",
        "lenient",
        "max_docs",
        "preference",
        "q",
        "refresh",
        "request_cache",
        "requests_per_second",
        "routing",
        "scroll",
        "scroll_size",
        "search_timeout",
        "search_type",
        "size",
        "slices",
        "sort",
        "stats",
        "terminate_after",
        "timeout",
        "version",
        "wait_for_active_shards",
        "wait_for_completion",
    )
    async def delete_by_query(
        self, index, body, doc_type=None, params=None, headers=None
    ):
        """
        Deletes documents matching the provided query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-delete-by-query.html>`_

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg body: The search definition using the Query DSL
        :arg doc_type: A comma-separated list of document types to
            search; leave empty to perform the operation on all types
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyze_wildcard: Specify whether wildcard and prefix
            queries should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg conflicts: What to do when the delete by query hits version
            conflicts?  Valid choices: abort, proceed  Default: abort
        :arg default_operator: The default operator for query string
            query (AND or OR)  Valid choices: AND, OR  Default: OR
        :arg df: The field to use as default where no field prefix is
            given in the query string
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg from_: Starting offset (default: 0)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such
            as providing text to a numeric field) should be ignored
        :arg max_docs: Maximum number of documents to process (default:
            all documents)
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg refresh: Should the effected indexes be refreshed?
        :arg request_cache: Specify if request cache should be used for
            this request or not, defaults to index level setting
        :arg requests_per_second: The throttle for this request in sub-
            requests per second. -1 means no throttle.
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index
            should be maintained for scrolled search
        :arg scroll_size: Size on the scroll request powering the delete
            by query  Default: 100
        :arg search_timeout: Explicit timeout for each search request.
            Defaults to no timeout.
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, dfs_query_then_fetch
        :arg size: Deprecated, please use `max_docs` instead
        :arg slices: The number of slices this task should be divided
            into. Defaults to 1, meaning the task isn't sliced into subtasks. Can be
            set to `auto`.  Default: 1
        :arg sort: A comma-separated list of <field>:<direction> pairs
        :arg stats: Specific 'tag' of the request for logging and
            statistical purposes
        :arg terminate_after: The maximum number of documents to collect
            for each shard, upon reaching which the query execution will terminate
            early.
        :arg timeout: Time each individual bulk request should wait for
            shards that are unavailable.  Default: 1m
        :arg version: Specify whether to return document version as part
            of a hit
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the delete by query
            operation. Defaults to 1, meaning the primary shard only. Set to `all`
            for all shard copies, otherwise set to any non-negative value less than
            or equal to the total number of copies for the shard (number of replicas
            + 1)
        :arg wait_for_completion: Should the request should block until
            the delete by query is complete.  Default: True
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_delete_by_query"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("requests_per_second")
    async def delete_by_query_rethrottle(self, task_id, params=None, headers=None):
        """
        Changes the number of requests per second for a particular Delete By Query
        operation.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-delete-by-query.html>`_

        :arg task_id: The task id to rethrottle
        :arg requests_per_second: The throttle to set on this request in
            floating sub-requests per second. -1 means set no throttle.
        """
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'task_id'.")

        return await self.transport.perform_request(
            "POST",
            _make_path("_delete_by_query", task_id, "_rethrottle"),
            params=params,
            headers=headers,
        )

    @query_params("master_timeout", "timeout")
    async def delete_script(self, id, params=None, headers=None):
        """
        Deletes a script.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/modules-scripting.html>`_

        :arg id: Script ID
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return await self.transport.perform_request(
            "DELETE", _make_path("_scripts", id), params=params, headers=headers
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "preference",
        "realtime",
        "refresh",
        "routing",
        "stored_fields",
        "version",
        "version_type",
    )
    async def exists(self, index, id, doc_type=None, params=None, headers=None):
        """
        Returns information about whether a document exists in an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document (use `_all` to fetch the
            first document matching the ID across all types)
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg realtime: Specify whether to perform the operation in
            realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg stored_fields: A comma-separated list of stored fields to
            return in the response
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte, force
        """
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            doc_type = "_doc"

        return await self.transport.perform_request(
            "HEAD", _make_path(index, doc_type, id), params=params, headers=headers
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "preference",
        "realtime",
        "refresh",
        "routing",
        "version",
        "version_type",
    )
    async def exists_source(self, index, id, doc_type=None, params=None, headers=None):
        """
        Returns information about whether a document source exists in an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document; deprecated and optional
            starting with 7.0
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg realtime: Specify whether to perform the operation in
            realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte, force
        """
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_source", id)
        else:
            path = _make_path(index, doc_type, id, "_source")

        return await self.transport.perform_request(
            "HEAD", path, params=params, headers=headers
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "analyze_wildcard",
        "analyzer",
        "default_operator",
        "df",
        "lenient",
        "preference",
        "q",
        "routing",
        "stored_fields",
    )
    async def explain(
        self, index, id, body=None, doc_type=None, params=None, headers=None
    ):
        """
        Returns information about why a specific matches (or doesn't match) a query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-explain.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg body: The query definition using the Query DSL
        :arg doc_type: The type of the document
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg analyze_wildcard: Specify whether wildcards and prefix
            queries in the query string query should be analyzed (default: false)
        :arg analyzer: The analyzer for the query string query
        :arg default_operator: The default operator for query string
            query (AND or OR)  Valid choices: AND, OR  Default: OR
        :arg df: The default field for query string query (default:
            _all)
        :arg lenient: Specify whether format-based query failures (such
            as providing text to a numeric field) should be ignored
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        :arg stored_fields: A comma-separated list of stored fields to
            return in the response
        """
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_explain", id)
        else:
            path = _make_path(index, doc_type, id, "_explain")

        return await self.transport.perform_request(
            "POST", path, params=params, headers=headers, body=body
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "fields",
        "ignore_unavailable",
        "include_unmapped",
    )
    async def field_caps(self, body=None, index=None, params=None, headers=None):
        """
        Returns the information about the capabilities of fields among multiple
        indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-field-caps.html>`_

        :arg body: An index filter specified with the Query DSL
        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg fields: A comma-separated list of field names
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg include_unmapped: Indicates whether unmapped fields should
            be included in the response.
        """
        return await self.transport.perform_request(
            "POST",
            _make_path(index, "_field_caps"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "preference",
        "realtime",
        "refresh",
        "routing",
        "stored_fields",
        "version",
        "version_type",
    )
    async def get(self, index, id, doc_type=None, params=None, headers=None):
        """
        Returns a document.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document (use `_all` to fetch the
            first document matching the ID across all types)
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg realtime: Specify whether to perform the operation in
            realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg stored_fields: A comma-separated list of stored fields to
            return in the response
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte, force
        """
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            doc_type = "_doc"

        return await self.transport.perform_request(
            "GET", _make_path(index, doc_type, id), params=params, headers=headers
        )

    @query_params("master_timeout")
    async def get_script(self, id, params=None, headers=None):
        """
        Returns a script.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/modules-scripting.html>`_

        :arg id: Script ID
        :arg master_timeout: Specify timeout for connection to master
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return await self.transport.perform_request(
            "GET", _make_path("_scripts", id), params=params, headers=headers
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "preference",
        "realtime",
        "refresh",
        "routing",
        "version",
        "version_type",
    )
    async def get_source(self, index, id, doc_type=None, params=None, headers=None):
        """
        Returns the source of a document.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document; deprecated and optional
            starting with 7.0
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg realtime: Specify whether to perform the operation in
            realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte, force
        """
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_source", id)
        else:
            path = _make_path(index, doc_type, id, "_source")

        return await self.transport.perform_request(
            "GET", path, params=params, headers=headers
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "preference",
        "realtime",
        "refresh",
        "routing",
        "stored_fields",
    )
    async def mget(self, body, index=None, doc_type=None, params=None, headers=None):
        """
        Allows to get multiple documents in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-multi-get.html>`_

        :arg body: Document identifiers; can be either `docs`
            (containing full document information) or `ids` (when index and type is
            provided in the URL.
        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg realtime: Specify whether to perform the operation in
            realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg stored_fields: A comma-separated list of stored fields to
            return in the response
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_mget"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "ccs_minimize_roundtrips",
        "max_concurrent_searches",
        "max_concurrent_shard_requests",
        "pre_filter_shard_size",
        "rest_total_hits_as_int",
        "search_type",
        "typed_keys",
    )
    async def msearch(self, body, index=None, doc_type=None, params=None, headers=None):
        """
        Allows to execute several search operations in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-multi-search.html>`_

        :arg body: The request definitions (metadata-search request
            definition pairs), separated by newlines
        :arg index: A comma-separated list of index names to use as
            default
        :arg doc_type: A comma-separated list of document types to use
            as default
        :arg ccs_minimize_roundtrips: Indicates whether network round-
            trips should be minimized as part of cross-cluster search requests
            execution  Default: true
        :arg max_concurrent_searches: Controls the maximum number of
            concurrent searches the multi search api will execute
        :arg max_concurrent_shard_requests: The number of concurrent
            shard requests each sub search executes concurrently per node. This
            value should be used to limit the impact of the search on the cluster in
            order to limit the number of concurrent shard requests  Default: 5
        :arg pre_filter_shard_size: A threshold that enforces a pre-
            filter roundtrip to prefilter search shards based on query rewriting if
            the number of shards the search request expands to exceeds the
            threshold. This filter roundtrip can limit the number of shards
            significantly if for instance a shard can not match any documents based
            on its rewrite method ie. if date filters are mandatory to match but the
            shard bounds and the query are disjoint.
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, query_and_fetch, dfs_query_then_fetch,
            dfs_query_and_fetch
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_msearch"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "ccs_minimize_roundtrips",
        "max_concurrent_searches",
        "rest_total_hits_as_int",
        "search_type",
        "typed_keys",
    )
    async def msearch_template(
        self, body, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Allows to execute several search template operations in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-multi-search.html>`_

        :arg body: The request definitions (metadata-search request
            definition pairs), separated by newlines
        :arg index: A comma-separated list of index names to use as
            default
        :arg doc_type: A comma-separated list of document types to use
            as default
        :arg ccs_minimize_roundtrips: Indicates whether network round-
            trips should be minimized as part of cross-cluster search requests
            execution  Default: true
        :arg max_concurrent_searches: Controls the maximum number of
            concurrent searches the multi search api will execute
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, query_and_fetch, dfs_query_then_fetch,
            dfs_query_and_fetch
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_msearch", "template"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "field_statistics",
        "fields",
        "ids",
        "offsets",
        "payloads",
        "positions",
        "preference",
        "realtime",
        "routing",
        "term_statistics",
        "version",
        "version_type",
    )
    async def mtermvectors(
        self, body=None, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Returns multiple termvectors in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-multi-termvectors.html>`_

        :arg body: Define ids, documents, parameters or a list of
            parameters per document here. You must at least provide a list of
            document ids. See documentation.
        :arg index: The index in which the document resides.
        :arg doc_type: The type of the document.
        :arg field_statistics: Specifies if document count, sum of
            document frequencies and sum of total term frequencies should be
            returned. Applies to all returned documents unless otherwise specified
            in body "params" or "docs".  Default: True
        :arg fields: A comma-separated list of fields to return. Applies
            to all returned documents unless otherwise specified in body "params" or
            "docs".
        :arg ids: A comma-separated list of documents ids. You must
            define ids as parameter or set "ids" or "docs" in the request body
        :arg offsets: Specifies if term offsets should be returned.
            Applies to all returned documents unless otherwise specified in body
            "params" or "docs".  Default: True
        :arg payloads: Specifies if term payloads should be returned.
            Applies to all returned documents unless otherwise specified in body
            "params" or "docs".  Default: True
        :arg positions: Specifies if term positions should be returned.
            Applies to all returned documents unless otherwise specified in body
            "params" or "docs".  Default: True
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random) .Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg realtime: Specifies if requests are real-time as opposed to
            near-real-time (default: true).
        :arg routing: Specific routing value. Applies to all returned
            documents unless otherwise specified in body "params" or "docs".
        :arg term_statistics: Specifies if total term frequency and
            document frequency should be returned. Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte, force
        """
        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_mtermvectors")
        else:
            path = _make_path(index, doc_type, "_mtermvectors")

        return await self.transport.perform_request(
            "POST", path, params=params, headers=headers, body=body
        )

    @query_params("master_timeout", "timeout")
    async def put_script(self, id, body, context=None, params=None, headers=None):
        """
        Creates or updates a script.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/modules-scripting.html>`_

        :arg id: Script ID
        :arg body: The document
        :arg context: Context name to compile script against
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_scripts", id, context),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "allow_no_indices", "expand_wildcards", "ignore_unavailable", "search_type"
    )
    async def rank_eval(self, body, index=None, params=None, headers=None):
        """
        Allows to evaluate the quality of ranked search results over a set of typical
        search queries

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-rank-eval.html>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg body: The ranking evaluation search definition, including
            search requests, document ratings and ranking metric definition.
        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, dfs_query_then_fetch
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST",
            _make_path(index, "_rank_eval"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "max_docs",
        "refresh",
        "requests_per_second",
        "scroll",
        "slices",
        "timeout",
        "wait_for_active_shards",
        "wait_for_completion",
    )
    async def reindex(self, body, params=None, headers=None):
        """
        Allows to copy documents from one index to another, optionally filtering the
        source documents by a query, changing the destination index settings, or
        fetching the documents from a remote cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-reindex.html>`_

        :arg body: The search definition using the Query DSL and the
            prototype for the index request.
        :arg max_docs: Maximum number of documents to process (default:
            all documents)
        :arg refresh: Should the affected indexes be refreshed?
        :arg requests_per_second: The throttle to set on this request in
            sub-requests per second. -1 means no throttle.
        :arg scroll: Control how long to keep the search context alive
            Default: 5m
        :arg slices: The number of slices this task should be divided
            into. Defaults to 1, meaning the task isn't sliced into subtasks. Can be
            set to `auto`.  Default: 1
        :arg timeout: Time each individual bulk request should wait for
            shards that are unavailable.  Default: 1m
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the reindex operation.
            Defaults to 1, meaning the primary shard only. Set to `all` for all
            shard copies, otherwise set to any non-negative value less than or equal
            to the total number of copies for the shard (number of replicas + 1)
        :arg wait_for_completion: Should the request should block until
            the reindex is complete.  Default: True
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST", "/_reindex", params=params, headers=headers, body=body
        )

    @query_params("requests_per_second")
    async def reindex_rethrottle(self, task_id, params=None, headers=None):
        """
        Changes the number of requests per second for a particular Reindex operation.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-reindex.html>`_

        :arg task_id: The task id to rethrottle
        :arg requests_per_second: The throttle to set on this request in
            floating sub-requests per second. -1 means set no throttle.
        """
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'task_id'.")

        return await self.transport.perform_request(
            "POST",
            _make_path("_reindex", task_id, "_rethrottle"),
            params=params,
            headers=headers,
        )

    @query_params()
    async def render_search_template(
        self, body=None, id=None, params=None, headers=None
    ):
        """
        Allows to use the Mustache language to pre-render a search definition.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/render-search-template-api.html>`_

        :arg body: The search definition template and its params
        :arg id: The id of the stored search template
        """
        return await self.transport.perform_request(
            "POST",
            _make_path("_render", "template", id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def scripts_painless_execute(self, body=None, params=None, headers=None):
        """
        Allows an arbitrary script to be executed and a result to be returned

        `<https://www.elastic.co/guide/en/elasticsearch/painless/master/painless-execute-api.html>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg body: The script to execute
        """
        return await self.transport.perform_request(
            "POST",
            "/_scripts/painless/_execute",
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("rest_total_hits_as_int", "scroll")
    async def scroll(self, body=None, scroll_id=None, params=None, headers=None):
        """
        Allows to retrieve a large numbers of results from a single search request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-request-body.html#request-body-search-scroll>`_

        :arg body: The scroll ID if not passed by URL or query
            parameter.
        :arg scroll_id: The scroll ID for scrolled search
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg scroll: Specify how long a consistent view of the index
            should be maintained for scrolled search
        """
        if scroll_id in SKIP_IN_PATH and body in SKIP_IN_PATH:
            raise ValueError("You need to supply scroll_id or body.")
        elif scroll_id and not body:
            body = {"scroll_id": scroll_id}
        elif scroll_id:
            params["scroll_id"] = scroll_id

        return await self.transport.perform_request(
            "POST", "/_search/scroll", params=params, headers=headers, body=body
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "allow_no_indices",
        "allow_partial_search_results",
        "analyze_wildcard",
        "analyzer",
        "batched_reduce_size",
        "ccs_minimize_roundtrips",
        "default_operator",
        "df",
        "docvalue_fields",
        "expand_wildcards",
        "explain",
        "from_",
        "ignore_throttled",
        "ignore_unavailable",
        "lenient",
        "max_concurrent_shard_requests",
        "min_compatible_shard_node",
        "pre_filter_shard_size",
        "preference",
        "q",
        "request_cache",
        "rest_total_hits_as_int",
        "routing",
        "scroll",
        "search_type",
        "seq_no_primary_term",
        "size",
        "sort",
        "stats",
        "stored_fields",
        "suggest_field",
        "suggest_mode",
        "suggest_size",
        "suggest_text",
        "terminate_after",
        "timeout",
        "track_scores",
        "track_total_hits",
        "typed_keys",
        "version",
    )
    async def search(
        self, body=None, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Returns results matching a query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-search.html>`_

        :arg body: The search definition using the Query DSL
        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to
            search; leave empty to perform the operation on all types
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg allow_partial_search_results: Indicate if an error should
            be returned if there is a partial search failure or timeout  Default:
            True
        :arg analyze_wildcard: Specify whether wildcard and prefix
            queries should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg batched_reduce_size: The number of shard results that
            should be reduced at once on the coordinating node. This value should be
            used as a protection mechanism to reduce the memory overhead per search
            request if the potential number of shards in the request can be large.
            Default: 512
        :arg ccs_minimize_roundtrips: Indicates whether network round-
            trips should be minimized as part of cross-cluster search requests
            execution  Default: true
        :arg default_operator: The default operator for query string
            query (AND or OR)  Valid choices: AND, OR  Default: OR
        :arg df: The field to use as default where no field prefix is
            given in the query string
        :arg docvalue_fields: A comma-separated list of fields to return
            as the docvalue representation of a field for each hit
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg explain: Specify whether to return detailed information
            about score computation as part of a hit
        :arg from_: Starting offset (default: 0)
        :arg ignore_throttled: Whether specified concrete, expanded or
            aliased indices should be ignored when throttled
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such
            as providing text to a numeric field) should be ignored
        :arg max_concurrent_shard_requests: The number of concurrent
            shard requests per node this search executes concurrently. This value
            should be used to limit the impact of the search on the cluster in order
            to limit the number of concurrent shard requests  Default: 5
        :arg min_compatible_shard_node: The minimum compatible version
            that all shards involved in search should have for this request to be
            successful
        :arg pre_filter_shard_size: A threshold that enforces a pre-
            filter roundtrip to prefilter search shards based on query rewriting if
            the number of shards the search request expands to exceeds the
            threshold. This filter roundtrip can limit the number of shards
            significantly if for instance a shard can not match any documents based
            on its rewrite method ie. if date filters are mandatory to match but the
            shard bounds and the query are disjoint.
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg request_cache: Specify if request cache should be used for
            this request or not, defaults to index level setting
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index
            should be maintained for scrolled search
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, dfs_query_then_fetch
        :arg seq_no_primary_term: Specify whether to return sequence
            number and primary term of the last modification of each hit
        :arg size: Number of hits to return (default: 10)
        :arg sort: A comma-separated list of <field>:<direction> pairs
        :arg stats: Specific 'tag' of the request for logging and
            statistical purposes
        :arg stored_fields: A comma-separated list of stored fields to
            return as part of a hit
        :arg suggest_field: Specify which field to use for suggestions
        :arg suggest_mode: Specify suggest mode  Valid choices: missing,
            popular, always  Default: missing
        :arg suggest_size: How many suggestions to return in response
        :arg suggest_text: The source text for which the suggestions
            should be returned
        :arg terminate_after: The maximum number of documents to collect
            for each shard, upon reaching which the query execution will terminate
            early.
        :arg timeout: Explicit operation timeout
        :arg track_scores: Whether to calculate and return scores even
            if they are not used for sorting
        :arg track_total_hits: Indicate if the number of documents that
            match the query should be tracked
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        :arg version: Specify whether to return document version as part
            of a hit
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_search"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "local",
        "preference",
        "routing",
    )
    async def search_shards(self, index=None, params=None, headers=None):
        """
        Returns information about the indices and shards that a search request would be
        executed against.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-shards.html>`_

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg routing: Specific routing value
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_search_shards"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "ccs_minimize_roundtrips",
        "expand_wildcards",
        "explain",
        "ignore_throttled",
        "ignore_unavailable",
        "preference",
        "profile",
        "rest_total_hits_as_int",
        "routing",
        "scroll",
        "search_type",
        "typed_keys",
    )
    async def search_template(
        self, body, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Allows to use the Mustache language to pre-render a search definition.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/search-template.html>`_

        :arg body: The search definition template and its params
        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to
            search; leave empty to perform the operation on all types
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg ccs_minimize_roundtrips: Indicates whether network round-
            trips should be minimized as part of cross-cluster search requests
            execution  Default: true
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg explain: Specify whether to return detailed information
            about score computation as part of a hit
        :arg ignore_throttled: Whether specified concrete, expanded or
            aliased indices should be ignored when throttled
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg profile: Specify whether to profile the query execution
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index
            should be maintained for scrolled search
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, query_and_fetch, dfs_query_then_fetch,
            dfs_query_and_fetch
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_search", "template"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "field_statistics",
        "fields",
        "offsets",
        "payloads",
        "positions",
        "preference",
        "realtime",
        "routing",
        "term_statistics",
        "version",
        "version_type",
    )
    async def termvectors(
        self, index, body=None, doc_type=None, id=None, params=None, headers=None
    ):
        """
        Returns information and statistics about terms in the fields of a particular
        document.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-termvectors.html>`_

        :arg index: The index in which the document resides.
        :arg body: Define parameters and or supply a document to get
            termvectors for. See documentation.
        :arg doc_type: The type of the document.
        :arg id: The id of the document, when not specified a doc param
            should be supplied.
        :arg field_statistics: Specifies if document count, sum of
            document frequencies and sum of total term frequencies should be
            returned.  Default: True
        :arg fields: A comma-separated list of fields to return.
        :arg offsets: Specifies if term offsets should be returned.
            Default: True
        :arg payloads: Specifies if term payloads should be returned.
            Default: True
        :arg positions: Specifies if term positions should be returned.
            Default: True
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random).
        :arg realtime: Specifies if request is real-time as opposed to
            near-real-time (default: true).
        :arg routing: Specific routing value.
        :arg term_statistics: Specifies if total term frequency and
            document frequency should be returned.
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type  Valid choices:
            internal, external, external_gte, force
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_termvectors", id)
        else:
            path = _make_path(index, doc_type, id, "_termvectors")

        return await self.transport.perform_request(
            "POST", path, params=params, headers=headers, body=body
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "if_primary_term",
        "if_seq_no",
        "lang",
        "refresh",
        "require_alias",
        "retry_on_conflict",
        "routing",
        "timeout",
        "wait_for_active_shards",
    )
    async def update(self, index, id, body, doc_type=None, params=None, headers=None):
        """
        Updates a document with a script or partial document.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-update.html>`_

        :arg index: The name of the index
        :arg id: Document ID
        :arg body: The request definition requires either `script` or
            partial `doc`
        :arg doc_type: The type of the document
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg if_primary_term: only perform the update operation if the
            last operation that has changed the document has the specified primary
            term
        :arg if_seq_no: only perform the update operation if the last
            operation that has changed the document has the specified sequence
            number
        :arg lang: The script language (default: painless)
        :arg refresh: If `true` then refresh the affected shards to make
            this operation visible to search, if `wait_for` then wait for a refresh
            to make this operation visible to search, if `false` (the default) then
            do nothing with refreshes.  Valid choices: true, false, wait_for
        :arg require_alias: When true, requires destination is an alias.
            Default is false
        :arg retry_on_conflict: Specify how many times should the
            operation be retried when a conflict occurs (default: 0)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the update operation.
            Defaults to 1, meaning the primary shard only. Set to `all` for all
            shard copies, otherwise set to any non-negative value less than or equal
            to the total number of copies for the shard (number of replicas + 1)
        """
        for param in (index, id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_update", id)
        else:
            path = _make_path(index, doc_type, id, "_update")

        return await self.transport.perform_request(
            "POST", path, params=params, headers=headers, body=body
        )

    @query_params(
        "_source",
        "_source_excludes",
        "_source_includes",
        "allow_no_indices",
        "analyze_wildcard",
        "analyzer",
        "conflicts",
        "default_operator",
        "df",
        "expand_wildcards",
        "from_",
        "ignore_unavailable",
        "lenient",
        "max_docs",
        "pipeline",
        "preference",
        "q",
        "refresh",
        "request_cache",
        "requests_per_second",
        "routing",
        "scroll",
        "scroll_size",
        "search_timeout",
        "search_type",
        "size",
        "slices",
        "sort",
        "stats",
        "terminate_after",
        "timeout",
        "version",
        "version_type",
        "wait_for_active_shards",
        "wait_for_completion",
    )
    async def update_by_query(
        self, index, body=None, doc_type=None, params=None, headers=None
    ):
        """
        Performs an update on every document in the index without changing the source,
        for example to pick up a mapping change.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-update-by-query.html>`_

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg body: The search definition using the Query DSL
        :arg doc_type: A comma-separated list of document types to
            search; leave empty to perform the operation on all types
        :arg _source: True or false to return the _source field or not,
            or a list of fields to return
        :arg _source_excludes: A list of fields to exclude from the
            returned _source field
        :arg _source_includes: A list of fields to extract and return
            from the _source field
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyze_wildcard: Specify whether wildcard and prefix
            queries should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg conflicts: What to do when the update by query hits version
            conflicts?  Valid choices: abort, proceed  Default: abort
        :arg default_operator: The default operator for query string
            query (AND or OR)  Valid choices: AND, OR  Default: OR
        :arg df: The field to use as default where no field prefix is
            given in the query string
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg from_: Starting offset (default: 0)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such
            as providing text to a numeric field) should be ignored
        :arg max_docs: Maximum number of documents to process (default:
            all documents)
        :arg pipeline: Ingest pipeline to set on index requests made by
            this action. (default: none)
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg refresh: Should the affected indexes be refreshed?
        :arg request_cache: Specify if request cache should be used for
            this request or not, defaults to index level setting
        :arg requests_per_second: The throttle to set on this request in
            sub-requests per second. -1 means no throttle.
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index
            should be maintained for scrolled search
        :arg scroll_size: Size on the scroll request powering the update
            by query  Default: 100
        :arg search_timeout: Explicit timeout for each search request.
            Defaults to no timeout.
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, dfs_query_then_fetch
        :arg size: Deprecated, please use `max_docs` instead
        :arg slices: The number of slices this task should be divided
            into. Defaults to 1, meaning the task isn't sliced into subtasks. Can be
            set to `auto`.  Default: 1
        :arg sort: A comma-separated list of <field>:<direction> pairs
        :arg stats: Specific 'tag' of the request for logging and
            statistical purposes
        :arg terminate_after: The maximum number of documents to collect
            for each shard, upon reaching which the query execution will terminate
            early.
        :arg timeout: Time each individual bulk request should wait for
            shards that are unavailable.  Default: 1m
        :arg version: Specify whether to return document version as part
            of a hit
        :arg version_type: Should the document increment the version
            number (internal) on hit or not (reindex)
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the update by query
            operation. Defaults to 1, meaning the primary shard only. Set to `all`
            for all shard copies, otherwise set to any non-negative value less than
            or equal to the total number of copies for the shard (number of replicas
            + 1)
        :arg wait_for_completion: Should the request should block until
            the update by query operation is complete.  Default: True
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if "from_" in params:
            params["from"] = params.pop("from_")

        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_update_by_query"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("requests_per_second")
    async def update_by_query_rethrottle(self, task_id, params=None, headers=None):
        """
        Changes the number of requests per second for a particular Update By Query
        operation.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/docs-update-by-query.html>`_

        :arg task_id: The task id to rethrottle
        :arg requests_per_second: The throttle to set on this request in
            floating sub-requests per second. -1 means set no throttle.
        """
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'task_id'.")

        return await self.transport.perform_request(
            "POST",
            _make_path("_update_by_query", task_id, "_rethrottle"),
            params=params,
            headers=headers,
        )

    @query_params()
    async def get_script_context(self, params=None, headers=None):
        """
        Returns all script contexts.

        `<https://www.elastic.co/guide/en/elasticsearch/painless/master/painless-contexts.html>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version
        """
        return await self.transport.perform_request(
            "GET", "/_script_context", params=params, headers=headers
        )

    @query_params()
    async def get_script_languages(self, params=None, headers=None):
        """
        Returns available script types, languages and contexts

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/modules-scripting.html>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version
        """
        return await self.transport.perform_request(
            "GET", "/_script_language", params=params, headers=headers
        )

    @query_params()
    async def close_point_in_time(self, body=None, params=None, headers=None):
        """
        Close a point in time

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/point-in-time-api.html>`_

        :arg body: a point-in-time id to close
        """
        return await self.transport.perform_request(
            "DELETE", "/_pit", params=params, headers=headers, body=body
        )

    @query_params(
        "expand_wildcards", "ignore_unavailable", "keep_alive", "preference", "routing"
    )
    async def open_point_in_time(self, index=None, params=None, headers=None):
        """
        Open a point in time that can be used in subsequent searches

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/point-in-time-api.html>`_

        :arg index: A comma-separated list of index names to open point
            in time; use `_all` or empty string to perform the operation on all
            indices
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg keep_alive: Specific the time to live for the point in time
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg routing: Specific routing value
        """
        return await self.transport.perform_request(
            "POST", _make_path(index, "_pit"), params=params, headers=headers
        )

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


import logging
import warnings
from typing import Any, Callable, Dict, Optional, Union

from elastic_transport import AsyncTransport, NodeConfig, TransportError
from elastic_transport.client_utils import DEFAULT

from ...exceptions import NotFoundError
from ...serializer import DEFAULT_SERIALIZERS
from ._base import (
    BaseClient,
    create_sniff_callback,
    default_sniff_callback,
    resolve_auth_headers,
)
from .async_search import AsyncSearchClient
from .autoscaling import AutoscalingClient
from .cat import CatClient
from .ccr import CcrClient
from .cluster import ClusterClient
from .dangling_indices import DanglingIndicesClient
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
from .utils import (
    _TYPE_HOSTS,
    CLIENT_META_SERVICE,
    SKIP_IN_PATH,
    _deprecated_options,
    _make_path,
    client_node_configs,
    query_params,
)
from .watcher import WatcherClient
from .xpack import XPackClient

logger = logging.getLogger("elasticsearch")


class AsyncElasticsearch(BaseClient):
    """
    Elasticsearch low-level client. Provides a straightforward mapping from
    Python to Elasticsearch REST APIs.

    The client instance has additional attributes to update APIs in different
    namespaces such as ``async_search``, ``indices``, ``security``, and more:

    .. code-block:: python

        client = Elasticsearch("http://localhost:9200")

        # Get Document API
        client.get(index="*", id="1")

        # Get Index API
        client.indices.get(index="*")

    Transport options can be set on the client constructor or using
    the :meth:`~elasticsearch.Elasticsearch.options` method:

    .. code-block:: python

        # Set 'api_key' on the constructor
        client = Elasticsearch(
            "http://localhost:9200",
            api_key=("id", "api_key")
        )
        client.search(...)

        # Set 'api_key' per request
        client.options(api_key=("id", "api_key")).search(...)
    """

    def __init__(
        self,
        hosts: Optional[_TYPE_HOSTS] = None,
        *,
        # API
        cloud_id: Optional[str] = None,
        api_key=None,
        basic_auth=None,
        bearer_auth=None,
        opaque_id=None,
        # Node
        headers=DEFAULT,
        connections_per_node=DEFAULT,
        http_compress=DEFAULT,
        verify_certs=DEFAULT,
        ca_certs=DEFAULT,
        client_cert=DEFAULT,
        client_key=DEFAULT,
        ssl_assert_hostname=DEFAULT,
        ssl_assert_fingerprint=DEFAULT,
        ssl_version=DEFAULT,
        ssl_context=DEFAULT,
        ssl_show_warn=DEFAULT,
        # Transport
        transport_class=AsyncTransport,
        request_timeout=DEFAULT,
        node_class=DEFAULT,
        node_pool_class=DEFAULT,
        randomize_nodes_in_pool=DEFAULT,
        node_selector_class=DEFAULT,
        dead_node_backoff_factor=DEFAULT,
        max_dead_node_backoff=DEFAULT,
        serializers=DEFAULT,
        default_mimetype="application/json",
        max_retries=DEFAULT,
        retry_on_status=DEFAULT,
        retry_on_timeout=DEFAULT,
        sniff_on_start=DEFAULT,
        sniff_before_requests=DEFAULT,
        sniff_on_node_failure=DEFAULT,
        sniff_timeout=DEFAULT,
        min_delay_between_sniffing=DEFAULT,
        sniffed_node_callback: Optional[
            Callable[[Dict[str, Any], NodeConfig], Optional[NodeConfig]]
        ] = None,
        meta_header=DEFAULT,
        # Deprecated
        timeout=DEFAULT,
        randomize_hosts=DEFAULT,
        host_info_callback: Optional[
            Callable[
                [Dict[str, Any], Dict[str, Union[str, int]]],
                Optional[Dict[str, Union[str, int]]],
            ]
        ] = None,
        sniffer_timeout=DEFAULT,
        sniff_on_connection_fail=DEFAULT,
        # Internal use only
        _transport: Optional[AsyncTransport] = None,
    ) -> None:
        if hosts is None and cloud_id is None and _transport is None:
            raise ValueError("Either 'hosts' or 'cloud_id' must be specified")

        if timeout is not DEFAULT:
            if request_timeout is not DEFAULT:
                raise ValueError(
                    "Can't specify both 'timeout' and 'request_timeout', "
                    "instead only specify 'request_timeout'"
                )
            warnings.warn(
                "The 'timeout' parameter is deprecated in favor of 'request_timeout'",
                category=DeprecationWarning,
                stacklevel=2,
            )
            request_timeout = timeout

        if randomize_hosts is not DEFAULT:
            if randomize_nodes_in_pool is not DEFAULT:
                raise ValueError(
                    "Can't specify both 'randomize_hosts' and 'randomize_nodes_in_pool', "
                    "instead only specify 'randomize_nodes_in_pool'"
                )
            warnings.warn(
                "The 'randomize_hosts' parameter is deprecated in favor of 'randomize_nodes_in_pool'",
                category=DeprecationWarning,
                stacklevel=2,
            )
            randomize_nodes_in_pool = randomize_hosts

        if sniffer_timeout is not DEFAULT:
            if min_delay_between_sniffing is not DEFAULT:
                raise ValueError(
                    "Can't specify both 'sniffer_timeout' and 'min_delay_between_sniffing', "
                    "instead only specify 'min_delay_between_sniffing'"
                )
            warnings.warn(
                "The 'sniffer_timeout' parameter is deprecated in favor of 'min_delay_between_sniffing'",
                category=DeprecationWarning,
                stacklevel=2,
            )
            min_delay_between_sniffing = sniffer_timeout

        if sniff_on_connection_fail is not DEFAULT:
            if sniff_on_node_failure is not DEFAULT:
                raise ValueError(
                    "Can't specify both 'sniff_on_connection_fail' and 'sniff_on_node_failure', "
                    "instead only specify 'sniff_on_node_failure'"
                )
            warnings.warn(
                "The 'sniff_on_connection_fail' parameter is deprecated in favor of 'sniff_on_node_failure'",
                category=DeprecationWarning,
                stacklevel=2,
            )
            sniff_on_node_failure = sniff_on_connection_fail

        # Setting min_delay_between_sniffing=True implies sniff_before_requests=True
        if min_delay_between_sniffing is not DEFAULT:
            sniff_before_requests = True

        sniffing_options = (
            sniff_timeout,
            sniff_on_start,
            sniff_before_requests,
            sniff_on_node_failure,
            sniffed_node_callback,
            min_delay_between_sniffing,
            sniffed_node_callback,
        )
        if cloud_id is not None and any(
            x is not DEFAULT and x is not None for x in sniffing_options
        ):
            raise ValueError(
                "Sniffing should not be enabled when connecting to Elastic Cloud"
            )

        sniff_callback = None
        if host_info_callback is not None:
            if sniffed_node_callback is not None:
                raise ValueError(
                    "Can't specify both 'host_info_callback' and 'sniffed_node_callback', "
                    "instead only specify 'sniffed_node_callback'"
                )
            warnings.warn(
                "The 'host_info_callback' parameter is deprecated in favor of 'sniffed_node_callback'",
                category=DeprecationWarning,
                stacklevel=2,
            )

            sniff_callback = create_sniff_callback(
                host_info_callback=host_info_callback
            )
        elif sniffed_node_callback is not None:
            sniff_callback = create_sniff_callback(
                sniffed_node_callback=sniffed_node_callback
            )
        elif (
            sniff_on_start is True
            or sniff_before_requests is True
            or sniff_on_node_failure is True
        ):
            sniff_callback = default_sniff_callback

        if _transport is None:
            node_configs = client_node_configs(
                hosts,
                cloud_id=cloud_id,
                connections_per_node=connections_per_node,
                http_compress=http_compress,
                verify_certs=verify_certs,
                ca_certs=ca_certs,
                client_cert=client_cert,
                client_key=client_key,
                ssl_assert_hostname=ssl_assert_hostname,
                ssl_assert_fingerprint=ssl_assert_fingerprint,
                ssl_version=ssl_version,
                ssl_context=ssl_context,
                ssl_show_warn=ssl_show_warn,
            )
            transport_kwargs = {}
            if node_class is not DEFAULT:
                transport_kwargs["node_class"] = node_class
            if node_pool_class is not DEFAULT:
                transport_kwargs["node_pool_class"] = node_class
            if randomize_nodes_in_pool is not DEFAULT:
                transport_kwargs["randomize_nodes_in_pool"] = randomize_nodes_in_pool
            if node_selector_class is not DEFAULT:
                transport_kwargs["node_selector_class"] = node_selector_class
            if dead_node_backoff_factor is not DEFAULT:
                transport_kwargs["dead_node_backoff_factor"] = dead_node_backoff_factor
            if max_dead_node_backoff is not DEFAULT:
                transport_kwargs["max_dead_node_backoff"] = max_dead_node_backoff
            if meta_header is not DEFAULT:
                transport_kwargs["meta_header"] = meta_header
            if serializers is DEFAULT:
                transport_kwargs["serializers"] = DEFAULT_SERIALIZERS
            else:
                transport_kwargs["serializers"] = serializers
            transport_kwargs["default_mimetype"] = default_mimetype
            if sniff_on_start is not DEFAULT:
                transport_kwargs["sniff_on_start"] = sniff_on_start
            if sniff_before_requests is not DEFAULT:
                transport_kwargs["sniff_before_requests"] = sniff_before_requests
            if sniff_on_node_failure is not DEFAULT:
                transport_kwargs["sniff_on_node_failure"] = sniff_on_node_failure
            if sniff_timeout is not DEFAULT:
                transport_kwargs["sniff_timeout"] = sniff_timeout
            if min_delay_between_sniffing is not DEFAULT:
                transport_kwargs[
                    "min_delay_between_sniffing"
                ] = min_delay_between_sniffing

            _transport = transport_class(
                node_configs,
                client_meta_service=CLIENT_META_SERVICE,
                sniff_callback=sniff_callback,
                **transport_kwargs,
            )

            super().__init__(_transport)

            # These are set per-request so are stored separately.
            self._request_timeout = request_timeout
            self._max_retries = max_retries
            self._retry_on_status = retry_on_status
            self._retry_on_timeout = retry_on_timeout

        else:
            super().__init__(_transport)

        if headers is not DEFAULT and headers is not None:
            self._headers.update(headers)
        if opaque_id is not DEFAULT and opaque_id is not None:
            self._headers["x-opaque-id"] = opaque_id
        self._headers = resolve_auth_headers(
            self._headers,
            api_key=api_key,
            basic_auth=basic_auth,
            bearer_auth=bearer_auth,
        )

        # namespaced clients for compatibility with API names
        self.async_search = AsyncSearchClient(self)
        self.autoscaling = AutoscalingClient(self)
        self.cat = CatClient(self)
        self.cluster = ClusterClient(self)
        self.features = FeaturesClient(self)
        self.indices = IndicesClient(self)
        self.ingest = IngestClient(self)
        self.nodes = NodesClient(self)
        self.snapshot = SnapshotClient(self)
        self.tasks = TasksClient(self)

        self.xpack = XPackClient(self)
        self.ccr = CcrClient(self)
        self.dangling_indices = DanglingIndicesClient(self)
        self.enrich = EnrichClient(self)
        self.eql = EqlClient(self)
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
            return f"<{self.__class__.__name__}({cons})>"
        except Exception:
            # probably operating on custom transport and connection_pool, ignore
            return super().__repr__()

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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/index.html>`_
        """
        client, params = _deprecated_options(self, params)
        try:
            await client._perform_request("HEAD", "/", params=params, headers=headers)
            return True
        except TransportError:
            return False

    @query_params()
    async def info(self, params=None, headers=None):
        """
        Returns basic information about the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/index.html>`_
        """
        client, params = _deprecated_options(self, params)
        return await client._perform_request("GET", "/", params=params, headers=headers)

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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-index_.html>`_

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
        client, params = _deprecated_options(self, params)
        for param in (index, id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_create", id)
        else:
            path = _make_path(index, doc_type, id, "_create")

        return await client._perform_request(
            "POST" if id in SKIP_IN_PATH else "PUT",
            path,
            params=params,
            headers=headers,
            body=body,
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
    async def index(self, index, body, id=None, params=None, headers=None):
        """
        Creates or updates a document in an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-index_.html>`_

        :arg index: The name of the index
        :arg body: The document
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
        client, params = _deprecated_options(self, params)
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await client._perform_request(
            "POST" if id in SKIP_IN_PATH else "PUT",
            _make_path(index, "_doc", id),
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-bulk.html>`_

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
        client, params = _deprecated_options(self, params)
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        headers["content-type"] = "application/x-ndjson"
        return await client._perform_request(
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/clear-scroll-api.html>`_

        :arg body: A comma-separated list of scroll IDs to clear if none
            was specified via the scroll_id parameter
        :arg scroll_id: A comma-separated list of scroll IDs to clear
        """
        client, params = _deprecated_options(self, params)
        if scroll_id in SKIP_IN_PATH and body in SKIP_IN_PATH:
            raise ValueError("You need to supply scroll_id or body.")
        elif scroll_id and not body:
            body = {"scroll_id": [scroll_id]}
        elif scroll_id:
            params["scroll_id"] = scroll_id

        return await client._perform_request(
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
    async def count(self, body=None, index=None, params=None, headers=None):
        """
        Returns number of documents matching a query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-count.html>`_

        :arg body: A query to restrict the results specified with the
            Query DSL (optional)
        :arg index: A comma-separated list of indices to restrict the
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
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
            "POST",
            _make_path(index, "_count"),
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-delete.html>`_

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
            internal, external, external_gte
        :arg wait_for_active_shards: Sets the number of shard copies
            that must be active before proceeding with the delete operation.
            Defaults to 1, meaning the primary shard only. Set to `all` for all
            shard copies, otherwise set to any non-negative value less than or equal
            to the total number of copies for the shard (number of replicas + 1)
        """
        client, params = _deprecated_options(self, params)
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            doc_type = "_doc"

        return await client._perform_request(
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
        "slices",
        "sort",
        "stats",
        "terminate_after",
        "timeout",
        "version",
        "wait_for_active_shards",
        "wait_for_completion",
    )
    async def delete_by_query(self, index, body, params=None, headers=None):
        """
        Deletes documents matching the provided query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-delete-by-query.html>`_

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg body: The search definition using the Query DSL
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
        :arg from\\_: Starting offset (default: 0)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such
            as providing text to a numeric field) should be ignored
        :arg max_docs: Maximum number of documents to process (default:
            all documents)
        :arg preference: Specify the node or shard the operation should
            be performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg refresh: Should the affected indexes be refreshed?
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
        client, params = _deprecated_options(self, params)
        if params and "from_" in params:
            params["from"] = params.pop("from_")

        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_delete_by_query"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("requests_per_second")
    async def delete_by_query_rethrottle(self, task_id, params=None, headers=None):
        """
        Changes the number of requests per second for a particular Delete By Query
        operation.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-delete-by-query.html>`_

        :arg task_id: The task id to rethrottle
        :arg requests_per_second: The throttle to set on this request in
            floating sub-requests per second. -1 means set no throttle.
        """
        client, params = _deprecated_options(self, params)
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'task_id'.")

        return await client._perform_request(
            "POST",
            _make_path("_delete_by_query", task_id, "_rethrottle"),
            params=params,
            headers=headers,
        )

    @query_params("master_timeout", "timeout")
    async def delete_script(self, id, params=None, headers=None):
        """
        Deletes a script.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-scripting.html>`_

        :arg id: Script ID
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        client, params = _deprecated_options(self, params)
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return await client._perform_request(
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
    async def exists(self, index, id, params=None, headers=None):
        """
        Returns information about whether a document exists in an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
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
            internal, external, external_gte
        """
        client, params = _deprecated_options(self, params)
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        try:
            await client._perform_request(
                "HEAD", _make_path(index, "_doc", id), params=params, headers=headers
            )
            return True
        except NotFoundError:
            return False

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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-get.html>`_

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
            internal, external, external_gte
        """
        client, params = _deprecated_options(self, params)
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        try:
            await client._perform_request(
                "HEAD",
                _make_path(index, doc_type, id, "_source"),
                params=params,
                headers=headers,
            )
            return True
        except NotFoundError:
            return False

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
    async def explain(self, index, id, body=None, params=None, headers=None):
        """
        Returns information about why a specific matches (or doesn't match) a query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-explain.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg body: The query definition using the Query DSL
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
        client, params = _deprecated_options(self, params)
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_explain", id),
            params=params,
            headers=headers,
            body=body,
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-field-caps.html>`_

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
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
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
    async def get(self, index, id, params=None, headers=None):
        """
        Returns a document.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
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
            internal, external, external_gte
        """
        client, params = _deprecated_options(self, params)
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await client._perform_request(
            "GET", _make_path(index, "_doc", id), params=params, headers=headers
        )

    @query_params("master_timeout")
    async def get_script(self, id, params=None, headers=None):
        """
        Returns a script.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-scripting.html>`_

        :arg id: Script ID
        :arg master_timeout: Specify timeout for connection to master
        """
        client, params = _deprecated_options(self, params)
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return await client._perform_request(
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
    async def get_source(self, index, id, params=None, headers=None):
        """
        Returns the source of a document.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
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
            internal, external, external_gte
        """
        client, params = _deprecated_options(self, params)
        for param in (index, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await client._perform_request(
            "GET", _make_path(index, "_source", id), params=params, headers=headers
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
    async def mget(self, body, index=None, params=None, headers=None):
        """
        Allows to get multiple documents in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-multi-get.html>`_

        :arg body: Document identifiers; can be either `docs`
            (containing full document information) or `ids` (when index is provided
            in the URL.
        :arg index: The name of the index
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
        client, params = _deprecated_options(self, params)
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_mget"),
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
    async def msearch(self, body, index=None, params=None, headers=None):
        """
        Allows to execute several search operations in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-multi-search.html>`_

        :arg body: The request definitions (metadata-search request
            definition pairs), separated by newlines
        :arg index: A comma-separated list of index names to use as
            default
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
            query_then_fetch, dfs_query_then_fetch
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        """
        client, params = _deprecated_options(self, params)
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        headers["content-type"] = "application/x-ndjson"
        return await client._perform_request(
            "POST",
            _make_path(index, "_msearch"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("master_timeout", "timeout")
    async def put_script(self, id, body, context=None, params=None, headers=None):
        """
        Creates or updates a script.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-scripting.html>`_

        :arg id: Script ID
        :arg body: The document
        :arg context: Context name to compile script against
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        client, params = _deprecated_options(self, params)
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await client._perform_request(
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-rank-eval.html>`_

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
        client, params = _deprecated_options(self, params)
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await client._perform_request(
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-reindex.html>`_

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
        client, params = _deprecated_options(self, params)
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await client._perform_request(
            "POST", "/_reindex", params=params, headers=headers, body=body
        )

    @query_params("requests_per_second")
    async def reindex_rethrottle(self, task_id, params=None, headers=None):
        """
        Changes the number of requests per second for a particular Reindex operation.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-reindex.html>`_

        :arg task_id: The task id to rethrottle
        :arg requests_per_second: The throttle to set on this request in
            floating sub-requests per second. -1 means set no throttle.
        """
        client, params = _deprecated_options(self, params)
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'task_id'.")

        return await client._perform_request(
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/render-search-template-api.html>`_

        :arg body: The search definition template and its params
        :arg id: The id of the stored search template
        """
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
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
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-request-body.html#request-body-search-scroll>`_

        :arg body: The scroll ID if not passed by URL or query
            parameter.
        :arg scroll_id: The scroll ID for scrolled search
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg scroll: Specify how long a consistent view of the index
            should be maintained for scrolled search
        """
        client, params = _deprecated_options(self, params)
        if scroll_id in SKIP_IN_PATH and body in SKIP_IN_PATH:
            raise ValueError("You need to supply scroll_id or body.")
        elif scroll_id and not body:
            body = {"scroll_id": scroll_id}
        elif scroll_id:
            params["scroll_id"] = scroll_id

        return await client._perform_request(
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
    async def search(self, body=None, index=None, params=None, headers=None):
        """
        Returns results matching a query.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-search.html>`_

        :arg body: The search definition using the Query DSL
        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
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
        :arg from\\_: Starting offset (default: 0)
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
            match the query should be tracked. A number can also be specified, to
            accurately track the total hit count up to the number.
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        :arg version: Specify whether to return document version as part
            of a hit
        """
        client, params = _deprecated_options(self, params)
        if params and "from_" in params:
            params["from"] = params.pop("from_")

        return await client._perform_request(
            "POST",
            _make_path(index, "_search"),
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-shards.html>`_

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
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
            "GET", _make_path(index, "_search_shards"), params=params, headers=headers
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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-update.html>`_

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
        client, params = _deprecated_options(self, params)
        for param in (index, id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        if doc_type in SKIP_IN_PATH:
            path = _make_path(index, "_update", id)
        else:
            path = _make_path(index, doc_type, id, "_update")

        return await client._perform_request(
            "POST", path, params=params, headers=headers, body=body
        )

    @query_params("requests_per_second")
    async def update_by_query_rethrottle(self, task_id, params=None, headers=None):
        """
        Changes the number of requests per second for a particular Update By Query
        operation.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-update-by-query.html>`_

        :arg task_id: The task id to rethrottle
        :arg requests_per_second: The throttle to set on this request in
            floating sub-requests per second. -1 means set no throttle.
        """
        client, params = _deprecated_options(self, params)
        if task_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'task_id'.")

        return await client._perform_request(
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
        """
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
            "GET", "/_script_context", params=params, headers=headers
        )

    @query_params()
    async def get_script_languages(self, params=None, headers=None):
        """
        Returns available script types, languages and contexts

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/modules-scripting.html>`_
        """
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
            "GET", "/_script_language", params=params, headers=headers
        )

    @query_params(
        "ccs_minimize_roundtrips",
        "max_concurrent_searches",
        "rest_total_hits_as_int",
        "search_type",
        "typed_keys",
    )
    async def msearch_template(self, body, index=None, params=None, headers=None):
        """
        Allows to execute several search template operations in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-multi-search.html>`_

        :arg body: The request definitions (metadata-search request
            definition pairs), separated by newlines
        :arg index: A comma-separated list of index names to use as
            default
        :arg ccs_minimize_roundtrips: Indicates whether network round-
            trips should be minimized as part of cross-cluster search requests
            execution  Default: true
        :arg max_concurrent_searches: Controls the maximum number of
            concurrent searches the multi search api will execute
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg search_type: Search operation type  Valid choices:
            query_then_fetch, dfs_query_then_fetch
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        """
        client, params = _deprecated_options(self, params)
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        headers["content-type"] = "application/x-ndjson"
        return await client._perform_request(
            "POST",
            _make_path(index, "_msearch", "template"),
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
    async def mtermvectors(self, body=None, index=None, params=None, headers=None):
        """
        Returns multiple termvectors in one request.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-multi-termvectors.html>`_

        :arg body: Define ids, documents, parameters or a list of
            parameters per document here. You must at least provide a list of
            document ids. See documentation.
        :arg index: The index in which the document resides.
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
            internal, external, external_gte
        """
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
            "POST",
            _make_path(index, "_mtermvectors"),
            params=params,
            headers=headers,
            body=body,
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
    async def search_template(self, body, index=None, params=None, headers=None):
        """
        Allows to use the Mustache language to pre-render a search definition.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-template.html>`_

        :arg body: The search definition template and its params
        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
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
            query_then_fetch, dfs_query_then_fetch
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        """
        client, params = _deprecated_options(self, params)
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_search", "template"),
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
    async def termvectors(self, index, body=None, id=None, params=None, headers=None):
        """
        Returns information and statistics about terms in the fields of a particular
        document.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-termvectors.html>`_

        :arg index: The index in which the document resides.
        :arg body: Define parameters and or supply a document to get
            termvectors for. See documentation.
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
            internal, external, external_gte
        """
        client, params = _deprecated_options(self, params)
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_termvectors", id),
            params=params,
            headers=headers,
            body=body,
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
    async def update_by_query(self, index, body=None, params=None, headers=None):
        """
        Performs an update on every document in the index without changing the source,
        for example to pick up a mapping change.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/docs-update-by-query.html>`_

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg body: The search definition using the Query DSL
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
        :arg from\\_: Starting offset (default: 0)
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
        client, params = _deprecated_options(self, params)
        if params and "from_" in params:
            params["from"] = params.pop("from_")

        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_update_by_query"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def close_point_in_time(self, body=None, params=None, headers=None):
        """
        Close a point in time

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/point-in-time-api.html>`_

        :arg body: a point-in-time id to close
        """
        client, params = _deprecated_options(self, params)
        return await client._perform_request(
            "DELETE", "/_pit", params=params, headers=headers, body=body
        )

    @query_params(
        "expand_wildcards", "ignore_unavailable", "keep_alive", "preference", "routing"
    )
    async def open_point_in_time(self, index, params=None, headers=None):
        """
        Open a point in time that can be used in subsequent searches

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/point-in-time-api.html>`_

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
        client, params = _deprecated_options(self, params)
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await client._perform_request(
            "POST", _make_path(index, "_pit"), params=params, headers=headers
        )

    @query_params()
    async def terms_enum(self, index, body=None, params=None, headers=None):
        """
        The terms enum API  can be used to discover terms in the index that begin with
        the provided string. It is designed for low-latency look-ups used in auto-
        complete scenarios.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-terms-enum.html>`_

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg body: field name, string which is the prefix expected in
            matching terms, timeout and size for max number of results
        """
        client, params = _deprecated_options(self, params)
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_terms_enum"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "exact_bounds",
        "extent",
        "grid_precision",
        "grid_type",
        "size",
        "track_total_hits",
    )
    async def search_mvt(
        self, index, field, zoom, x, y, body=None, params=None, headers=None
    ):
        """
        Searches a vector tile for geospatial values. Returns results as a binary
        Mapbox vector tile.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-vector-tile-api.html>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg index: Comma-separated list of data streams, indices, or
            aliases to search
        :arg field: Field containing geospatial data to return
        :arg zoom: Zoom level for the vector tile to search
        :arg x: X coordinate for the vector tile to search
        :arg y: Y coordinate for the vector tile to search
        :arg body: Search request body.
        :arg exact_bounds: If false, the meta layer's feature is the
            bounding box of the tile. If true, the meta layer's feature is a
            bounding box resulting from a `geo_bounds` aggregation.
        :arg extent: Size, in pixels, of a side of the vector tile.
            Default: 4096
        :arg grid_precision: Additional zoom levels available through
            the aggs layer. Accepts 0-8.  Default: 8
        :arg grid_type: Determines the geometry type for features in the
            aggs layer.  Valid choices: grid, point, centroid  Default: grid
        :arg size: Maximum number of features to return in the hits
            layer. Accepts 0-10000.  Default: 10000
        :arg track_total_hits: Indicate if the number of documents that
            match the query should be tracked. A number can also be specified, to
            accurately track the total hit count up to the number.
        """
        client, params = _deprecated_options(self, params)
        for param in (index, field, zoom, x, y):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_mvt", field, zoom, x, y),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("routing")
    async def knn_search(self, index, body=None, params=None, headers=None):
        """
        Performs a kNN search.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/search-search.html>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg body: The search definition
        :arg routing: A comma-separated list of specific routing values
        """
        client, params = _deprecated_options(self, params)
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await client._perform_request(
            "POST",
            _make_path(index, "_knn_search"),
            params=params,
            headers=headers,
            body=body,
        )

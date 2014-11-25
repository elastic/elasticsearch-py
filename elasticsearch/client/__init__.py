from __future__ import unicode_literals
import weakref
import logging

from ..transport import Transport
from ..exceptions import NotFoundError, TransportError
from ..compat import string_types, urlparse
from .indices import IndicesClient
from .cluster import ClusterClient
from .cat import CatClient
from .nodes import NodesClient
from .snapshot import SnapshotClient
from .utils import query_params, _make_path

logger = logging.getLogger('elasticsearch')

def _normalize_hosts(hosts):
    """
    Helper function to transform hosts argument to
    :class:`~elasticsearch.Elasticsearch` to a list of dicts.
    """
    # if hosts are empty, just defer to defaults down the line
    if hosts is None:
        return [{}]

    # passed in just one string
    if isinstance(hosts, string_types):
        hosts = [hosts]

    out = []
    # normalize hosts to dicts
    for host in hosts:
        if isinstance(host, string_types):
            if '://' not in host:
                host = "//%s" % host

            parsed_url = urlparse(host)
            h = {"host": parsed_url.hostname}

            if parsed_url.port:
                h["port"] = parsed_url.port

            if parsed_url.scheme == "https":
                h['port'] = parsed_url.port or 443
                h['use_ssl'] = True
                h['scheme'] = 'http'
            elif parsed_url.scheme:
                h['scheme'] = parsed_url.scheme

            if parsed_url.username or parsed_url.password:
                h['http_auth'] = '%s:%s' % (parsed_url.username, parsed_url.password)

            if parsed_url.path and parsed_url.path != '/':
                h['url_prefix'] = parsed_url.path

            out.append(h)
        else:
            out.append(host)
    return out


class Elasticsearch(object):
    """
    Elasticsearch low-level client. Provides a straightforward mapping from
    Python to ES REST endpoints.

    The instance has attributes `cat`, `cluster`, `indices`, `nodes` and
    `snapshot` that provide access to instances of
    :class:`~elasticsearch.client.CatClient`,
    :class:`~elasticsearch.client.ClusterClient`,
    :class:`~elasticsearch.client.IndicesClient`,
    :class:`~elasticsearch.client.NodesClient` and
    :class:`~elasticsearch.client.SnapshotClient` respectively. This is the
    preferred (and only supported) way to get access to those classes and their
    methods.

    You can speify your own connection class which should be used by providing
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
        # and an url_prefix
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
            # make sure we verify SSL certificates (off by default)
            verify_certs=True,
            # provide a path to CA certs on disk
            ca_certs='/path/to/CA_certs'
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

    """
    def __init__(self, hosts=None, transport_class=Transport, **kwargs):
        """
        :arg hosts: list of nodes we should connect to. Node should be a
            dictionary ({"host": "localhost", "port": 9200}), the entire dictionary
            will be passed to the :class:`~elasticsearch.Connection` class as
            kwargs, or a string in the format of ``host[:port]`` which will be
            translated to a dictionary automatically.  If no value is given the
            :class:`~elasticsearch.Urllib3HttpConnection` class defaults will be used.

        :arg transport_class: :class:`~elasticsearch.Transport` subclass to use.

        :arg kwargs: any additional arguments will be passed on to the
            :class:`~elasticsearch.Transport` class and, subsequently, to the
            :class:`~elasticsearch.Connection` instances.
        """
        self.transport = transport_class(_normalize_hosts(hosts), **kwargs)

        # namespaced clients for compatibility with API names
        # use weakref to make GC's work a little easier
        self.indices = IndicesClient(weakref.proxy(self))
        self.cluster = ClusterClient(weakref.proxy(self))
        self.cat = CatClient(weakref.proxy(self))
        self.nodes = NodesClient(weakref.proxy(self))
        self.snapshot = SnapshotClient(weakref.proxy(self))

    def __repr__(self):
        try:
            # get a lost of all connections
            cons = self.transport.hosts
            # truncate to 10 if there are too many
            if len(cons) > 5:
                cons = cons[:5] + ['...']
            return '<Elasticsearch(%r)>' % cons
        except:
            # probably operating on custom transport and connection_pool, ignore
            return super(Elasticsearch, self).__repr__()

    def _bulk_body(self, body):
        # if not passed in a string, serialize items and join by newline
        if not isinstance(body, string_types):
            body = '\n'.join(map(self.transport.serializer.dumps, body))

        # bulk body must end with a newline
        if not body.endswith('\n'):
            body += '\n'

        return body

    @query_params()
    def ping(self, params=None):
        """
        Returns True if the cluster is up, False otherwise.
        """
        try:
            self.transport.perform_request('HEAD', '/', params=params)
        except TransportError:
            return False
        return True

    @query_params()
    def info(self, params=None):
        """
        Get the basic info from the current cluster.
        """
        _, data = self.transport.perform_request('GET', '/', params=params)
        return data

    @query_params('consistency', 'parent', 'percolate', 'refresh',
        'replication', 'routing', 'timeout', 'timestamp', 'ttl', 'version', 'version_type')
    def create(self, index, doc_type, body, id=None, params=None):
        """
        Adds a typed JSON document in a specific index, making it searchable.
        Behind the scenes this method calls index(..., op_type='create')
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-index_.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: Document ID
        :arg body: The document
        :arg consistency: Explicit write consistency setting for the operation
        :arg id: Specific document ID (when the POST method is used)
        :arg parent: ID of the parent document
        :arg percolate: Percolator queries to execute while indexing the document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        return self.index(index, doc_type, body, id=id, params=params, op_type='create')

    @query_params('consistency', 'op_type', 'parent', 'refresh',
        'replication', 'routing', 'timeout', 'timestamp', 'ttl', 'version', 'version_type')
    def index(self, index, doc_type, body, id=None, params=None):
        """
        Adds or updates a typed JSON document in a specific index, making it searchable.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-index_.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg body: The document
        :arg id: Document ID
        :arg consistency: Explicit write consistency setting for the operation
        :arg op_type: Explicit operation type (default: index)
        :arg parent: ID of the parent document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        _, data = self.transport.perform_request('PUT' if id else 'POST',
            _make_path(index, doc_type, id), params=params, body=body)
        return data

    @query_params('parent', 'preference', 'realtime', 'refresh', 'routing')
    def exists(self, index, id, doc_type='_all', params=None):
        """
        Returns a boolean indicating whether or not given document exists in Elasticsearch.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document (uses `_all` by default to
            fetch the first document matching the ID across all types)
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or
            search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        """
        try:
            self.transport.perform_request('HEAD', _make_path(index, doc_type, id), params=params)
        except NotFoundError:
            return False
        return True

    @query_params('_source', '_source_exclude', '_source_include', 'fields',
        'parent', 'preference', 'realtime', 'refresh', 'routing', 'version', 'version_type')
    def get(self, index, id, doc_type='_all', params=None):
        """
        Get a typed JSON document from the index based on its id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg id: The document ID
        :arg doc_type: The type of the document (uses `_all` by default to
            fetch the first document matching the ID across all types)
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg fields: A comma-separated list of fields to return in the response
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or
            search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg version: Explicit version number for concurrency control
        :arg version_type: Explicit version number for concurrency control

        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, id),
            params=params)
        return data

    @query_params('_source', '_source_exclude', '_source_include', 'parent', 'preference',
        'realtime', 'refresh', 'routing', 'version', 'version_type')
    def get_source(self, index, id, doc_type='_all', params=None):
        """
        Get the source of a document by it's index, type and id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document (uses `_all` by default to
            fetch the first document matching the ID across all types)
        :arg id: The document ID
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg version: Explicit version number for concurrency control
        :arg version_type: Explicit version number for concurrency control
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, id, '_source'),
            params=params)
        return data

    @query_params('_source', '_source_exclude', '_source_include', 'fields',
        'parent', 'preference', 'realtime', 'refresh', 'routing')
    def mget(self, body, index=None, doc_type=None, params=None):
        """
        Get multiple documents based on an index, type (optional) and ids.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-multi-get.html>`_

        :arg body: Document identifiers; can be either `docs` (containing full
            document information) or `ids` (when index and type is provided in the URL.
        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg fields: A comma-separated list of fields to return in the response
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_mget'),
            params=params, body=body)
        return data

    @query_params('consistency', 'fields', 'lang', 'parent', 'refresh',
        'replication', 'retry_on_conflict', 'routing', 'script', 'timeout',
        'timestamp', 'ttl', 'version', 'version_type')
    def update(self, index, doc_type, id, body=None, params=None):
        """
        Update a document based on a script or partial data provided.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-update.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: Document ID
        :arg body: The request definition using either `script` or partial `doc`
        :arg consistency: Explicit write consistency setting for the operation
        :arg fields: A comma-separated list of fields to return in the response
        :arg lang: The script language (default: mvel)
        :arg parent: ID of the parent document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg retry_on_conflict: Specify how many times should the operation be
            retried when a conflict occurs (default: 0)
        :arg routing: Specific routing value
        :arg script: The URL-encoded script definition (instead of using request body)
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Explicit version number for concurrency control
        """
        _, data = self.transport.perform_request('POST', _make_path(index, doc_type, id, '_update'),
            params=params, body=body)
        return data

    @query_params('_source', '_source_exclude', '_source_include',
        'analyze_wildcard', 'analyzer', 'default_operator', 'df',
        'explain', 'fields', 'indices_boost', 'lenient',
        'allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'lowercase_expanded_terms', 'from_', 'preference', 'q', 'routing',
        'scroll', 'search_type', 'size', 'sort', 'source', 'stats',
        'suggest_field', 'suggest_mode', 'suggest_size', 'suggest_text', 'timeout',
        'version')
    def search(self, index=None, doc_type=None, body=None, params=None):
        """
        Execute a search query and get back search hits that match the query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_

        :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search;
            leave empty to perform the operation on all types
        :arg body: The search definition using the Query DSL
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg analyze_wildcard: Specify whether wildcard and prefix queries
            should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string query (AND
            or OR) (default: OR)
        :arg df: The field to use as default where no field prefix is given in
            the query string
        :arg explain: Specify whether to return detailed information about
            score computation as part of a hit
        :arg fields: A comma-separated list of fields to return as part of a hit
        :arg indices_boost: Comma-separated list of index boosts
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg lowercase_expanded_terms: Specify whether query terms should be lowercased
        :arg from\_: Starting offset (default: 0)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg search_type: Search operation type
        :arg size: Number of hits to return (default: 10)
        :arg sort: A comma-separated list of <field>:<direction> pairs
        :arg source: The URL-encoded request definition using the Query DSL
            (instead of using request body)
        :arg stats: Specific 'tag' of the request for logging and statistical purposes
        :arg suggest_field: Specify which field to use for suggestions
        :arg suggest_mode: Specify suggest mode (default: missing)
        :arg suggest_size: How many suggestions to return in response
        :arg suggest_text: The source text for which the suggestions should be returned
        :arg timeout: Explicit operation timeout
        :arg version: Specify whether to return document version as part of a hit
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if 'from_' in params:
            params['from'] = params.pop('from_')

        if doc_type and not index:
            index = '_all'
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_search'),
            params=params, body=body)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'local', 'preference', 'routing')
    def search_shards(self, index=None, doc_type=None, params=None):
        """
        The search shards api returns the indices and shards that a search
        request would be executed against. This can give useful feedback for working
        out issues or planning optimizations with routing and shard preferences.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-shards.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both. (default: '"open"')
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: Specific routing value
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_search_shards'), params=params)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'preference', 'routing', 'scroll', 'search_type')
    def search_template(self, index=None, doc_type=None, body=None, params=None):
        """
        A query that accepts a query template and a map of key/value pairs to
        fill in template parameters.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/query-dsl-template-query.html>`_

        :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search; leave
            empty to perform the operation on all types
        :arg body: The search definition template and its params
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg search_type: Search operation type
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_search', 'template'), params=params, body=body)
        return data

    @query_params('_source', '_source_exclude', '_source_include',
        'analyze_wildcard', 'analyzer', 'default_operator', 'df', 'fields',
        'lenient', 'lowercase_expanded_terms', 'parent', 'preference', 'q',
        'routing', 'source')
    def explain(self, index, doc_type, id, body=None, params=None):
        """
        The explain api computes a score explanation for a query and a specific
        document. This can give useful feedback whether a document matches or
        didn't match a specific query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-explain.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: The document ID
        :arg body: The query definition using the Query DSL
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg analyze_wildcard: Specify whether wildcards and prefix queries in
            the query string query should be analyzed (default: false)
        :arg analyzer: The analyzer for the query string query
        :arg default_operator: The default operator for query string query (AND
            or OR), (default: OR)
        :arg df: The default field for query string query (default: _all)
        :arg fields: A comma-separated list of fields to return in the response
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg lowercase_expanded_terms: Specify whether query terms should be lowercased
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        :arg source: The URL-encoded query definition (instead of using the
            request body)
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, id, '_explain'),
            params=params, body=body)
        return data

    @query_params('scroll')
    def scroll(self, scroll_id, params=None):
        """
        Scroll a search request created by specifying the scroll parameter.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_

        :arg scroll_id: The scroll ID
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        """
        _, data = self.transport.perform_request('GET', '/_search/scroll',
            params=params, body=scroll_id)
        return data

    @query_params()
    def clear_scroll(self, scroll_id=None, body=None, params=None):
        """
        Clear the scroll request created by specifying the scroll parameter to
        search.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_

        :arg scroll_id: The scroll ID or a list of scroll IDs
        :arg body: A comma-separated list of scroll IDs to clear if none was
            specified via the scroll_id parameter
        """
        _, data = self.transport.perform_request('DELETE', _make_path('_search', 'scroll', scroll_id),
            body=body, params=params)
        return data


    @query_params('consistency', 'parent', 'refresh', 'replication', 'routing',
        'timeout', 'version', 'version_type')
    def delete(self, index, doc_type, id, params=None):
        """
        Delete a typed JSON document from a specific index based on its id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: The document ID
        :arg consistency: Specific write consistency setting for the operation
        :arg parent: ID of parent document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type (default: sync)
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        _, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, id), params=params)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'min_score', 'preference', 'q', 'routing', 'source')
    def count(self, index=None, doc_type=None, body=None, params=None):
        """
        Execute a query and get the number of matches for that query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-count.html>`_

        :arg index: A comma-separated list of indices to restrict the results
        :arg doc_type: A comma-separated list of types to restrict the results
        :arg body: A query to restrict the results (optional)
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg min_score: Include only documents with a specific `_score` value in the result
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        :arg source: The URL-encoded query definition (instead of using the request body)
        """
        _, data = self.transport.perform_request('POST', _make_path(index, doc_type, '_count'),
            params=params, body=body)
        return data

    @query_params('consistency', 'refresh', 'routing', 'replication', 'timeout')
    def bulk(self, body, index=None, doc_type=None, params=None):
        """
        Perform many index/delete operations in a single API call.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-bulk.html>`_

        See the :func:`~elasticsearch.helpers.bulk` helper function for a more
        friendly API.

        :arg body: The operation definition and data (action-data pairs), as
            either a newline separated string, or a sequence of dicts to
            serialize (one per row).
        :arg index: Default index for items which don't provide one
        :arg doc_type: Default document type for items which don't provide one
        :arg consistency: Explicit write consistency setting for the operation
        :arg refresh: Refresh the index after performing the operation
        :arg routing: Specific routing value
        :arg replication: Explicitly set the replication type (default: sync)
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('POST', _make_path(index, doc_type, '_bulk'),
            params=params, body=self._bulk_body(body))
        return data

    @query_params('search_type')
    def msearch(self, body, index=None, doc_type=None, params=None):
        """
        Execute several search requests within the same API.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-multi-search.html>`_

        :arg body: The request definitions (metadata-search request definition
            pairs), as either a newline separated string, or a sequence of
            dicts to serialize (one per row).
        :arg index: A comma-separated list of index names to use as default
        :arg doc_type: A comma-separated list of document types to use as default
        :arg search_type: Search operation type
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_msearch'),
            params=params, body=self._bulk_body(body))
        return data

    @query_params('allow_no_indices', 'analyzer', 'consistency',
        'default_operator', 'df', 'expand_wildcards', 'ignore_unavailable', 'q',
        'replication', 'routing', 'source', 'timeout')
    def delete_by_query(self, index, doc_type=None, body=None, params=None):
        """
        Delete documents from one or more indices and one or more types based on a query.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-delete-by-query.html>`_

        :arg index: A comma-separated list of indices to restrict the operation;
            use `_all` to perform the operation on all indices
        :arg doc_type: A comma-separated list of types to restrict the operation
        :arg body: A query to restrict the operation specified with the Query
            DSL
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyzer: The analyzer to use for the query string
        :arg consistency: Specific write consistency setting for the operation
        :arg default_operator: The default operator for query string query (AND
            or OR), default u'OR'
        :arg df: The field to use as default where no field prefix is given in
            the query string
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default u'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg q: Query in the Lucene query string syntax
        :arg replication: Specific replication type, default u'sync'
        :arg routing: Specific routing value
        :arg source: The URL-encoded query definition (instead of using the
            request body)
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, '_query'),
            params=params, body=body)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'preference', 'routing', 'source')
    def suggest(self, body, index=None, params=None):
        """
        The suggest feature suggests similar looking terms based on a provided
        text by using a suggester.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-search.html>`_

        :arg index: A comma-separated list of index names to restrict the operation;
            use `_all` or empty string to perform the operation on all indices
        :arg body: The request definition
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: Specific routing value
        :arg source: The URL-encoded request definition (instead of using request body)
        """
        _, data = self.transport.perform_request('POST', _make_path(index, '_suggest'),
            params=params, body=body)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'percolate_format', 'percolate_index', 'percolate_type', 'preference',
        'routing', 'version', 'version_type')
    def percolate(self, index, doc_type, id=None, body=None, params=None):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_

        :arg index: The index of the document being percolated.
        :arg doc_type: The type of the document being percolated.
        :arg id: Substitute the document in the request body with a document
            that is known by the specified id. On top of the id, the index and
            type parameter will be used to retrieve the document from within the
            cluster.
        :arg body: The percolator request definition using the percolate DSL
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg percolate_format: Return an array of matching query IDs instead of
            objects
        :arg percolate_index: The index to percolate the document into. Defaults
            to index.
        :arg percolate_type: The type to percolate document into. Defaults to
            type.
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_percolate'), params=params, body=body)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable')
    def mpercolate(self, body, index=None, doc_type=None, params=None):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_

        :arg index: The index of the document being count percolated to use as
            default
        :arg doc_type: The type of the document being percolated to use as
            default.
        :arg body: The percolate request definitions (header & body pair),
            separated by newlines
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_mpercolate'), params=params, body=self._bulk_body(body))
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'percolate_index', 'percolate_type', 'preference', 'routing', 'version',
        'version_type')
    def count_percolate(self, index, doc_type, id=None, body=None, params=None):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-percolate.html>`_

        :arg index: The index of the document being count percolated.
        :arg doc_type: The type of the document being count percolated.
        :arg id: Substitute the document in the request body with a document
            that is known by the specified id. On top of the id, the index and
            type parameter will be used to retrieve the document from within the
            cluster.
        :arg body: The count percolator request definition using the percolate
            DSL
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg percolate_index: The index to count percolate the document into.
            Defaults to index.
        :arg percolate_type: The type to count percolate document into. Defaults
            to type.
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_percolate', 'count'), params=params, body=body)
        return data

    @query_params('boost_terms', 'include', 'max_doc_freq', 'max_query_terms',
        'max_word_length', 'min_doc_freq', 'min_term_freq', 'min_word_length',
        'mlt_fields', 'percent_terms_to_match', 'routing', 'search_from',
        'search_indices', 'search_query_hint', 'search_scroll', 'search_size',
        'search_source', 'search_type', 'search_types', 'stop_words')
    def mlt(self, index, doc_type, id, body=None, params=None):
        """
        Get documents that are "like" a specified document.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-more-like-this.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document (use `_all` to fetch the first
            document matching the ID across all types)
        :arg id: The document ID
        :arg body: A specific search request definition
        :arg boost_terms: The boost factor
        :arg include: Whether to include the queried document from the response
        :arg max_doc_freq: The word occurrence frequency as count: words with
            higher occurrence in the corpus will be ignored
        :arg max_query_terms: The maximum query terms to be included in the generated query
        :arg max_word_length: The minimum length of the word: longer words will be ignored
        :arg min_doc_freq: The word occurrence frequency as count: words with
            lower occurrence in the corpus will be ignored
        :arg min_term_freq: The term frequency as percent: terms with lower
            occurence in the source document will be ignored
        :arg min_word_length: The minimum length of the word: shorter words will be ignored
        :arg mlt_fields: Specific fields to perform the query against
        :arg percent_terms_to_match: How many terms have to match in order to
            consider the document a match (default: 0.3)
        :arg routing: Specific routing value
        :arg search_from: The offset from which to return results
        :arg search_indices: A comma-separated list of indices to perform the
            query against (default: the index containing the document)
        :arg search_query_hint: The search query hint
        :arg search_scroll: A scroll search request definition
        :arg search_size: The number of documents to return (default: 10)
        :arg search_source: A specific search request definition (instead of
            using the request body)
        :arg search_type: Specific search type (eg. `dfs_then_fetch`, `count`, etc)
        :arg search_types: A comma-separated list of types to perform the query
            against (default: the same type as the document)
        :arg stop_words: A list of stop words to be ignored
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, id, '_mlt'),
            params=params, body=body)
        return data

    @query_params('field_statistics', 'fields', 'offsets', 'parent', 'payloads',
        'positions', 'preference', 'realtime', 'routing', 'term_statistics')
    def termvectors(self, index, doc_type, id, body=None, params=None):
        """
        Returns information and statistics on terms in the fields of a
        particular document. The document could be stored in the index or
        artificially provided by the user (Added in 1.4). Note that for
        documents stored in the index, this is a near realtime API as the term
        vectors are not available until the next refresh.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-termvectors.html>`

        :arg index: The index in which the document resides.
        :arg doc_type: The type of the document.
        :arg id: The id of the document.
        :arg body: Define parameters. See documentation.
        :arg field_statistics: Specifies if document count, sum of document
            frequencies and sum of total term frequencies should be returned.,
            default True
        :arg fields: A comma-separated list of fields to return.
        :arg offsets: Specifies if term offsets should be returned., default
            True
        :arg parent: Parent id of documents.
        :arg payloads: Specifies if term payloads should be returned., default
            True
        :arg positions: Specifies if term positions should be returned., default
            True
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random).
        :arg realtime: Specifies if request is real-time as opposed to near-
            real-time (default: true).
        :arg routing: Specific routing value.
        :arg term_statistics: Specifies if total term frequency and document
            frequency should be returned., default False
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_termvector'), params=params, body=body)
        return data

    # backwards compatibility
    termvector = termvectors

    @query_params('field_statistics', 'fields', 'ids', 'offsets', 'parent',
        'payloads', 'positions', 'preference', 'routing', 'term_statistics')
    def mtermvectors(self, index=None, doc_type=None, body=None, params=None):
        """
        Multi termvectors API allows to get multiple termvectors based on an
        index, type and id.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/docs-multi-termvectors.html>`_

        :arg index: The index in which the document resides.
        :arg doc_type: The type of the document.
        :arg body: Define ids, parameters or a list of parameters per document
            here. You must at least provide a list of document ids. See
            documentation.
        :arg field_statistics: Specifies if document count, sum of document
            frequencies and sum of total term frequencies should be returned.
            Applies to all returned documents unless otherwise specified in body
            "params" or "docs"., default True
        :arg fields: A comma-separated list of fields to return. Applies to all
            returned documents unless otherwise specified in body "params" or
            "docs".
        :arg ids: A comma-separated list of documents ids. You must define ids
            as parameter or set "ids" or "docs" in the request body
        :arg offsets: Specifies if term offsets should be returned. Applies to
            all returned documents unless otherwise specified in body "params"
            or "docs"., default True
        :arg parent: Parent id of documents. Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg payloads: Specifies if term payloads should be returned. Applies to
            all returned documents unless otherwise specified in body "params"
            or "docs"., default True
        :arg positions: Specifies if term positions should be returned. Applies
            to all returned documents unless otherwise specified in body
            "params" or "docs"., default True
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random) .Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg routing: Specific routing value. Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg term_statistics: Specifies if total term frequency and document
            frequency should be returned. Applies to all returned documents
            unless otherwise specified in body "params" or "docs"., default
            False
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_mtermvectors'), params=params, body=body)
        return data

    @query_params('verbose')
    def benchmark(self, index=None, doc_type=None, body=None, params=None):
        """
        The benchmark API provides a standard mechanism for submitting queries
        and measuring their performance relative to one another.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg doc_type: The name of the document type
        :arg body: The search definition using the Query DSL
        :arg verbose: Specify whether to return verbose statistics about each
            iteration (default: false)
        """
        _, data = self.transport.perform_request('PUT', _make_path(index,
            doc_type, '_bench'), params=params, body=body)
        return data

    @query_params()
    def abort_benchmark(self, name=None, params=None):
        """
        Aborts a running benchmark.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_

        :arg name: A benchmark name
        """
        _, data = self.transport.perform_request('POST', _make_path('_bench',
            'abort', name), params=params)
        return data

    @query_params()
    def list_benchmarks(self, index=None, doc_type=None, params=None):
        """
        View the progress of long-running benchmarks.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/search-benchmark.html>`_

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg doc_type: The name of the document type
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_bench'), params=params)
        return data

    @query_params('op_type', 'version', 'version_type')
    def put_script(self, lang, id, body, params=None):
        """
        Create a script in given language with specified ID.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg body: The document
        :arg op_type: Explicit operation type, default u'index'
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        _, data = self.transport.perform_request('PUT', _make_path('_scripts',
            lang, id), params=params, body=body)
        return data

    @query_params('version', 'version_type')
    def get_script(self, lang, id, params=None):
        """
        Retrieve a script from the API.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        _, data = self.transport.perform_request('GET', _make_path('_scripts',
            lang, id), params=params)
        return data

    @query_params('version', 'version_type')
    def delete_script(self, lang, id, params=None):
        """
        Remove a stored script from elasticsearch.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        _, data = self.transport.perform_request('DELETE',
            _make_path('_scripts', lang, id), params=params)
        return data

    @query_params()
    def put_template(self, id, body, params=None):
        """
        Create a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg body: The document
        """
        _, data = self.transport.perform_request('PUT', _make_path('_search',
            'template', id), params=params, body=body)
        return data

    @query_params()
    def get_template(self, id, body=None, params=None):
        """
        Retrieve a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg body: The document
        """
        _, data = self.transport.perform_request('GET', _make_path('_search',
            'template', id), params=params, body=body)
        return data

    @query_params()
    def delete_template(self, id=None, params=None):
        """
        Delete a search template.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        """
        _, data = self.transport.perform_request('DELETE', _make_path('_search',
            'template', id), params=params)
        return data


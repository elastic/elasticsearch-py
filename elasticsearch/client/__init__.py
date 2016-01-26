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
from .utils import query_params, _make_path, SKIP_IN_PATH

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

    The instance has attributes ``cat``, ``cluster``, ``indices``, ``nodes``
    and ``snapshot`` that provide access to instances of
    :class:`~elasticsearch.client.CatClient`,
    :class:`~elasticsearch.client.ClusterClient`,
    :class:`~elasticsearch.client.IndicesClient`,
    :class:`~elasticsearch.client.NodesClient` and
    :class:`~elasticsearch.client.SnapshotClient` respectively. This is the
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
            # make sure we verify SSL certificates (off by default)
            verify_certs=True,
            # provide a path to CA certs on disk
            ca_certs='/path/to/CA_certs'
        )

    SSL client authentication is supported
    (see :class:`~elasticsearch.Urllib3HttpConnection` for
    detailed description of the options)::

        es = Elasticsearch(
            ['localhost:443', 'other_host:443'],
            # turn on SSL
            use_ssl=True,
            # make sure we verify SSL certificates (off by default)
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
        `<http://www.elastic.co/guide/>`_
        """
        try:
            self.transport.perform_request('HEAD', '/', params=params)
        except NotFoundError:
            return False
        return True

    @query_params()
    def info(self, params=None):
        """
        Get the basic info from the current cluster.
        `<http://www.elastic.co/guide/>`_
        """
        _, data = self.transport.perform_request('GET', '/', params=params)
        return data

    @query_params('consistency', 'parent', 'refresh', 'routing',
        'timeout', 'timestamp', 'ttl', 'version', 'version_type')
    def create(self, index, doc_type, body, id=None, params=None):
        """
        Adds a typed JSON document in a specific index, making it searchable.
        Behind the scenes this method calls index(..., op_type='create')
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg body: The document
        :arg id: Document ID
        :arg consistency: Explicit write consistency setting for the operation,
            valid choices are: 'one', 'quorum', 'all'
        :arg op_type: Explicit operation type, default 'index', valid choices
            are: 'index', 'create'
        :arg parent: ID of the parent document
        :arg refresh: Refresh the index after performing the operation
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        return self.index(index, doc_type, body, id=id, params=params, op_type='create')

    @query_params('consistency', 'op_type', 'parent', 'refresh', 'routing',
        'timeout', 'timestamp', 'ttl', 'version', 'version_type')
    def index(self, index, doc_type, body, id=None, params=None):
        """
        Adds or updates a typed JSON document in a specific index, making it searchable.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg body: The document
        :arg id: Document ID
        :arg consistency: Explicit write consistency setting for the operation,
            valid choices are: 'one', 'quorum', 'all'
        :arg op_type: Explicit operation type, default 'index', valid choices
            are: 'index', 'create'
        :arg parent: ID of the parent document
        :arg refresh: Refresh the index after performing the operation
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (index, doc_type, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('POST' if id in SKIP_IN_PATH else 'PUT',
            _make_path(index, doc_type, id), params=params, body=body)
        return data

    @query_params('parent', 'preference', 'realtime', 'refresh', 'routing')
    def exists(self, index, doc_type, id, params=None):
        """
        Returns a boolean indicating whether or not given document exists in Elasticsearch.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document (use `_all` to fetch the first
            document matching the ID across all types)
        :arg id: The document ID
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or
            search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        """
        for param in (index, doc_type, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        try:
            self.transport.perform_request('HEAD', _make_path(index, doc_type,
                id), params=params)
        except NotFoundError:
            return False
        return True

    @query_params('_source', '_source_exclude', '_source_include', 'fields',
        'parent', 'preference', 'realtime', 'refresh', 'routing', 'version',
        'version_type')
    def get(self, index, id, doc_type='_all', params=None):
        """
        Get a typed JSON document from the index based on its id.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document (use `_all` to fetch the first
            document matching the ID across all types)
        :arg id: The document ID
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
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (index, doc_type, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id), params=params)
        return data

    @query_params('_source', '_source_exclude', '_source_include', 'parent',
        'preference', 'realtime', 'refresh', 'routing', 'version',
        'version_type')
    def get_source(self, index, doc_type, id, params=None):
        """
        Get the source of a document by it's index, type and id.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document; use `_all` to fetch the first
            document matching the ID across all types
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
        :arg realtime: Specify whether to perform the operation in realtime or
            search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        :arg routing: Specific routing value
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (index, doc_type, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_source'), params=params)
        return data

    @query_params('_source', '_source_exclude', '_source_include', 'fields',
        'preference', 'realtime', 'refresh')
    def mget(self, body, index=None, doc_type=None, params=None):
        """
        Get multiple documents based on an index, type (optional) and ids.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-multi-get.html>`_

        :arg body: Document identifiers; can be either `docs` (containing full
            document information) or `ids` (when index and type is provided in
            the URL.
        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg fields: A comma-separated list of fields to return in the response
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or
            search mode
        :arg refresh: Refresh the shard containing the document before
            performing the operation
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_mget'), params=params, body=body)
        return data

    @query_params('consistency', 'detect_noop', 'fields', 'lang', 'parent',
        'refresh', 'retry_on_conflict', 'routing', 'script', 'script_id',
        'scripted_upsert', 'timeout', 'timestamp', 'ttl', 'version',
        'version_type')
    def update(self, index, doc_type, id, body=None, params=None):
        """
        Update a document based on a script or partial data provided.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: Document ID
        :arg body: The request definition using either `script` or partial `doc`
        :arg consistency: Explicit write consistency setting for the operation,
            valid choices are: 'one', 'quorum', 'all'
        :arg detect_noop: Specifying as true will cause Elasticsearch to check
            if there are changes and, if there aren't, turn the update request
            into a noop.
        :arg fields: A comma-separated list of fields to return in the response
        :arg lang: The script language (default: groovy)
        :arg parent: ID of the parent document. Is is only used for routing and
            when for the upsert request
        :arg refresh: Refresh the index after performing the operation
        :arg retry_on_conflict: Specify how many times should the operation be
            retried when a conflict occurs (default: 0)
        :arg routing: Specific routing value
        :arg script: The URL-encoded script definition (instead of using request
            body)
        :arg script_id: The id of a stored script
        :arg scripted_upsert: True if the script referenced in script or
            script_id should be called to perform inserts - defaults to false
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'force'
        """
        for param in (index, doc_type, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('POST', _make_path(index,
            doc_type, id, '_update'), params=params, body=body)
        return data

    @query_params('_source', '_source_exclude', '_source_include',
        'allow_no_indices', 'analyze_wildcard', 'analyzer', 'default_operator',
        'df', 'expand_wildcards', 'explain', 'fielddata_fields', 'fields',
        'from_', 'ignore_unavailable', 'lenient', 'lowercase_expanded_terms',
        'preference', 'q', 'request_cache', 'routing', 'scroll', 'search_type',
        'size', 'sort', 'stats', 'suggest_field', 'suggest_mode',
        'suggest_size', 'suggest_text', 'terminate_after', 'timeout',
        'track_scores', 'version')
    def search(self, index=None, doc_type=None, body=None, params=None):
        """
        Execute a search query and get back search hits that match the query.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html>`_

        :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search; leave
            empty to perform the operation on all types
        :arg body: The search definition using the Query DSL
        :arg _source: True or false to return the _source field or not, or a
            list of fields to return
        :arg _source_exclude: A list of fields to exclude from the returned
            _source field
        :arg _source_include: A list of fields to extract and return from the
            _source field
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyze_wildcard: Specify whether wildcard and prefix queries
            should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string query (AND
            or OR), default 'OR', valid choices are: 'AND', 'OR'
        :arg df: The field to use as default where no field prefix is given in
            the query string
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg explain: Specify whether to return detailed information about score
            computation as part of a hit
        :arg fielddata_fields: A comma-separated list of fields to return as the
            field data representation of a field for each hit
        :arg fields: A comma-separated list of fields to return as part of a hit
        :arg from\_: Starting offset (default: 0)
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg lowercase_expanded_terms: Specify whether query terms should be
            lowercased
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg request_cache: Specify if request cache should be used for this
            request or not, defaults to index level setting
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg search_type: Search operation type, valid choices are:
            'query_then_fetch', 'dfs_query_then_fetch', 'count', 'scan'
        :arg size: Number of hits to return (default: 10)
        :arg sort: A comma-separated list of <field>:<direction> pairs
        :arg stats: Specific 'tag' of the request for logging and statistical
            purposes
        :arg suggest_field: Specify which field to use for suggestions
        :arg suggest_mode: Specify suggest mode, default 'missing', valid
            choices are: 'missing', 'popular', 'always'
        :arg suggest_size: How many suggestions to return in response
        :arg suggest_text: The source text for which the suggestions should be
            returned
        :arg terminate_after: The maximum number of documents to collect for
            each shard, upon reaching which the query execution will terminate
            early.
        :arg timeout: Explicit operation timeout
        :arg track_scores: Whether to calculate and return scores even if they
            are not used for sorting
        :arg version: Specify whether to return document version as part of a
            hit
        """
        # from is a reserved word so it cannot be used, use from_ instead
        if 'from_' in params:
            params['from'] = params.pop('from_')

        if doc_type and not index:
            index = '_all'
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_search'), params=params, body=body)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'local', 'preference', 'routing')
    def search_shards(self, index=None, doc_type=None, params=None):
        """
        The search shards api returns the indices and shards that a search
        request would be executed against. This can give useful feedback for working
        out issues or planning optimizations with routing and shard preferences.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-shards.html>`_

        :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search; leave
            empty to perform the operation on all types
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
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
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg index: A comma-separated list of index names to search; use `_all`
            or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search; leave
            empty to perform the operation on all types
        :arg body: The search definition template and its params
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        :arg search_type: Search operation type, valid choices are:
            'query_then_fetch', 'query_and_fetch', 'dfs_query_then_fetch',
            'dfs_query_and_fetch', 'count', 'scan'
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_search', 'template'), params=params, body=body)
        return data

    @query_params('_source', '_source_exclude', '_source_include',
        'analyze_wildcard', 'analyzer', 'default_operator', 'df', 'fields',
        'lenient', 'lowercase_expanded_terms', 'parent', 'preference', 'q',
        'routing')
    def explain(self, index, doc_type, id, body=None, params=None):
        """
        The explain api computes a score explanation for a query and a specific
        document. This can give useful feedback whether a document matches or
        didn't match a specific query.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-explain.html>`_

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
            or OR), default 'OR', valid choices are: 'AND', 'OR'
        :arg df: The default field for query string query (default: _all)
        :arg fields: A comma-separated list of fields to return in the response
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg lowercase_expanded_terms: Specify whether query terms should be
            lowercased
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        """
        for param in (index, doc_type, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_explain'), params=params, body=body)
        return data

    @query_params('scroll')
    def scroll(self, scroll_id=None, body=None, params=None):
        """
        Scroll a search request created by specifying the scroll parameter.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_

        :arg scroll_id: The scroll ID
        :arg body: The scroll ID if not passed by URL or query parameter.
        :arg scroll: Specify how long a consistent view of the index should be
            maintained for scrolled search
        """
        if scroll_id in SKIP_IN_PATH and body in SKIP_IN_PATH:
            raise ValueError("You need to supply scroll_id or body.")
        elif scroll_id and not body:
            body = scroll_id
        elif scroll_id:
            params['scroll_id'] = scroll_id

        _, data = self.transport.perform_request('GET', '/_search/scroll',
            params=params, body=body)
        return data

    @query_params()
    def clear_scroll(self, scroll_id=None, body=None, params=None):
        """
        Clear the scroll request created by specifying the scroll parameter to
        search.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-scroll.html>`_

        :arg scroll_id: A comma-separated list of scroll IDs to clear
        :arg body: A comma-separated list of scroll IDs to clear if none was
            specified via the scroll_id parameter
        """
        _, data = self.transport.perform_request('DELETE', _make_path('_search',
            'scroll', scroll_id), params=params, body=body)
        return data

    @query_params('consistency', 'parent', 'refresh', 'routing', 'timeout',
        'version', 'version_type')
    def delete(self, index, doc_type, id, params=None):
        """
        Delete a typed JSON document from a specific index based on its id.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html>`_

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: The document ID
        :arg consistency: Specific write consistency setting for the operation,
            valid choices are: 'one', 'quorum', 'all'
        :arg parent: ID of parent document
        :arg refresh: Refresh the index after performing the operation
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (index, doc_type, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('DELETE', _make_path(index,
            doc_type, id), params=params)
        return data

    @query_params('allow_no_indices', 'analyze_wildcard', 'analyzer',
        'default_operator', 'df', 'expand_wildcards', 'ignore_unavailable',
        'lenient', 'lowercase_expanded_terms', 'min_score', 'preference', 'q',
        'routing')
    def count(self, index=None, doc_type=None, body=None, params=None):
        """
        Execute a query and get the number of matches for that query.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-count.html>`_

        :arg index: A comma-separated list of indices to restrict the results
        :arg doc_type: A comma-separated list of types to restrict the results
        :arg body: A query to restrict the results specified with the Query DSL
            (optional)
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyze_wildcard: Specify whether wildcard and prefix queries
            should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string query (AND
            or OR), default 'OR', valid choices are: 'AND', 'OR'
        :arg df: The field to use as default where no field prefix is given in
            the query string
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg lowercase_expanded_terms: Specify whether query terms should be
            lowercased
        :arg min_score: Include only documents with a specific `_score` value in
            the result
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        """
        if doc_type and not index:
            index = '_all'

        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_count'), params=params, body=body)
        return data

    @query_params('consistency', 'fields', 'refresh', 'routing', 'timeout')
    def bulk(self, body, index=None, doc_type=None, params=None):
        """
        Perform many index/delete operations in a single API call.

        See the :func:`~elasticsearch.helpers.bulk` helper function for a more
        friendly API.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html>`_

        :arg body: The operation definition and data (action-data pairs),
            separated by newlines
        :arg index: Default index for items which don't provide one
        :arg doc_type: Default document type for items which don't provide one
        :arg consistency: Explicit write consistency setting for the operation,
            valid choices are: 'one', 'quorum', 'all'
        :arg fields: Default comma-separated list of fields to return in the
            response for updates
        :arg refresh: Refresh the index after performing the operation
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        _, data = self.transport.perform_request('POST', _make_path(index,
            doc_type, '_bulk'), params=params, body=self._bulk_body(body))
        return data

    @query_params('search_type')
    def msearch(self, body, index=None, doc_type=None, params=None):
        """
        Execute several search requests within the same API.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-multi-search.html>`_

        :arg body: The request definitions (metadata-search request definition
            pairs), separated by newlines
        :arg index: A comma-separated list of index names to use as default
        :arg doc_type: A comma-separated list of document types to use as
            default
        :arg search_type: Search operation type, valid choices are:
            'query_then_fetch', 'query_and_fetch', 'dfs_query_then_fetch',
            'dfs_query_and_fetch', 'count', 'scan'
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_msearch'), params=params, body=self._bulk_body(body))
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'preference', 'routing')
    def suggest(self, body, index=None, params=None):
        """
        The suggest feature suggests similar looking terms based on a provided
        text by using a suggester.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html>`_

        :arg body: The request definition
        :arg index: A comma-separated list of index names to restrict the
            operation; use `_all` or empty string to perform the operation on
            all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: Specific routing value
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        _, data = self.transport.perform_request('POST', _make_path(index,
            '_suggest'), params=params, body=body)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable',
        'percolate_format', 'percolate_index', 'percolate_preference',
        'percolate_routing', 'percolate_type', 'preference', 'routing',
        'version', 'version_type')
    def percolate(self, index, doc_type, id=None, body=None, params=None):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-percolate.html>`_

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
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg percolate_format: Return an array of matching query IDs instead of
            objects, valid choices are: 'ids'
        :arg percolate_index: The index to percolate the document into. Defaults
            to index.
        :arg percolate_preference: Which shard to prefer when executing the
            percolate request.
        :arg percolate_routing: The routing value to use when percolating the
            existing document.
        :arg percolate_type: The type to percolate document into. Defaults to
            type.
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg routing: A comma-separated list of specific routing values
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (index, doc_type):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_percolate'), params=params, body=body)
        return data

    @query_params('allow_no_indices', 'expand_wildcards', 'ignore_unavailable')
    def mpercolate(self, body, index=None, doc_type=None, params=None):
        """
        The percolator allows to register queries against an index, and then
        send percolate requests which include a doc, and getting back the
        queries that match on that doc out of the set of registered queries.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-percolate.html>`_

        :arg body: The percolate request definitions (header & body pair),
            separated by newlines
        :arg index: The index of the document being count percolated to use as
            default
        :arg doc_type: The type of the document being percolated to use as
            default.
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
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
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-percolate.html>`_

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
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
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
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (index, doc_type):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_percolate', 'count'), params=params, body=body)
        return data

    @query_params('dfs', 'field_statistics', 'fields', 'offsets', 'parent',
        'payloads', 'positions', 'preference', 'realtime', 'routing',
        'term_statistics', 'version', 'version_type')
    def termvectors(self, index, doc_type, id=None, body=None, params=None):
        """
        Returns information and statistics on terms in the fields of a
        particular document. The document could be stored in the index or
        artificially provided by the user (Added in 1.4). Note that for
        documents stored in the index, this is a near realtime API as the term
        vectors are not available until the next refresh.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-termvectors.html>`_

        :arg index: The index in which the document resides.
        :arg doc_type: The type of the document.
        :arg id: The id of the document, when not specified a doc param should
            be supplied.
        :arg body: Define parameters and or supply a document to get termvectors
            for. See documentation.
        :arg dfs: Specifies if distributed frequencies should be returned
            instead shard frequencies., default False
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
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (index, doc_type):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, id, '_termvectors'), params=params, body=body)
        return data

    @query_params('field_statistics', 'fields', 'ids', 'offsets', 'parent',
        'payloads', 'positions', 'preference', 'realtime', 'routing',
        'term_statistics', 'version', 'version_type')
    def mtermvectors(self, index=None, doc_type=None, body=None, params=None):
        """
        Multi termvectors API allows to get multiple termvectors based on an
        index, type and id.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/docs-multi-termvectors.html>`_

        :arg index: The index in which the document resides.
        :arg doc_type: The type of the document.
        :arg body: Define ids, documents, parameters or a list of parameters per
            document here. You must at least provide a list of document ids. See
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
        :arg realtime: Specifies if requests are real-time as opposed to near-
            real-time (default: true).
        :arg routing: Specific routing value. Applies to all returned documents
            unless otherwise specified in body "params" or "docs".
        :arg term_statistics: Specifies if total term frequency and document
            frequency should be returned. Applies to all returned documents
            unless otherwise specified in body "params" or "docs"., default
            False
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            doc_type, '_mtermvectors'), params=params, body=body)
        return data

    @query_params('op_type', 'version', 'version_type')
    def put_script(self, lang, id, body, params=None):
        """
        Create a script in given language with specified ID.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg body: The document
        :arg op_type: Explicit operation type, default 'index', valid choices
            are: 'index', 'create'
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (lang, id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('PUT', _make_path('_scripts',
            lang, id), params=params, body=body)
        return data

    @query_params('version', 'version_type')
    def get_script(self, lang, id, params=None):
        """
        Retrieve a script from the API.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (lang, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('GET', _make_path('_scripts',
            lang, id), params=params)
        return data

    @query_params('version', 'version_type')
    def delete_script(self, lang, id, params=None):
        """
        Remove a stored script from elasticsearch.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html>`_

        :arg lang: Script language
        :arg id: Script ID
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (lang, id):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('DELETE',
            _make_path('_scripts', lang, id), params=params)
        return data

    @query_params('op_type', 'version', 'version_type')
    def put_template(self, id, body, params=None):
        """
        Create a search template.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg body: The document
        :arg op_type: Explicit operation type, default 'index', valid choices
            are: 'index', 'create'
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        _, data = self.transport.perform_request('PUT', _make_path('_search',
            'template', id), params=params, body=body)
        return data

    @query_params('version', 'version_type')
    def get_template(self, id, params=None):
        """
        Retrieve a search template.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('GET', _make_path('_search',
            'template', id), params=params)
        return data

    @query_params('version', 'version_type')
    def delete_template(self, id, params=None):
        """
        Delete a search template.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: Template ID
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type, valid choices are: 'internal',
            'external', 'external_gte', 'force'
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")
        _, data = self.transport.perform_request('DELETE', _make_path('_search',
            'template', id), params=params)
        return data

    @query_params('allow_no_indices', 'analyze_wildcard', 'analyzer',
        'default_operator', 'df', 'expand_wildcards', 'ignore_unavailable',
        'lenient', 'lowercase_expanded_terms', 'min_score', 'preference', 'q',
        'routing')
    def search_exists(self, index=None, doc_type=None, body=None, params=None):
        """
        The exists API allows to easily determine if any matching documents
        exist for a provided query.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-exists.html>`_

        :arg index: A comma-separated list of indices to restrict the results
        :arg doc_type: A comma-separated list of types to restrict the results
        :arg body: A query to restrict the results specified with the Query DSL
            (optional)
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyze_wildcard: Specify whether wildcard and prefix queries
            should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string query (AND
            or OR), default 'OR', valid choices are: 'AND', 'OR'
        :arg df: The field to use as default where no field prefix is given in
            the query string
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such as
            providing text to a numeric field) should be ignored
        :arg lowercase_expanded_terms: Specify whether query terms should be
            lowercased
        :arg min_score: Include only documents with a specific `_score` value in
            the result
        :arg preference: Specify the node or shard the operation should be
            performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: Specific routing value
        """
        try:
            self.transport.perform_request('POST', _make_path(index,
                doc_type, '_search', 'exists'), params=params, body=body)
        except NotFoundError:
            return False
        return True

    @query_params('allow_no_indices', 'expand_wildcards', 'fields',
        'ignore_unavailable', 'level')
    def field_stats(self, index=None, body=None, params=None):
        """
        The field stats api allows one to find statistical properties of a
        field without executing a search, but looking up measurements that are
        natively available in the Lucene index.
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/search-field-stats.html>`_

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg body: Field json objects containing the name and optionally a range
            to filter out indices result, that have results outside the defined
            bounds
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to concrete
            indices that are open, closed or both., default 'open', valid
            choices are: 'open', 'closed', 'none', 'all'
        :arg fields: A comma-separated list of fields for to get field
            statistics for (min value, max value, and more)
        :arg ignore_unavailable: Whether specified concrete indices should be
            ignored when unavailable (missing or closed)
        :arg level: Defines if field stats should be returned on a per index
            level or on a cluster wide level, default 'cluster', valid choices
            are: 'indices', 'cluster'
        """
        _, data = self.transport.perform_request('GET', _make_path(index,
            '_field_stats'), params=params, body=body)
        return data

    @query_params()
    def render_search_template(self, id=None, body=None, params=None):
        """
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-template.html>`_

        :arg id: The id of the stored search template
        :arg body: The search definition template and its params
        """
        _, data = self.transport.perform_request('GET', _make_path('_render',
            'template', id), params=params, body=body)
        return data


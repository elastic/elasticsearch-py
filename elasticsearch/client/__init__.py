from ..transport import Transport
from .indices import IndicesClient
from .cluster import ClusterClient
from .utils import query_params, _make_path

def _normalize_hosts(hosts):
    """
    Helper function to transform hosts argument to
    :class:`~elasticsearch.Elasticsearch` to a list of dicts.
    """
    # if hosts are empty, just defer to defaults down the line
    if hosts is None:
        return [{}]

    out = []
    # normalize hosts to dicts
    for i, host in enumerate(hosts):
        if isinstance(host, (type(''), type(u''))):
            h = {"host": host}
            if ':' in host:
                # TODO: detect auth urls
                host, port = host.rsplit(':', 1)
                if port.isdigit():
                    port = int(port)
                    h = {"host": host, "port": port}
            out.append(h)
        else:
            out.append(host)
    return out


class Elasticsearch(object):
    """
    Elasticsearch low-level client. Provides a straightforward mapping from
    Python to ES REST endpoints.
    """
    def __init__(self, hosts=None, transport_class=Transport, **kwargs):
        """
        :arg hosts: list of nodes we should connect to. Node should be a
            dictionary ({"host": "localhost", "port": 9200}), the entire dictionary
            will be passed to the :class:`~elasticsearch.Connection` class as
            kwargs, or a string in the format ot ``host[:port]`` which will be
            translated to a dictionary automatically.  If no value is given the
            :class:`~elasticsearch.Connection` class defaults will be used.

        :arg transport_class: :class:`~elasticsearch.Transport` subclass to use.

        :arg kwargs: any additional arguments will be passed on to the
            :class:`~elasticsearch.Transport` class and, subsequently, to the
            :class:`~elasticsearch.Connection` instances.
        """
        self.transport = transport_class(_normalize_hosts(hosts), **kwargs)

        # namespaced clients for compatibility with API names
        self.indices = IndicesClient(self)
        self.cluster = ClusterClient(self)

    @query_params('consistency', 'id', 'parent', 'percolate', 'refresh', 'replication', 'routing', 'timeout', 'timestamp', 'ttl', 'version', 'version_type')
    def create(self, index, doc_type, body, id=None, params=None):
        """
        The index API adds or updates a typed JSON document in a specific index, making it searchable.
        http://elasticsearch.org/guide/reference/api/index_/

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: Document ID
        :arg body: The document
        :arg consistency: Explicit write consistency setting for the operation
        :arg id: Specific document ID (when the POST method is used)
        :arg parent: ID of the parent document
        :arg percolate: Percolator queries to execute while indexing the document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type, default u'sync'
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg timestamp: Explicit timestamp for the document
        :arg ttl: Expiration time for the document
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        params['op_type'] = 'create'
        status, data = self.transport.perform_request('PUT' if id else 'POST', _make_path(index, doc_type, id), params=params, body=body)
        return data

    @query_params('fields', 'parent', 'preference', 'realtime', 'refresh', 'routing')
    def get(self, index, doc_type, id, params=None):
        """
        The get API allows to get a typed JSON document from the index based on its id.
        http://elasticsearch.org/guide/reference/api/get/

        :arg index: The name of the index
        :arg doc_type: The type of the document (use `_all` to fetch the first document matching the ID across all types)
        :arg id: The document ID
        :arg fields: A comma-separated list of fields to return in the response
        :arg parent: The ID of the parent document
        :arg preference: Specify the node or shard the operation should be performed on (default: random)
        :arg realtime: Specify whether to perform the operation in realtime or search mode
        :arg refresh: Refresh the shard containing the document before performing the operation
        :arg routing: Specific routing value
        """
        status, data = self.transport.perform_request('GET', _make_path(index, doc_type, id), params=params)
        return data

    @query_params('analyze_wildcard', 'analyzer', 'default_operator', 'df', 'explain', 'fields', 'ignore_indices', 'indices_boost', 'lenient', 'lowercase_expanded_terms', 'offset', 'preference', 'q', 'routing', 'scroll', 'search_type', 'size', 'sort', 'source', 'stats', 'suggest_field', 'suggest_mode', 'suggest_size', 'suggest_text', 'timeout', 'version')
    def search(self, index=None, doc_type=None, body=None, params=None):
        """
        The search API allows to execute a search query and get back search hits that match the query.
        http://www.elasticsearch.org/guide/reference/api/search/

        :arg index: A comma-separated list of index names to search; use `_all` or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to search; leave empty to perform the operation on all types
        :arg body: The search definition using the Query DSL
        :arg analyze_wildcard: Specify whether wildcard and prefix queries should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string query (AND or OR), default u'OR'
        :arg df: The field to use as default where no field prefix is given in the query string
        :arg explain: Specify whether to return detailed information about score computation as part of a hit
        :arg fields: A comma-separated list of fields to return as part of a hit
        :arg ignore_indices: When performed on multiple indices, allows to ignore `missing` ones, default u'none'
        :arg indices_boost: Comma-separated list of index boosts
        :arg lenient: Specify whether format-based query failures (such as providing text to a numeric field) should be ignored
        :arg lowercase_expanded_terms: Specify whether query terms should be lowercased
        :arg offset: Starting offset (default: 0)
        :arg preference: Specify the node or shard the operation should be performed on (default: random)
        :arg q: Query in the Lucene query string syntax
        :arg routing: A comma-separated list of specific routing values
        :arg scroll: Specify how long a consistent view of the index should be maintained for scrolled search
        :arg search_type: Search operation type
        :arg size: Number of hits to return (default: 10)
        :arg sort: A comma-separated list of <field>:<direction> pairs
        :arg source: The URL-encoded request definition using the Query DSL (instead of using request body)
        :arg stats: Specific 'tag' of the request for logging and statistical purposes
        :arg suggest_field: Specify which field to use for suggestions
        :arg suggest_mode: Specify suggest mode, default u'missing'
        :arg suggest_size: How many suggestions to return in response
        :arg suggest_text: The source text for which the suggestions should be returned
        :arg timeout: Explicit operation timeout
        :arg version: Specify whether to return document version as part of a hit
        """
        if doc_type and not index:
            index = '_all'
        status, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_search'), params=params, body=body)
        return data

    @query_params('consistency', 'parent', 'refresh', 'replication', 'routing', 'timeout', 'version', 'version_type')
    def delete(self, index, doc_type, id, params=None):
        """
        The delete API allows to delete a typed JSON document from a specific index based on its id.
        http://elasticsearch.org/guide/reference/api/delete/

        :arg index: The name of the index
        :arg doc_type: The type of the document
        :arg id: The document ID
        :arg consistency: Specific write consistency setting for the operation
        :arg parent: ID of parent document
        :arg refresh: Refresh the index after performing the operation
        :arg replication: Specific replication type, default u'sync'
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        :arg version: Explicit version number for concurrency control
        :arg version_type: Specific version type
        """
        status, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, id), params=params)
        return data


from functools import wraps
try:
    # PY2
    from urllib import quote_plus
except ImportError:
    # PY3
    from urllib.parse import quote_plus

from .transport import Transport
from .exceptions import NotFoundError

# parts of URL to be omitted
SKIP_IN_PATH = (None, '', [], ())

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

def _escape(part):
    """
    Escape a single part of a URL string. If it is a list or tuple, turn it
    into a comma-separated string first.
    """
    if isinstance(part, (list, tuple)):
        part = ','.join(part)
    # mark ',' as safe for nicer url in logs
    return quote_plus(part, ',')

def _make_path(*parts):
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists nad tuples to comma separated values.
    """
    #TODO: maybe only allow some parts to be lists/tuples ?
    return '/' + '/'.join(_escape(p) for p in parts if p not in SKIP_IN_PATH)


# parameters that apply to all methods
GLOBAL_PARAMS = ('pretty', )

def query_params(*es_query_params):
    """
    Decorator that pops all accepted parameters from method's kwargs and puts
    them in the params argument.
    """
    def _wrapper(func):
        @wraps(func)
        def _wrapped(*args, **kwargs):
            params = kwargs.pop('params', {})
            for p in es_query_params + GLOBAL_PARAMS:
                if p in kwargs:
                    params[p] = kwargs.pop(p)
            return func(*args, params=params, **kwargs)
        return _wrapped
    return _wrapper


class NamespacedClient(object):
    def __init__(self, client):
        self.client = client

    @property
    def transport(self):
        return self.client.transport

class ClusterClient(NamespacedClient):
    @query_params('level', 'local', 'master_timeout', 'timeout', 'wait_for_active_shards', 'wait_for_nodes', 'wait_for_relocating_shards', 'wait_for_status')
    def health(self, index=None, params=None):
        """
        The cluster health API allows to get a very simple status on the health of the cluster.
        http://elasticsearch.org/guide/reference/api/admin-cluster-health/

        :arg index: Limit the information returned to a specific index
        :arg level: Specify the level of detail for returned information, default u'cluster'
        :arg local: Return local information, do not retrieve the state from master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master node
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Wait until the specified number of shards is active
        :arg wait_for_nodes: Wait until the specified number of nodes is available
        :arg wait_for_relocating_shards: Wait until the specified number of relocating shards is finished
        :arg wait_for_status: Wait until cluster is in a specific state, default None
        """
        status, data = self.transport.perform_request('GET', _make_path('_cluster', 'health', index), params=params)
        return data

class InidicesClient(NamespacedClient):
    @query_params('analyzer', 'field', 'filters', 'format', 'index', 'prefer_local', 'text', 'tokenizer')
    def analyze(self, index=None, body=None, params=None):
        """
        Performs the analysis process on a text and return the tokens breakdown of the text.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-analyze/

        :arg index: The name of the index to scope the operation
        :arg body: The text on which the analysis should be performed
        :arg analyzer: The name of the analyzer to use
        :arg field: The name of the field to
        :arg filters: A comma-separated list of filters to use for the analysis
        :arg format: Format of the output, default u'detailed'
        :arg index: The name of the index to scope the operation
        :arg prefer_local: With `true`, specify that a local shard should be used if available, with `false`, use a random shard (default: true)
        :arg text: The text on which the analysis should be performed (when request body is not used)
        :arg tokenizer: The name of the tokenizer to use for the analysis
        """
        status, data = self.transport.perform_request('GET', _make_path(index, '_analyze'), params=params, body=body)
        return data

    @query_params('ignore_indices')
    def refresh(self, index=None, params=None):
        """
        The refresh API allows to explicitly refresh one or more index, making all operations performed since the last refresh available for search.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-refresh/

        :arg index: A comma-separated list of index names; use `_all` or empty string to perform the operation on all indices
        :arg ignore_indices: When performed on multiple indices, allows to ignore `missing` ones, default u'none'
        """
        status, data = self.transport.perform_request('POST', _make_path(index, '_refresh'), params=params)
        return data

    @query_params('timeout')
    def create(self, index, body=None, params=None):
        """
        Create index in Elasticsearch.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index/

        :arg index: The name of the index
        :arg body: The configuration for the index (`settings` and `mappings`)
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('PUT', _make_path(index), params=params, body=body)
        return data

    @query_params('timeout')
    def delete(self, index=None, params=None):
        """
        Delete index in Elasticsearch
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-index/

        :arg index: A list of indices to delete, `None` if all indices should be removed.
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('DELETE', _make_path(index), params=params)
        return data

    @query_params()
    def exists(self, index, params=None):
        """
        http://www.elasticsearch.org/guide/reference/api/admin-indices-indices-exists/

        :arg index: A list of indices to check
        """
        try:
            self.transport.perform_request('HEAD', _make_path(index), params=params)
        except NotFoundError:
            return False
        return True

    @query_params('ignore_conflicts', 'timeout')
    def put_mapping(self, index, body, doc_type=None, params=None):
        """
        The put mapping API allows to register specific mapping definition for a specific type.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-put-mapping/

        :arg index: A comma-separated list of index names; use `_all` to perform the operation on all indices
        :arg doc_type: The name of the document type
        :arg body: The mapping definition
        :arg ignore_conflicts: Specify whether to ignore conflicts while updating the mapping (default: false)
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('PUT', _make_path(index, doc_type, '_mapping'), params=params, body=body)
        return data

    @query_params()
    def get_mapping(self, index=None, doc_type=None, params=None):
        """
        The get mapping API allows to retrieve mapping definition of index or index/type.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-get-mapping/

        :arg index: A comma-separated list of index names; use `_all` or empty string for all indices
        :arg doc_type: A comma-separated list of document types
        """
        status, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_mapping'), params=params)
        return data

    @query_params()
    def delete_mapping(self, index, doc_type, params=None):
        """
        Allow to delete a mapping (type) along with its data.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-mapping/

        :arg index: A comma-separated list of index names; use `_all` for all indices
        :arg doc_type: The name of the document type to delete
        """
        status, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, '_mapping'), params=params)
        return data


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
        self.indices = InidicesClient(self)
        self.cluster = ClusterClient(self)


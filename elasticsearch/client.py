from functools import wraps
try:
    # PY2
    from urllib import quote_plus
except ImportError:
    # PY3
    from urllib.parse import quote_plus

from .transport import Transport
from .exceptions import NotFoundError

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

def _normalize_list(list_or_string):
    """
    for index and type arguments in url, identify if it's a string or a
    sequence and produce a working representation (comma separated string).
    """
    if isinstance(list_or_string, (type(''), type(u''))):
        return quote_plus(list_or_string)
    return quote_plus(','.join(list_or_string))


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
    pass

class InidicesClient(NamespacedClient):
    @query_params('timeout')
    def create(self, index, body=None, params=None):
        """
        Create index in Elasticsearch.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index/

        :arg index: The name of the index
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('PUT', '/%s' % quote_plus(index), params=params, body=body)
        return data

    @query_params('timeout')
    def delete(self, index=None, params=None):
        """
        Delete index in Elasticsearch
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-index/

        :arg timeout: Explicit operation timeout
        """
        url = '/' if not index else '/' + _normalize_list(index)
        status, data = self.transport.perform_request('DELETE', url, params=params)
        return data

    @query_params()
    def exists(self, index, params=None):
        """
        http://www.elasticsearch.org/guide/reference/api/admin-indices-indices-exists/

        :arg index: A comma-separated list of indices to check
        """
        try:
            self.transport.perform_request('HEAD', '/' + _normalize_list(index), params=params)
        except NotFoundError:
            return False
        return True


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


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


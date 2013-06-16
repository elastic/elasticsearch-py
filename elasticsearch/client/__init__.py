from ..transport import Transport
from .indices import IndicesClient
from .cluster import ClusterClient

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

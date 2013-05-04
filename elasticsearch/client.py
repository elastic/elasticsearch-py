from .transport import Transport

def _normalize_hosts(hosts):
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

class ElasticSearch(object):
    def __init__(self, hosts=None, **kwargs):
        self.transport = Transport(_normalize_hosts(hosts), **kwargs)

from functools import wraps
try:
    # PY2
    from urllib import quote_plus
except ImportError:
    # PY3
    from urllib.parse import quote_plus

# parts of URL to be omitted
SKIP_IN_PATH = (None, '', [], ())

def _escape(part):
    """
    Escape a single part of a URL string. If it is a list or tuple, turn it
    into a comma-separated string first.
    """
    if isinstance(part, (list, tuple)):
        part = ','.join(part)
    if isinstance(part, (type(''), type(u''))):
        # mark ',' as safe for nicer url in logs
        return quote_plus(part, ',')
    return str(part)

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
                    val = kwargs.pop(p)
                    if isinstance(val, (list, tuple)):
                        val = ','.join(val)
                    params[p] = val
            return func(*args, params=params, **kwargs)
        return _wrapped
    return _wrapper


class NamespacedClient(object):
    def __init__(self, client):
        self.client = client

    @property
    def transport(self):
        return self.client.transport

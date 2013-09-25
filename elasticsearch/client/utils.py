from datetime import date, datetime
from functools import wraps
try:
    # PY2
    from urllib import quote_plus
except ImportError:
    # PY3
    from urllib.parse import quote_plus

# parts of URL to be omitted
SKIP_IN_PATH = (None, '', [], ())

def _escape(value):
    """
    Escape a single value of a URL string or a query parameter. If it is a list
    or tuple, turn it into a comma-separated string first.
    """

    # make sequences into comma-separated stings
    if isinstance(value, (list, tuple)):
        value = u','.join(value)

    # dates and datetimes into isoformat
    elif isinstance(value, (date, datetime)):
        value = value.isoformat()

    # make bools into true/false strings
    elif isinstance(value, bool):
        value = str(value).lower()

    # encode strings to utf-8
    if isinstance(value, (type(''), type(u''))):
        try:
            return value.encode('utf-8')
        except UnicodeDecodeError:
            # Python 2 and str, no need to re-encode
            pass
    
    return str(value)

def _make_path(*parts):
    """
    Create a URL string from parts, omit all `None` values and empty strings.
    Convert lists nad tuples to comma separated values.
    """
    #TODO: maybe only allow some parts to be lists/tuples ?
    return '/' + '/'.join(
        quote_plus(_escape(p), ',') for p in parts if p not in SKIP_IN_PATH)

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
                    params[p] = _escape(kwargs.pop(p))

            # don't treat ignore as other params to avoid escaping
            if 'ignore' in kwargs:
                params['ignore'] = kwargs.pop('ignore')
            return func(*args, params=params, **kwargs)
        return _wrapped
    return _wrapper


class NamespacedClient(object):
    def __init__(self, client):
        self.client = client

    @property
    def transport(self):
        return self.client.transport

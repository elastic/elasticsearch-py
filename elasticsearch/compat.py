import sys

PY2 = sys.version_info[0] == 2

if PY2:
    u = lambda s: s.decode('utf-8')
    string_types = basestring,
    from urllib import quote_plus, urlencode
    from itertools import imap as map
else:
    u = str
    string_types = str, bytes
    from urllib.parse import quote_plus, urlencode
    map = map

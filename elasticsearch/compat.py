import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_types = basestring,
    from urllib import quote_plus, urlencode
    from urlparse import  urlparse
    from itertools import imap as map
else:
    string_types = str, bytes
    from urllib.parse import quote_plus, urlencode, urlparse
    map = map

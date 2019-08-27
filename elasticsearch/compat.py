import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_types = (basestring,)
    text_type = unicode
    from urllib import quote_plus, urlencode, unquote
    from urlparse import urlparse
    from itertools import imap as map
    from Queue import Queue
else:
    string_types = str, bytes
    text_type = str
    from urllib.parse import quote_plus, urlencode, urlparse, unquote

    map = map
    from queue import Queue

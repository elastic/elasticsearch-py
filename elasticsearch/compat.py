# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_types = (basestring,)  # noqa: F821
    from urllib import quote_plus, quote, urlencode, unquote
    from urlparse import urlparse
    from itertools import imap as map
    from Queue import Queue
else:
    string_types = str, bytes
    from urllib.parse import quote, quote_plus, urlencode, urlparse, unquote

    map = map
    from queue import Queue

__all__ = [
    "string_types",
    "quote_plus",
    "quote",
    "urlencode",
    "unquote",
    "urlparse",
    "map",
    "Queue",
]

#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import sys

PY2 = sys.version_info[0] == 2

if PY2:
    string_types = (basestring,)  # noqa: F821
    from itertools import imap as map
    from urllib import quote, quote_plus, unquote, urlencode

    from Queue import Queue
    from urlparse import urlparse
else:
    string_types = str, bytes
    from urllib.parse import quote, quote_plus, unquote, urlencode, urlparse

    map = map
    from queue import Queue

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


__all__ = [
    "string_types",
    "quote_plus",
    "quote",
    "urlencode",
    "unquote",
    "urlparse",
    "map",
    "Queue",
    "Mapping",
]

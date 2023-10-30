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

import asyncio
from collections.abc import Mapping
from queue import Queue
from urllib.parse import quote, quote_plus, unquote, urlencode, urlparse

string_types = str, bytes

map = map


def to_str(x, encoding="ascii"):
    if not isinstance(x, str):
        return x.decode(encoding)
    return x


def to_bytes(x, encoding="ascii"):
    if not isinstance(x, bytes):
        return x.encode(encoding)
    return x


reraise_exceptions = (RecursionError, asyncio.CancelledError)

try:
    from threading import Lock
except ImportError:  # Python <3.7 isn't guaranteed to have threading support.

    class Lock:
        def __enter__(self):
            pass

        def __exit__(self, *_):
            pass


__all__ = [
    "string_types",
    "reraise_exceptions",
    "quote_plus",
    "quote",
    "urlencode",
    "unquote",
    "urlparse",
    "map",
    "Queue",
    "Mapping",
]

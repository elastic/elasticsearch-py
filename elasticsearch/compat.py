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

from queue import Queue
from typing import Tuple, Type, Union
from urllib.parse import quote, quote_plus, unquote, urlencode, urlparse

string_types: Tuple[Type[str], Type[bytes]] = (str, bytes)


def to_str(x: Union[str, bytes], encoding: str = "ascii") -> str:
    if not isinstance(x, str):
        return x.decode(encoding)
    return x


def to_bytes(x: Union[str, bytes], encoding: str = "ascii") -> bytes:
    if not isinstance(x, bytes):
        return x.encode(encoding)
    return x


try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


reraise_exceptions: Tuple[Type[Exception], ...] = (RecursionError,)

try:
    import asyncio

    reraise_exceptions += (asyncio.CancelledError,)
except (ImportError, AttributeError):
    pass


__all__ = [
    "string_types",
    "reraise_exceptions",
    "quote_plus",
    "quote",
    "urlencode",
    "unquote",
    "urlparse",
    "Queue",
    "Mapping",
]

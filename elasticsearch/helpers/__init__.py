# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import sys
from .errors import BulkIndexError, ScanError
from .actions import expand_action, streaming_bulk, bulk, parallel_bulk
from .actions import scan, reindex
from .actions import _chunk_actions, _process_bulk_chunk

__all__ = [
    "BulkIndexError",
    "ScanError",
    "expand_action",
    "streaming_bulk",
    "bulk",
    "parallel_bulk",
    "scan",
    "reindex",
    "_chunk_actions",
    "_process_bulk_chunk",
]


try:
    # Asyncio only supported on Python 3.6+
    if sys.version_info < (3, 6):
        raise ImportError

    from .._async.helpers import (
        async_scan,
        async_bulk,
        async_reindex,
        async_streaming_bulk,
    )

    __all__ += ["async_scan", "async_bulk", "async_reindex", "async_streaming_bulk"]
except (ImportError, SyntaxError):
    pass

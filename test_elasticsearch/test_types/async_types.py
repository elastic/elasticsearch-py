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

from typing import Any, AsyncGenerator, Dict

from elasticsearch import (
    AIOHttpConnection,
    AsyncElasticsearch,
    AsyncTransport,
    ConnectionPool,
)
from elasticsearch.helpers import (
    async_bulk,
    async_reindex,
    async_scan,
    async_streaming_bulk,
)

es = AsyncElasticsearch(
    [{"host": "localhost", "port": 9443}],
    transport_class=AsyncTransport,
)
t = AsyncTransport(
    [{}],
    connection_class=AIOHttpConnection,
    connection_pool_class=ConnectionPool,
    sniff_on_start=True,
    sniffer_timeout=0.1,
    sniff_timeout=1,
    sniff_on_connection_fail=False,
    max_retries=1,
    retry_on_status={100, 400, 503},
    retry_on_timeout=True,
    send_get_body_as="source",
)


async def async_gen() -> AsyncGenerator[Dict[Any, Any], None]:
    yield {}


async def async_scan_types() -> None:
    async for _ in async_scan(
        es,
        query={"query": {"match_all": {}}},
        request_timeout=10,
        clear_scroll=True,
        scroll_kwargs={"request_timeout": 10},
    ):
        pass
    async for _ in async_scan(
        es,
        raise_on_error=False,
        preserve_order=False,
        scroll="10m",
        size=10,
        request_timeout=10.0,
    ):
        pass


async def async_streaming_bulk_types() -> None:
    async for _ in async_streaming_bulk(es, async_gen()):
        pass
    async for _ in async_streaming_bulk(es, async_gen().__aiter__()):
        pass
    async for _ in async_streaming_bulk(es, [{}]):
        pass
    async for _ in async_streaming_bulk(es, ({},)):
        pass


async def async_bulk_types() -> None:
    _, _ = await async_bulk(es, async_gen())
    _, _ = await async_bulk(es, async_gen().__aiter__())
    _, _ = await async_bulk(es, [{}])
    _, _ = await async_bulk(es, ({},))


async def async_reindex_types() -> None:
    _, _ = await async_reindex(
        es, "src-index", "target-index", query={"query": {"match": {"key": "val"}}}
    )
    _, _ = await async_reindex(
        es, source_index="src-index", target_index="target-index", target_client=es
    )
    _, _ = await async_reindex(
        es,
        "src-index",
        "target-index",
        chunk_size=1,
        scroll="10m",
        scan_kwargs={"request_timeout": 10},
        bulk_kwargs={"request_timeout": 10},
    )

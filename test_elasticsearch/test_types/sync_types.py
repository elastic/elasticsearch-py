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

from typing import Any, Dict, Generator

from elasticsearch import (
    ConnectionPool,
    Elasticsearch,
    RequestsHttpConnection,
    Transport,
)
from elasticsearch.helpers import bulk, reindex, scan, streaming_bulk

es = Elasticsearch(
    [{"host": "localhost", "port": 9443}],
    transport_class=Transport,
)
t = Transport(
    [{}],
    connection_class=RequestsHttpConnection,
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


def sync_gen() -> Generator[Dict[Any, Any], None, None]:
    yield {}


def scan_types() -> None:
    for _ in scan(
        es,
        query={"query": {"match_all": {}}},
        request_timeout=10,
        clear_scroll=True,
        scroll_kwargs={"request_timeout": 10},
    ):
        pass
    for _ in scan(
        es,
        raise_on_error=False,
        preserve_order=False,
        scroll="10m",
        size=10,
        request_timeout=10.0,
    ):
        pass


def streaming_bulk_types() -> None:
    for _ in streaming_bulk(es, sync_gen()):
        pass
    for _ in streaming_bulk(es, sync_gen().__iter__()):
        pass
    for _ in streaming_bulk(es, [{}]):
        pass
    for _ in streaming_bulk(es, ({},)):
        pass


def bulk_types() -> None:
    _, _ = bulk(es, sync_gen())
    _, _ = bulk(es, sync_gen().__iter__())
    _, _ = bulk(es, [{}])
    _, _ = bulk(es, ({},))


def reindex_types() -> None:
    _, _ = reindex(
        es, "src-index", "target-index", query={"query": {"match": {"key": "val"}}}
    )
    _, _ = reindex(
        es, source_index="src-index", target_index="target-index", target_client=es
    )
    _, _ = reindex(
        es,
        "src-index",
        "target-index",
        chunk_size=1,
        scroll="10m",
        scan_kwargs={"request_timeout": 10},
        bulk_kwargs={"request_timeout": 10},
    )

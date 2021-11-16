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

import pytest

import elasticsearch

from ...utils import CA_CERTS, wipe_cluster

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("sync_client")
async def async_client(elasticsearch_url):
    # 'sync_client' fixture is used for the guaranteed wipe_cluster() call.

    if not hasattr(elasticsearch, "AsyncElasticsearch"):
        pytest.skip("test requires 'AsyncElasticsearch' and aiohttp to be installed")

    # Unfortunately the asyncio client needs to be rebuilt every
    # test execution due to how pytest-asyncio manages
    # event loops (one per test!)
    client = None
    try:
        client = elasticsearch.AsyncElasticsearch(
            elasticsearch_url, request_timeout=3, ca_certs=CA_CERTS
        )
        yield client
    finally:
        if client:
            wipe_cluster(client)
            await client.close()

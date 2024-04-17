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

from typing import Tuple

import pytest
import pytest_asyncio

from elasticsearch import AsyncElasticsearch

from .cluster import CA_CERTS, es_url, es_version


@pytest_asyncio.fixture(scope="session")
async def elasticsearch_url():
    try:
        return await es_url()
    except RuntimeError as e:
        pytest.skip(str(e))


@pytest.fixture(scope="session")
def ca_certs():
    return CA_CERTS


@pytest_asyncio.fixture(scope="session")
async def elasticsearch_version(elasticsearch_url, ca_certs) -> Tuple[int, ...]:
    """Returns the version of the current Elasticsearch cluster"""
    return await es_version(AsyncElasticsearch(elasticsearch_url, ca_certs=ca_certs))

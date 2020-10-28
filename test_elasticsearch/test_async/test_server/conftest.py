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

import os
import pytest
import asyncio
import elasticsearch

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
async def async_client():
    client = None
    try:
        if not hasattr(elasticsearch, "AsyncElasticsearch"):
            pytest.skip("test requires 'AsyncElasticsearch'")

        kw = {
            "timeout": 30,
            "ca_certs": ".ci/certs/ca.pem",
            "connection_class": elasticsearch.AIOHttpConnection,
        }

        client = elasticsearch.AsyncElasticsearch(
            [os.environ.get("ELASTICSEARCH_HOST", {})], **kw
        )

        # wait for yellow status
        for _ in range(100):
            try:
                await client.cluster.health(wait_for_status="yellow")
                break
            except ConnectionError:
                await asyncio.sleep(0.1)
        else:
            # timeout
            pytest.skip("Elasticsearch failed to start.")

        yield client

    finally:
        if client:
            version = tuple(
                [
                    int(x) if x.isdigit() else 999
                    for x in (await client.info())["version"]["number"].split(".")
                ]
            )

            expand_wildcards = ["open", "closed"]
            if version >= (7, 7):
                expand_wildcards.append("hidden")

            await client.indices.delete(
                index="*", ignore=404, expand_wildcards=expand_wildcards
            )
            await client.indices.delete_template(name="*", ignore=404)
            await client.indices.delete_index_template(name="*", ignore=404)
            await client.close()

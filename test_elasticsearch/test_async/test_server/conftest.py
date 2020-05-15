# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

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

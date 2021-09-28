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

import io
import logging
import re

import pytest

from elasticsearch import AsyncElasticsearch, RequestError
from elasticsearch.helpers.test import CA_CERTS, ELASTICSEARCH_URL

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="function")
async def mvt_setup(async_client):
    await async_client.indices.create(
        index="museums",
        body={
            "mappings": {
                "properties": {
                    "location": {"type": "geo_point"},
                    "name": {"type": "keyword"},
                    "price": {"type": "long"},
                    "included": {"type": "boolean"},
                }
            }
        },
    )
    await async_client.bulk(
        index="museums",
        body=[
            {"index": {"_id": "1"}},
            {
                "location": "52.374081,4.912350",
                "name": "NEMO Science Museum",
                "price": 1750,
                "included": True,
            },
            {"index": {"_id": "2"}},
            {
                "location": "52.369219,4.901618",
                "name": "Museum Het Rembrandthuis",
                "price": 1500,
                "included": False,
            },
            {"index": {"_id": "3"}},
            {
                "location": "52.371667,4.914722",
                "name": "Nederlands Scheepvaartmuseum",
                "price": 1650,
                "included": True,
            },
            {"index": {"_id": "4"}},
            {
                "location": "52.371667,4.914722",
                "name": "Amsterdam Centre for Architecture",
                "price": 0,
                "included": True,
            },
        ],
        refresh=True,
    )


async def test_mapbox_vector_tile_logging(mvt_setup):
    client = AsyncElasticsearch(ELASTICSEARCH_URL, ca_certs=CA_CERTS)
    await client.info()

    output = io.StringIO()
    handler = logging.StreamHandler(output)
    logger = logging.getLogger("elasticsearch")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    try:
        await client.search_mvt(
            index="museums",
            zoom=13,
            x=4207,
            y=2692,
            field="location",
        )
    finally:
        logger.removeHandler(handler)

    handler.flush()
    logs = output.getvalue()
    print(logs)
    assert re.search(
        r"^POST https?://[^/]+/museums/_mvt/location/13/4207/2692 \[status:200 request:0\.[0-9]{3}s\]\n"
        r"> None\n"
        r"< b'.+'$",
        logs,
        flags=re.DOTALL,
    )

    output = io.StringIO()
    handler = logging.StreamHandler(output)
    logger = logging.getLogger("elasticsearch")
    logger.addHandler(handler)

    # Errors should still be JSON
    try:
        with pytest.raises(RequestError) as e:
            await client.search_mvt(
                index="museums",
                zoom=-100,
                x=4207,
                y=2692,
                field="location",
            )
    finally:
        logger.removeHandler(handler)

    assert str(e.value) == (
        "RequestError(400, 'illegal_argument_exception', "
        "'Invalid geotile_grid precision of -100. Must be between 0 and 29.')"
    )
    assert e.value.status_code == 400

    handler.flush()
    logs = output.getvalue()
    assert re.search(
        r"^POST https?://[^/]+/museums/_mvt/location/-100/4207/2692 \[status:400 request:0\.[0-9]{3}s\]\n",
        logs,
        flags=re.DOTALL,
    )

    # The JSON error body is still logged properly.
    assert logs.endswith(
        '> None\n< {"error":{"root_cause":[{"type":"illegal_argument_exception","reason":"Invalid '
        'geotile_grid precision of -100. Must be between 0 and 29."}],"type":"illegal_argument_exception",'
        '"reason":"Invalid geotile_grid precision of -100. Must be between 0 and 29."},"status":400}\n'
    )


async def test_mapbox_vector_tile_response(mvt_setup):
    try:
        import mapbox_vector_tile
    except ImportError:
        return pytest.skip(reason="Requires the 'mapbox-vector-tile' package")

    client = AsyncElasticsearch(ELASTICSEARCH_URL, ca_certs=CA_CERTS)

    resp = await client.search_mvt(
        index="museums",
        zoom=13,
        x=4207,
        y=2692,
        field="location",
        grid_precision=2,
        fields=["name", "price"],
        query={"term": {"included": True}},
        aggs={
            "min_price": {"min": {"field": "price"}},
            "max_price": {"max": {"field": "price"}},
            "avg_price": {"avg": {"field": "price"}},
        },
    )
    assert isinstance(resp, bytes)

    # Decode the binary as MVT
    tile = mapbox_vector_tile.decode(resp)

    # Assert some general things about the structure, mostly we want
    # to know that we got back a valid MVT.
    assert set(tile.keys()) == {"hits", "aggs", "meta"}

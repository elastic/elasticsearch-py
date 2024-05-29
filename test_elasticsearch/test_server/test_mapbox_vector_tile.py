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

from elasticsearch import RequestError


@pytest.fixture(scope="function")
def mvt_setup(sync_client):
    sync_client.indices.create(
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
    sync_client.bulk(
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


def test_mapbox_vector_tile_error(sync_client, mvt_setup):
    sync_client.search_mvt(
        index="museums",
        zoom=13,
        x=4207,
        y=2692,
        field="location",
    )

    with pytest.raises(RequestError) as e:
        sync_client.search_mvt(
            index="museums",
            zoom=-100,
            x=4207,
            y=2692,
            field="location",
        )

    assert str(e.value) == (
        "BadRequestError(400, 'illegal_argument_exception', "
        "'Invalid geotile_grid precision of -100. Must be between 0 and 29.')"
    )
    assert e.value.meta.status == 400
    assert e.value.status_code == 400
    assert e.value.body == {
        "error": {
            "root_cause": [
                {
                    "type": "illegal_argument_exception",
                    "reason": "Invalid geotile_grid precision of -100. Must be between 0 and 29.",
                }
            ],
            "type": "illegal_argument_exception",
            "reason": "Invalid geotile_grid precision of -100. Must be between 0 and 29.",
        },
        "status": 400,
    }


def test_mapbox_vector_tile_response(sync_client, mvt_setup):
    try:
        import mapbox_vector_tile
    except ImportError:
        return pytest.skip("Requires the 'mapbox-vector-tile' package")

    resp = sync_client.search_mvt(
        index="museums",
        zoom=13,
        x=4207,
        y=2692,
        field="location",
        body={
            "grid_precision": 2,
            "fields": ["name", "price"],
            "query": {"term": {"included": True}},
            "aggs": {
                "min_price": {"min": {"field": "price"}},
                "max_price": {"max": {"field": "price"}},
                "avg_price": {"avg": {"field": "price"}},
            },
        },
    )

    assert resp.meta.status == 200
    assert isinstance(resp.body, bytes)

    # Decode the binary as MVT
    tile = mapbox_vector_tile.decode(resp.body)

    # Assert some general things about the structure, mostly we want
    # to know that we got back a valid MVT.
    assert set(tile.keys()) == {"hits", "aggs", "meta"}

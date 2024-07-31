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

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize("kwargs", [{"body": {"text": "привет"}}, {"text": "привет"}])
async def test_indices_analyze_unicode(async_client, kwargs):
    resp = await async_client.indices.analyze(**kwargs)
    assert resp == {
        "tokens": [
            {
                "end_offset": 6,
                "position": 0,
                "start_offset": 0,
                "token": "привет",
                "type": "<ALPHANUM>",
            }
        ]
    }


async def test_bulk_works_with_string_body(async_client):
    docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
    response = await async_client.bulk(body=docs)

    assert response["errors"] is False
    assert len(response["items"]) == 1


async def test_bulk_works_with_bytestring_body(async_client):
    docs = (
        b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}'
    )
    response = await async_client.bulk(body=docs)

    assert response["errors"] is False
    assert len(response["items"]) == 1

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


@pytest.mark.parametrize("kwargs", [{"body": {"text": "привет"}}, {"text": "привет"}])
def test_indices_analyze_unicode(sync_client, kwargs):
    resp = sync_client.indices.analyze(**kwargs)
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


def test_bulk_works_with_string_body(sync_client):
    docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
    resp = sync_client.bulk(body=docs)

    assert resp["errors"] is False
    assert 1 == len(resp["items"])


def test_bulk_works_with_bytestring_body(sync_client):
    docs = (
        b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}\n'
    )
    resp = sync_client.bulk(body=docs)

    assert resp["errors"] is False
    assert 1 == len(resp["items"])

    # Pop inconsistent items before asserting
    resp["items"][0]["index"].pop("_id")
    resp["items"][0]["index"].pop("_version")
    assert resp["items"][0] == {
        "index": {
            "_index": "bulk_test_index",
            "result": "created",
            "_shards": {"total": 2, "successful": 1, "failed": 0},
            "_seq_no": 0,
            "_primary_term": 1,
            "status": 201,
        }
    }

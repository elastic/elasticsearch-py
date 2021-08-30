# -*- coding: utf-8 -*-
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

from __future__ import unicode_literals

import pytest


def test_indices_analyze_unicode(sync_client):
    resp = sync_client.indices.analyze(body='{"text": "привет"}')
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


class TestBulk:
    docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'

    @pytest.mark.parametrize("docs", [docs, docs.encode("utf-8")])
    def test_bulk_works_with_string_bytestring_body(self, docs, sync_client):
        response = sync_client.bulk(body=docs)

        assert (response["errors"]) is False
        assert len(response["items"]) == 1
        # Pop inconsistent items before asserting
        response["items"][0]["index"].pop("_id")
        response["items"][0]["index"].pop("_version")
        assert response["items"][0] == {
            "index": {
                "_index": "bulk_test_index",
                "result": "created",
                "_shards": {"total": 2, "successful": 1, "failed": 0},
                "_seq_no": 0,
                "_primary_term": 1,
                "status": 201,
            }
        }

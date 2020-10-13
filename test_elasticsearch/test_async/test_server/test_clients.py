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

pytestmark = pytest.mark.asyncio


class TestUnicode:
    async def test_indices_analyze(self, async_client):
        await async_client.indices.analyze(body='{"text": "привет"}')


class TestBulk:
    async def test_bulk_works_with_string_body(self, async_client):
        docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
        response = await async_client.bulk(body=docs)

        assert response["errors"] is False
        assert len(response["items"]) == 1

    async def test_bulk_works_with_bytestring_body(self, async_client):
        docs = b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}'
        response = await async_client.bulk(body=docs)

        assert response["errors"] is False
        assert len(response["items"]) == 1


class TestYarlMissing:
    async def test_aiohttp_connection_works_without_yarl(
        self, async_client, monkeypatch
    ):
        # This is a defensive test case for if aiohttp suddenly stops using yarl.
        from elasticsearch._async import http_aiohttp

        monkeypatch.setattr(http_aiohttp, "yarl", False)

        resp = await async_client.info(pretty=True)
        assert isinstance(resp, dict)

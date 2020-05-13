# -*- coding: utf-8 -*-
# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

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

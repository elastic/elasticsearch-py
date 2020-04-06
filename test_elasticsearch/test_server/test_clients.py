# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from . import ElasticsearchTestCase


class TestUnicode(ElasticsearchTestCase):
    def test_indices_analyze(self):
        self.client.indices.analyze(body='{"text": "привет"}')


class TestBulk(ElasticsearchTestCase):
    def test_bulk_works_with_string_body(self):
        docs = '{ "index" : { "_index" : "bulk_test_index", "_id" : "1" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))

    def test_bulk_works_with_bytestring_body(self):
        docs = b'{ "index" : { "_index" : "bulk_test_index", "_id" : "2" } }\n{"answer": 42}'
        response = self.client.bulk(body=docs)

        self.assertFalse(response["errors"])
        self.assertEqual(1, len(response["items"]))

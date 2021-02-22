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

from elasticsearch import Elasticsearch
from elasticsearch.client.utils import _make_path, _escape
from elasticsearch.compat import PY2

from ..test_cases import TestCase, SkipTest


class TestMakePath(TestCase):
    def test_handles_unicode(self):
        id = "中文"
        self.assertEquals(
            "/some-index/type/%E4%B8%AD%E6%96%87", _make_path("some-index", "type", id)
        )

    def test_handles_utf_encoded_string(self):
        if not PY2:
            raise SkipTest("Only relevant for py2")
        id = "中文".encode("utf-8")
        self.assertEquals(
            "/some-index/type/%E4%B8%AD%E6%96%87", _make_path("some-index", "type", id)
        )

    def test_handles_whitespace_character(self):
        self.assertEquals(
            "/path/%20with/%20/a%20space", _make_path("path", " with", " ", "a space")
        )


class TestEscape(TestCase):
    def test_handles_ascii(self):
        string = "abc123"
        self.assertEquals(b"abc123", _escape(string))

    def test_handles_unicode(self):
        string = "中文"
        self.assertEquals(b"\xe4\xb8\xad\xe6\x96\x87", _escape(string))

    def test_handles_bytestring(self):
        string = b"celery-task-meta-c4f1201f-eb7b-41d5-9318-a75a8cfbdaa0"
        self.assertEquals(string, _escape(string))


class TestBulkBody(TestCase):
    def test_proper_bulk_body_as_string_is_not_modified(self):
        es = Elasticsearch()
        string_body = '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n'
        self.assertEqual(string_body, es._bulk_body(string_body))

    def test_proper_bulk_body_as_bytestring_is_not_modified(self):
        es = Elasticsearch()
        bytestring_body = b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n'
        self.assertEqual(bytestring_body, es._bulk_body(bytestring_body))

    def test_bulk_body_as_string_adds_trailing_newline(self):
        es = Elasticsearch()
        string_body = '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"'
        self.assertEqual(
            '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n',
            es._bulk_body(string_body),
        )

    def test_bulk_body_as_bytestring_adds_trailing_newline(self):
        es = Elasticsearch()
        bytestring_body = b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"'
        self.assertEqual(
            b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n',
            es._bulk_body(bytestring_body),
        )

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

from elasticsearch.client.utils import _bulk_body, _escape, _make_path, query_params
from elasticsearch.compat import PY2

from ..test_cases import SkipTest, TestCase


class TestQueryParams(TestCase):
    def setup_method(self, _):
        self.calls = []

    @query_params("simple_param")
    def func_to_wrap(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    def test_handles_params(self):
        self.func_to_wrap(params={"simple_param_2": "2"}, simple_param="3")
        self.assertEqual(
            self.calls,
            [
                (
                    (),
                    {
                        "params": {"simple_param": b"3", "simple_param_2": "2"},
                        "headers": {},
                    },
                )
            ],
        )

    def test_handles_headers(self):
        self.func_to_wrap(headers={"X-Opaque-Id": "app-1"})
        self.assertEqual(
            self.calls, [((), {"params": {}, "headers": {"x-opaque-id": "app-1"}})]
        )

    def test_handles_opaque_id(self):
        self.func_to_wrap(opaque_id="request-id")
        self.assertEqual(
            self.calls, [((), {"params": {}, "headers": {"x-opaque-id": "request-id"}})]
        )

    def test_handles_empty_none_and_normalization(self):
        self.func_to_wrap(params=None)
        self.assertEqual(self.calls[-1], ((), {"params": {}, "headers": {}}))

        self.func_to_wrap(headers=None)
        self.assertEqual(self.calls[-1], ((), {"params": {}, "headers": {}}))

        self.func_to_wrap(headers=None, params=None)
        self.assertEqual(self.calls[-1], ((), {"params": {}, "headers": {}}))

        self.func_to_wrap(headers={}, params={})
        self.assertEqual(self.calls[-1], ((), {"params": {}, "headers": {}}))

        self.func_to_wrap(headers={"X": "y"})
        self.assertEqual(self.calls[-1], ((), {"params": {}, "headers": {"x": "y"}}))

    def test_per_call_authentication(self):
        self.func_to_wrap(api_key=("name", "key"))
        self.assertEqual(
            self.calls[-1],
            ((), {"headers": {"authorization": "ApiKey bmFtZTprZXk="}, "params": {}}),
        )

        self.func_to_wrap(http_auth=("user", "password"))
        self.assertEqual(
            self.calls[-1],
            (
                (),
                {
                    "headers": {"authorization": "Basic dXNlcjpwYXNzd29yZA=="},
                    "params": {},
                },
            ),
        )

        self.func_to_wrap(http_auth="abcdef")
        self.assertEqual(
            self.calls[-1],
            ((), {"headers": {"authorization": "Basic abcdef"}, "params": {}}),
        )

        # If one or the other is 'None' it's all good!
        self.func_to_wrap(http_auth=None, api_key=None)
        self.assertEqual(self.calls[-1], ((), {"headers": {}, "params": {}}))

        self.func_to_wrap(http_auth="abcdef", api_key=None)
        self.assertEqual(
            self.calls[-1],
            ((), {"headers": {"authorization": "Basic abcdef"}, "params": {}}),
        )

        # If both are given values an error is raised.
        with self.assertRaises(ValueError) as e:
            self.func_to_wrap(http_auth="key", api_key=("1", "2"))
        self.assertEqual(
            str(e.exception),
            "Only one of 'http_auth' and 'api_key' may be passed at a time",
        )


class TestMakePath(TestCase):
    def test_handles_unicode(self):
        id = "中文"
        self.assertEqual(
            "/some-index/type/%E4%B8%AD%E6%96%87", _make_path("some-index", "type", id)
        )

    def test_handles_utf_encoded_string(self):
        if not PY2:
            raise SkipTest("Only relevant for py2")
        id = "中文".encode("utf-8")
        self.assertEqual(
            "/some-index/type/%E4%B8%AD%E6%96%87", _make_path("some-index", "type", id)
        )


class TestEscape(TestCase):
    def test_handles_ascii(self):
        string = "abc123"
        self.assertEqual(b"abc123", _escape(string))

    def test_handles_unicode(self):
        string = "中文"
        self.assertEqual(b"\xe4\xb8\xad\xe6\x96\x87", _escape(string))

    def test_handles_bytestring(self):
        string = b"celery-task-meta-c4f1201f-eb7b-41d5-9318-a75a8cfbdaa0"
        self.assertEqual(string, _escape(string))


class TestBulkBody(TestCase):
    def test_proper_bulk_body_as_string_is_not_modified(self):
        string_body = '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n'
        self.assertEqual(string_body, _bulk_body(None, string_body))

    def test_proper_bulk_body_as_bytestring_is_not_modified(self):
        bytestring_body = b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n'
        self.assertEqual(bytestring_body, _bulk_body(None, bytestring_body))

    def test_bulk_body_as_string_adds_trailing_newline(self):
        string_body = '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"'
        self.assertEqual(
            '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n',
            _bulk_body(None, string_body),
        )

    def test_bulk_body_as_bytestring_adds_trailing_newline(self):
        bytestring_body = b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"'
        self.assertEqual(
            b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n',
            _bulk_body(None, bytestring_body),
        )

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

from elasticsearch.client.utils import _bulk_body, _escape, _make_path, query_params
from elasticsearch.compat import PY2


class TestQueryParams:
    def setup_method(self, _):
        self.calls = []

    @query_params("simple_param")
    def func_to_wrap(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    def test_handles_params(self):
        self.func_to_wrap(params={"simple_param_2": "2"}, simple_param="3")
        assert self.calls == [
            (
                (),
                {
                    "params": {"simple_param": b"3", "simple_param_2": "2"},
                    "headers": {},
                },
            )
        ]

    def test_handles_headers(self):
        self.func_to_wrap(headers={"X-Opaque-Id": "app-1"})
        assert self.calls == [((), {"params": {}, "headers": {"x-opaque-id": "app-1"}})]

    def test_handles_opaque_id(self):
        self.func_to_wrap(opaque_id="request-id")
        assert self.calls == [
            ((), {"params": {}, "headers": {"x-opaque-id": "request-id"}})
        ]

    def test_handles_empty_none_and_normalization(self):
        self.func_to_wrap(params=None)
        assert self.calls[-1] == ((), {"params": {}, "headers": {}})

        self.func_to_wrap(headers=None)
        assert self.calls[-1] == ((), {"params": {}, "headers": {}})

        self.func_to_wrap(headers=None, params=None)
        assert self.calls[-1] == ((), {"params": {}, "headers": {}})

        self.func_to_wrap(headers={}, params={})
        assert self.calls[-1] == ((), {"params": {}, "headers": {}})

        self.func_to_wrap(headers={"X": "y"})
        assert self.calls[-1] == ((), {"params": {}, "headers": {"x": "y"}})

    def test_per_call_authentication(self):
        self.func_to_wrap(api_key=("name", "key"))
        assert self.calls[-1] == (
            (),
            {"headers": {"authorization": "ApiKey bmFtZTprZXk="}, "params": {}},
        )

        self.func_to_wrap(http_auth=("user", "password"))
        assert self.calls[-1] == (
            (),
            {
                "headers": {"authorization": "Basic dXNlcjpwYXNzd29yZA=="},
                "params": {},
            },
        )

        self.func_to_wrap(http_auth="abcdef")
        assert self.calls[-1] == (
            (),
            {"headers": {"authorization": "Basic abcdef"}, "params": {}},
        )

        # If one or the other is 'None' it's all good!
        self.func_to_wrap(http_auth=None, api_key=None)
        assert self.calls[-1] == ((), {"headers": {}, "params": {}})

        self.func_to_wrap(http_auth="abcdef", api_key=None)
        assert self.calls[-1] == (
            (),
            {"headers": {"authorization": "Basic abcdef"}, "params": {}},
        )

        # If both are given values an error is raised.
        with pytest.raises(ValueError) as e:
            self.func_to_wrap(http_auth="key", api_key=("1", "2"))
        assert (
            str(e.value)
            == "Only one of 'http_auth' and 'api_key' may be passed at a time"
        )


class TestMakePath:
    def test_handles_unicode(self):
        id = "中文"
        assert "/some-index/type/%E4%B8%AD%E6%96%87" == _make_path(
            "some-index", "type", id
        )

    @pytest.mark.skipif(not PY2, reason="Only relevant for Python 2")
    def test_handles_utf_encoded_string(self):
        id = "中文".encode("utf-8")
        assert "/some-index/type/%E4%B8%AD%E6%96%87" == _make_path(
            "some-index", "type", id
        )


class TestEscape:
    def test_handles_ascii(self):
        string = "abc123"
        assert b"abc123" == _escape(string)

    def test_handles_unicode(self):
        string = "中文"
        assert b"\xe4\xb8\xad\xe6\x96\x87" == _escape(string)

    def test_handles_bytestring(self):
        string = b"celery-task-meta-c4f1201f-eb7b-41d5-9318-a75a8cfbdaa0"
        assert string == _escape(string)


class TestBulkBody:
    def test_proper_bulk_body_as_string_is_not_modified(self):
        string_body = '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n'
        assert string_body == _bulk_body(None, string_body)

    def test_proper_bulk_body_as_bytestring_is_not_modified(self):
        bytestring_body = b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n'
        assert bytestring_body == _bulk_body(None, bytestring_body)

    def test_bulk_body_as_string_adds_trailing_newline(self):
        string_body = '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"'
        assert '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n' == _bulk_body(
            None, string_body
        )

    def test_bulk_body_as_bytestring_adds_trailing_newline(self):
        bytestring_body = b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"'
        assert (
            b'"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"\n'
            == _bulk_body(None, bytestring_body)
        )

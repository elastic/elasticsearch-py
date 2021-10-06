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

import os
import warnings

import pytest

from elasticsearch.client.utils import _bulk_body, _escape, _make_path, query_params
from elasticsearch.compat import PY2

from ..test_cases import SkipTest, TestCase


class TestQueryParams(TestCase):
    def setup_method(self, _):
        self.calls = []

    @query_params("simple_param")
    def func_to_wrap(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    @query_params(
        "query_only",
        "query_and_body",
        body_params=["query_and_body", "body_only", "from_"],
    )
    def func_with_body_params(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    @query_params(
        "query_only",
        "query_and_body",
        body_params=["query_and_body", "body_only"],
        body_required=True,
    )
    def func_with_body_params_required(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    @query_params("query_only", body_name="named_body")
    def func_with_named_body(self, *args, **kwargs):
        self.calls.append((args, kwargs))

    @query_params(
        request_mimetypes=["application/json"],
        response_mimetypes=["text/plain", "application/json"],
    )
    def func_with_mimetypes(self, *args, **kwargs):
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

    def test_body_params(self):
        with warnings.catch_warnings(record=True) as w:
            # No params, should be same as an empty call
            self.func_with_body_params()
            assert self.calls[-1] == ((), {"headers": {}, "params": {}})

            # No overlap with 'body_params'
            self.func_with_body_params(query_only=1)
            assert self.calls[-1] == (
                (),
                {"headers": {}, "params": {"query_only": "1"}},
            )

            # One body parameter
            self.func_with_body_params(query_and_body=1)
            assert self.calls[-1] == (
                (),
                {"body": {"query_and_body": 1}, "headers": {}, "params": {}},
            )
            self.func_with_body_params(body_only=1)
            assert self.calls[-1] == (
                (),
                {"body": {"body_only": 1}, "headers": {}, "params": {}},
            )

            # Multiple body field parameters
            self.func_with_body_params(query_and_body=1, body_only=1)
            assert self.calls[-1] == (
                (),
                {
                    "body": {"query_and_body": 1, "body_only": 1},
                    "headers": {},
                    "params": {},
                },
            )

            # All the parameters
            self.func_with_body_params(query_only=1, query_and_body=1, body_only=1)
            assert self.calls[-1] == (
                (),
                {
                    "body": {"query_and_body": 1, "body_only": 1},
                    "headers": {},
                    "params": {"query_only": "1"},
                },
            )

        # There should be no 'DeprecationWarnings'
        # emitted for any of the above cases.
        assert w == []

        # Positional arguments pass-through
        self.func_with_body_params(1)
        assert self.calls[-1] == (
            (1,),
            {"headers": {}, "params": {}},
        )

        # Positional arguments disable body serialization
        self.func_with_body_params(1, query_and_body=1)
        assert self.calls[-1] == (
            (1,),
            {"headers": {}, "params": {"query_and_body": "1"}},
        )

    def test_body_params_errors(self):
        with pytest.raises(TypeError) as e:
            self.func_with_body_params(body={}, body_only=True)
        assert str(e.value) == (
            "The 'body_only' parameter is only serialized in the request body "
            "and can't be combined with the 'body' parameter. Either stop using "
            "the 'body' parameter and use keyword-arguments only or move the "
            "specified parameters into the 'body'. "
            "See https://github.com/elastic/elasticsearch-py/issues/1698 for more information"
        )

        # Positional arguments disable body serialization
        with pytest.raises(TypeError) as e:
            self.func_with_body_params(1, body_only=1)
        assert str(e.value) == (
            "The 'body_only' parameter is only serialized in the request body "
            "and can't be combined with the 'body' parameter. Either stop using "
            "the 'body' parameter and use keyword-arguments only or move the "
            "specified parameters into the 'body'. "
            "See https://github.com/elastic/elasticsearch-py/issues/1698 for more information"
        )

    def test_body_params_deprecations(self):
        # APIs with body_params deprecate the 'body' parameter.
        with pytest.warns(DeprecationWarning) as w:
            self.func_with_body_params(body={})

        assert self.calls[-1] == ((), {"body": {}, "headers": {}, "params": {}})
        assert len(w) == 1
        assert w[0].category == DeprecationWarning
        assert str(w[0].message) == (
            "The 'body' parameter is deprecated for the "
            "'func_with_body_params' API and will be removed in a future version. "
            "Instead use API parameters directly. "
            "See https://github.com/elastic/elasticsearch-py/issues/1698 for more information"
        )

        # APIs that don't have body parameters don't have a deprecated 'body' parameter
        with warnings.catch_warnings(record=True) as w:
            self.func_to_wrap(body={})

        assert self.calls[-1] == ((), {"body": {}, "headers": {}, "params": {}})
        assert w == []

        # Positional arguments are deprecated for all APIs
        with pytest.warns(DeprecationWarning) as w:
            self.func_to_wrap(1)

        assert self.calls[-1] == ((1,), {"headers": {}, "params": {}})
        assert len(w) == 1
        assert w[0].category == DeprecationWarning
        assert str(w[0].message) == (
            "Using positional arguments for APIs is deprecated and will be disabled in "
            "8.0.0. Instead use only keyword arguments for all APIs. See https://github.com/"
            "elastic/elasticsearch-py/issues/1698 for more information"
        )

    def test_body_params_removes_underscore_suffix(self):
        self.func_with_body_params(from_=0)
        assert self.calls[-1] == (
            (),
            {"body": {"from": 0}, "headers": {}, "params": {}},
        )

    def test_named_body_params(self):
        # Passing 'named_body' results in no error or warning
        with warnings.catch_warnings(record=True) as w:
            self.func_with_named_body(named_body=[])

        assert self.calls[-1] == ((), {"body": [], "headers": {}, "params": {}})
        assert w == []

        # Passing 'body' is a warning but works
        with warnings.catch_warnings(record=True) as w:
            self.func_with_named_body(body=[])

        assert self.calls[-1] == ((), {"body": [], "headers": {}, "params": {}})
        assert len(w) == 1
        assert str(w[0].message) == (
            "The 'body' parameter is deprecated for the 'func_with_named_body' "
            "API and will be removed in a future version. Instead use the 'named_body' parameter. "
            "See https://github.com/elastic/elasticsearch-py/issues/1698 for more information"
        )

        # Passing both 'named_body' and 'body' is an error
        self.calls[:] = []
        with warnings.catch_warnings(record=True) as w:
            with pytest.raises(TypeError) as e:
                self.func_with_named_body(named_body=[], body=[])

        assert self.calls == []
        assert w == []
        assert str(e.value) == (
            "Can't use 'named_body' and 'body' parameters together because 'named_body' "
            "is an alias for 'body'. Instead you should only use the 'named_body' parameter. "
            "See https://github.com/elastic/elasticsearch-py/issues/1698 for more information"
        )

        # Positional arguments aren't impacted. Only warning is for positional args
        with warnings.catch_warnings(record=True) as w:
            self.func_with_named_body([])

        assert self.calls == [(([],), {"headers": {}, "params": {}})]
        assert len(w) == 1
        assert str(w[0].message) == (
            "Using positional arguments for APIs is deprecated and will be disabled in "
            "8.0.0. Instead use only keyword arguments for all APIs. "
            "See https://github.com/elastic/elasticsearch-py/issues/1698 for more information"
        )

    def test_body_required_with_body_fields(self):
        self.func_with_body_params_required(query_only=True)
        assert self.calls[-1] == (
            (),
            {"body": {}, "headers": {}, "params": {"query_only": b"true"}},
        )

        self.func_with_body_params_required(body_only=True)
        assert self.calls[-1] == (
            (),
            {"body": {"body_only": True}, "headers": {}, "params": {}},
        )

        self.func_with_body_params_required(query_and_body=True)
        assert self.calls[-1] == (
            (),
            {"body": {"query_and_body": True}, "headers": {}, "params": {}},
        )

        self.func_with_body_params_required(body={})
        assert self.calls[-1] == ((), {"body": {}, "headers": {}, "params": {}})

        self.func_with_body_params_required(body={"hello": "world"})
        assert self.calls[-1] == (
            (),
            {"body": {"hello": "world"}, "headers": {}, "params": {}},
        )

        self.func_with_body_params_required()
        assert self.calls[-1] == ((), {"body": {}, "headers": {}, "params": {}})

    def test_mimetype_headers(self):
        compat_envvar = os.environ.pop("ELASTIC_CLIENT_APIVERSIONING", None)
        try:
            self.func_with_mimetypes()
            assert self.calls[-1] == (
                (),
                {
                    "headers": {
                        "accept": "text/plain,application/json",
                        "content-type": "application/json",
                    },
                    "params": {},
                },
            )

            self.func_with_mimetypes(headers={})
            assert self.calls[-1] == (
                (),
                {
                    "headers": {
                        "accept": "text/plain,application/json",
                        "content-type": "application/json",
                    },
                    "params": {},
                },
            )

            self.func_with_mimetypes(
                headers={
                    "Content-Type": "application/x-octet-stream",
                    "AccepT": "application/x-octet-stream",
                }
            )
            assert self.calls[-1] == (
                (),
                {
                    "headers": {
                        "accept": "application/x-octet-stream",
                        "content-type": "application/x-octet-stream",
                    },
                    "params": {},
                },
            )

        finally:
            if compat_envvar:
                os.environ["ELASTIC_CLIENT_APIVERSIONING"] = compat_envvar

    def test_mimetype_headers_compatibility_mode(self):
        compat_envvar = os.environ.pop("ELASTIC_CLIENT_APIVERSIONING", None)
        try:
            for compat_mode_enabled in ["true", "1"]:
                os.environ["ELASTIC_CLIENT_APIVERSIONING"] = compat_mode_enabled

                self.func_with_mimetypes()
                assert self.calls[-1] == (
                    (),
                    {
                        "headers": {
                            "accept": "text/plain,application/vnd.elasticsearch+json;compatible-with=7",
                            "content-type": "application/vnd.elasticsearch+json;compatible-with=7",
                        },
                        "params": {},
                    },
                )

                self.func_with_mimetypes(headers={"Content-Type": "text/plain"})
                assert self.calls[-1] == (
                    (),
                    {
                        "headers": {
                            "accept": "text/plain,application/vnd.elasticsearch+json;compatible-with=7",
                            "content-type": "text/plain",
                        },
                        "params": {},
                    },
                )
        finally:
            if compat_envvar:
                os.environ["ELASTIC_CLIENT_APIVERSIONING"] = compat_envvar


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

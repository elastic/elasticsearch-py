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

from elasticsearch.client import _normalize_hosts
from elasticsearch.client.utils import _bulk_body, _escape, _make_path, query_params


class TestNormalizeHosts:
    def test_none_uses_defaults(self):
        assert [{}] == _normalize_hosts(None)

    def test_strings_are_used_as_hostnames(self):
        assert [{"host": "elastic.co"}] == _normalize_hosts(["elastic.co"])

    def test_strings_are_parsed_for_port_and_user(self):
        assert [
            {"host": "elastic.co", "port": 42},
            {"host": "elastic.co", "http_auth": "user:secre]"},
        ] == _normalize_hosts(["elastic.co:42", "user:secre%5D@elastic.co"])

    def test_strings_are_parsed_for_scheme(self):
        assert [
            {"host": "elastic.co", "port": 42, "use_ssl": True},
            {
                "host": "elastic.co",
                "http_auth": "user:secret",
                "use_ssl": True,
                "port": 443,
                "url_prefix": "/prefix",
            },
        ] == _normalize_hosts(
            ["https://elastic.co:42", "https://user:secret@elastic.co/prefix"]
        )

    def test_dicts_are_left_unchanged(self):
        assert [{"host": "local", "extra": 123}] == _normalize_hosts(
            [{"host": "local", "extra": 123}]
        )

    def test_single_string_is_wrapped_in_list(self):
        assert [{"host": "elastic.co"}] == _normalize_hosts("elastic.co")


class TestQueryParams:
    calls = []

    @query_params("simple_param")
    def func_to_wrap(self, *args, **kwargs):
        self.calls = []
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
        with pytest.raises(
            ValueError,
            match="Only one of 'http_auth' and 'api_key' may be passed at a time",
        ):
            self.func_to_wrap(http_auth="key", api_key=("1", "2"))


class TestMakePath:
    id = "中文"

    @pytest.mark.parametrize("id", [id, id.encode("utf-8")])
    def test_handles_unicode(self, id):
        assert "/some-index/type/%E4%B8%AD%E6%96%87" == _make_path(
            "some-index", "type", id
        )


class TestEscape:
    @pytest.mark.parametrize(
        ["left", "right"],
        [
            ("abc123", b"abc123"),
            ("中文", b"\xe4\xb8\xad\xe6\x96\x87"),
            (
                b"celery-task-meta-c4f1201f-eb7b-41d5-9318-a75a8cfbdaa0",
                b"celery-task-meta-c4f1201f-eb7b-41d5-9318-a75a8cfbdaa0",
            ),
        ],
    )
    def test_handles_ascii_unicode_bytestring(self, left, right):
        assert right == _escape(left)


class TestBulkBody:
    id = '"{"index":{ "_index" : "test"}}\n{"field1": "value1"}"'
    id_newline = id + "\n"

    @pytest.mark.parametrize(
        ["left", "right"],
        [
            (id_newline, id_newline),
            (id_newline.encode("utf-8"), id_newline.encode("utf-8")),
            (id_newline, id),
            (id_newline.encode("utf-8"), id.encode("utf-8")),
        ],
    )
    def test_proper_bulk_string_bytestring(self, left, right):
        assert left == _bulk_body(None, right)

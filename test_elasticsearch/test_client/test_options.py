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

import pytest

from elasticsearch import Elasticsearch
from test_elasticsearch.test_cases import DummyTransport, DummyTransportTestCase


class TestOptions(DummyTransportTestCase):
    def assert_called_with_headers(self, client, method, target, headers):
        calls = client.transport.calls
        assert (method, target) in calls
        called_headers = calls[(method, target)][-1]["headers"].copy()
        for header in (
            "accept",
            "content-type",
        ):  # Common HTTP headers that we're not testing.
            called_headers.pop(header, None)
        assert headers == called_headers

    @pytest.mark.parametrize(
        ["options", "headers"],
        [
            (
                {"headers": {"authorization": "custom method"}},
                {"Authorization": "custom method"},
            ),
            ({"api_key": "key"}, {"Authorization": "ApiKey key"}),
            ({"api_key": ("id", "value")}, {"Authorization": "ApiKey aWQ6dmFsdWU="}),
            (
                {"basic_auth": ("username", "password")},
                {"Authorization": "Basic dXNlcm5hbWU6cGFzc3dvcmQ="},
            ),
            ({"basic_auth": "encoded"}, {"Authorization": "Basic encoded"}),
            ({"bearer_auth": "bear"}, {"Authorization": "Bearer bear"}),
            (
                {"opaque_id": "test-id"},
                {"X-Opaque-Id": "test-id"},
            ),
            (
                {
                    "opaque_id": "opaq-id",
                    "headers": {"custom": "key"},
                    "api_key": ("id", "val"),
                },
                {
                    "custom": "key",
                    "authorization": "ApiKey aWQ6dmFs",
                    "x-opaque-id": "opaq-id",
                },
            ),
        ],
    )
    def test_options_to_headers(self, options, headers):
        # Tests that authentication works identically from the constructor
        # or from the client.options() API.
        client = self.client.options(**options)
        client.indices.exists(index="test")
        self.assert_called_with_headers(client, "HEAD", "/test", headers=headers)

        client = Elasticsearch(
            "http://localhost:9200", transport_class=DummyTransport, **options
        )
        client.indices.exists(index="test")
        self.assert_called_with_headers(client, "HEAD", "/test", headers=headers)

        client = Elasticsearch(
            "http://localhost:9200",
            transport_class=DummyTransport,
            headers={"Authorization": "not it"},
        )
        client = self.client.options(**options)
        client.indices.exists(index="test")
        self.assert_called_with_headers(client, "HEAD", "/test", headers=headers)

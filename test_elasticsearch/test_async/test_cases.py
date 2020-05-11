# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from collections import defaultdict
from unittest import SkipTest  # noqa: F401
import elasticsearch
from ..test_cases import ElasticsearchTestCase


class AsyncDummyTransport(object):
    def __init__(self, hosts, responses=None, **kwargs):
        self.hosts = hosts
        self.responses = responses
        self.call_count = 0
        self.calls = defaultdict(list)

    async def perform_request(self, method, url, params=None, headers=None, body=None):
        resp = 200, {}
        if self.responses:
            resp = self.responses[self.call_count]
        self.call_count += 1
        self.calls[(method, url)].append((params, headers, body))
        return resp


class AsyncElasticsearchTestCase(ElasticsearchTestCase):
    def setup_method(self, _):
        if not hasattr(elasticsearch, "AsyncElasticsearch"):
            raise SkipTest("This test case requires 'AsyncElasticsearch'")
        self.client = elasticsearch.AsyncElasticsearch(
            transport_class=AsyncDummyTransport
        )

    def assert_call_count_equals(self, count):
        self.assertEqual(count, self.client.transport.call_count)

    def assert_url_called(self, method, url, count=1):
        self.assertIn((method, url), self.client.transport.calls)
        calls = self.client.transport.calls[(method, url)]
        self.assertEqual(count, len(calls))
        return calls


class TestAsyncElasticsearchTestCase(AsyncElasticsearchTestCase):
    def test_our_transport_used(self):
        self.assertIsInstance(self.client.transport, AsyncDummyTransport)

    def test_start_with_0_call(self):
        self.assert_call_count_equals(0)

    async def test_each_call_is_recorded(self):
        await self.client.transport.perform_request("GET", "/")
        await self.client.transport.perform_request(
            "DELETE", "/42", params={}, body="body"
        )
        self.assert_call_count_equals(2)
        self.assertEqual(
            [({}, None, "body")], self.assert_url_called("DELETE", "/42", 1)
        )

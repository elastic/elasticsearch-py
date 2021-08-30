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

from elasticsearch.client import Elasticsearch

from .common import DummyTransport, assert_helper


class TestClient:
    def test_request_timeout_is_passed_through_unescaped(self):
        client = Elasticsearch(transport_class=DummyTransport)
        client.ping(request_timeout=0.1)
        calls = assert_helper(client, "HEAD", "/")
        assert [({"request_timeout": 0.1}, {}, None)] == calls

    def test_params_is_copied_when(self):
        client = Elasticsearch(transport_class=DummyTransport)
        params = {"request_timeout": object()}
        client.ping(params=params)
        client.ping(params=params)
        calls = assert_helper(client, "HEAD", "/", 2)
        assert [(params, {}, None), (params, {}, None)] == calls
        assert calls[0][0] is not calls[1][0]

    def test_headers_is_copied_when(self):
        client = Elasticsearch(transport_class=DummyTransport)
        headers = {"authentication": "value"}
        client.ping(headers=headers)
        client.ping(headers=headers)
        calls = assert_helper(client, "HEAD", "/", 2)
        assert [({}, headers, None), ({}, headers, None)] == calls
        assert calls[0][0] is not calls[1][0]

    def test_from_in_search(self):
        client = Elasticsearch(transport_class=DummyTransport)
        client.search(index="i", from_=10)
        calls = assert_helper(client, "POST", "/i/_search")
        assert [({"from": b"10"}, {}, None)] == calls

    def test_repr_contains_hosts(self):
        client = Elasticsearch(transport_class=DummyTransport)
        assert "<Elasticsearch([{}])>" == repr(client)

    def test_repr_subclass(self):
        class OtherElasticsearch(Elasticsearch):
            pass

        assert "<OtherElasticsearch([{}])>" == repr(OtherElasticsearch())

    def test_repr_contains_hosts_passed_in(self):
        assert "es.org" in repr(Elasticsearch(["es.org:123"]))

    def test_repr_truncates_host_to_5(self):
        hosts = [{"host": "es" + str(i)} for i in range(10)]
        es = Elasticsearch(hosts)
        assert '{"host": "es5"}' not in repr(es)
        assert "..." in repr(es)

    @pytest.mark.parametrize(
        ["id", "request_method", "url"],
        [("", "POST", "/my-index/_doc"), (0, "PUT", "/my-index/_doc/0")],
    )
    def test_index_uses_id(self, id, request_method, url):
        client = Elasticsearch(transport_class=DummyTransport)
        client.index(index="my-index", id=id, body={})

        assert_helper(client, request_method, url)

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

from ..test_cases import DummyTransportTestCase


class TestClient(DummyTransportTestCase):
    def test_request_timeout_is_passed_through_unescaped(self):
        self.client.ping(request_timeout=0.1)
        calls = self.assert_url_called("HEAD", "/")
        assert [({"request_timeout": 0.1}, {}, None)] == calls

    def test_params_is_copied_when(self):
        rt = object()
        params = dict(request_timeout=rt)
        self.client.ping(params=params)
        self.client.ping(params=params)
        calls = self.assert_url_called("HEAD", "/", 2)
        assert [
            ({"request_timeout": rt}, {}, None),
            ({"request_timeout": rt}, {}, None),
        ] == calls
        assert not (calls[0][0] is calls[1][0])

    def test_headers_is_copied_when(self):
        hv = "value"
        headers = dict(Authentication=hv)
        self.client.ping(headers=headers)
        self.client.ping(headers=headers)
        calls = self.assert_url_called("HEAD", "/", 2)
        assert [
            ({}, {"authentication": hv}, None),
            ({}, {"authentication": hv}, None),
        ] == calls
        assert not (calls[0][0] is calls[1][0])

    def test_from_in_search(self):
        self.client.search(index="i", from_=10)
        calls = self.assert_url_called("POST", "/i/_search")
        assert [({"from": "10"}, {}, None)] == calls

    def test_repr_contains_hosts(self):
        assert "<Elasticsearch([{}])>" == repr(self.client)

    def test_repr_subclass(self):
        class OtherElasticsearch(Elasticsearch):
            pass

        assert "<OtherElasticsearch([{}])>" == repr(OtherElasticsearch())

    def test_repr_contains_hosts_passed_in(self):
        assert "es.org" in repr(Elasticsearch(["es.org:123"]))

    def test_repr_truncates_host_to_5(self):
        hosts = [{"host": "es" + str(i)} for i in range(10)]
        es = Elasticsearch(hosts)
        assert "es5" not in repr(es)
        assert "..." in repr(es)

    def test_index_uses_post_if_id_is_empty(self):
        self.client.index(index="my-index", id="", body={})

        self.assert_url_called("POST", "/my-index/_doc")

    def test_index_uses_put_if_id_is_not_empty(self):
        self.client.index(index="my-index", id=0, body={})

        self.assert_url_called("PUT", "/my-index/_doc/0")

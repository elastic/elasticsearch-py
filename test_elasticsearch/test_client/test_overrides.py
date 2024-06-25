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

from ..test_cases import DummyTransportTestCase


class TestOverriddenUrlTargets(DummyTransportTestCase):
    def test_create(self):
        self.client.create(index="test-index", id="test-id", body={})
        self.assert_url_called("PUT", "/test-index/_create/test-id")

    def test_delete(self):
        self.client.delete(index="test-index", id="test-id")
        self.assert_url_called("DELETE", "/test-index/_doc/test-id")

    def test_index(self):
        self.client.index(index="test-index", document={})
        self.assert_url_called("POST", "/test-index/_doc")

        self.client.index(index="test-index", id="test-id", document={})
        self.assert_url_called("PUT", "/test-index/_doc/test-id")

    def test_update(self):
        self.client.update(index="test-index", id="test-id", body={})
        self.assert_url_called("POST", "/test-index/_update/test-id")

    def test_cluster_state(self):
        self.client.cluster.state()
        self.assert_url_called("GET", "/_cluster/state")

        self.client.cluster.state(index="test-index")
        self.assert_url_called("GET", "/_cluster/state/_all/test-index")

        self.client.cluster.state(index="test-index", metric="test-metric")
        self.assert_url_called("GET", "/_cluster/state/test-metric/test-index")

    def test_cluster_stats(self):
        self.client.cluster.stats()
        self.assert_url_called("GET", "/_cluster/stats")

        self.client.cluster.stats(node_id="test-node")
        self.assert_url_called("GET", "/_cluster/stats/nodes/test-node")

    def test_index_uses_post_if_id_is_empty(self):
        self.client.index(index="my-index", id="", document={})
        self.assert_url_called("POST", "/my-index/_doc")

    def test_index_uses_put_if_id_is_not_empty(self):
        self.client.index(index="my-index", id=0, document={})
        self.assert_url_called("PUT", "/my-index/_doc/0")

    @pytest.mark.parametrize("param_name", ["from", "from_"])
    def test_from_in_search(self, param_name):
        self.client.search(index="i", **{param_name: 10})
        calls = self.assert_url_called("POST", "/i/_search")
        assert calls[0]["body"] == {"from": 10}

    def test_sort_in_search(self):
        self.client.search(index="i", sort="@timestamp:asc")
        calls = self.assert_url_called("POST", "/i/_search?sort=%40timestamp%3Aasc")
        assert calls[0]["body"] is None

        self.client.search(index="i", sort=["@timestamp:asc", "field"])
        calls = self.assert_url_called(
            "POST", "/i/_search?sort=%40timestamp%3Aasc,field"
        )
        assert calls[0]["body"] is None

        self.client.search(index="i", sort=("field", "@timestamp:asc"))
        calls = self.assert_url_called(
            "POST", "/i/_search?sort=field,%40timestamp%3Aasc"
        )
        assert calls[0]["body"] is None

        self.client.search(index="i", sort=("field", "@timestamp"))
        calls = self.assert_url_called("POST", "/i/_search")
        assert calls[-1]["body"] == {"sort": ("field", "@timestamp")}

        self.client.search(index="i2", sort=["@timestamp", "field"])
        calls = self.assert_url_called("POST", "/i2/_search")
        assert calls[-1]["body"] == {"sort": ["@timestamp", "field"]}

        self.client.search(
            index="i3", sort=("field", "@timestamp:asc", {"field": "desc"})
        )
        calls = self.assert_url_called("POST", "/i3/_search")
        assert calls[-1]["body"] == {
            "sort": ("field", "@timestamp:asc", {"field": "desc"})
        }

        self.client.search(index="i4", sort=["@timestamp:asc", {"field": "desc"}])
        calls = self.assert_url_called("POST", "/i4/_search")
        assert calls[-1]["body"] == {"sort": ["@timestamp:asc", {"field": "desc"}]}

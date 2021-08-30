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


class TestCluster:
    @pytest.mark.parametrize("node_id", [None, "node-1", "node-2"])
    def test_stats_node_id(self, node_id):
        client = Elasticsearch(transport_class=DummyTransport)
        client.cluster.stats(node_id=node_id)
        url = "/_cluster/stats"
        if node_id:
            url += "/nodes/" + node_id
        assert_helper(client, "GET", url)

    @pytest.mark.parametrize(
        ["index", "metric", "url_suffix"],
        [
            (None, None, None),
            (None, "cluster_name", "/cluster_name"),
            ("index-1", None, "/_all/index-1"),
            ("index-1", "cluster_name", "/cluster_name/index-1"),
        ],
    )
    def test_state_with_index_without_metric_defaults_to_all(
        self, index, metric, url_suffix
    ):
        client = Elasticsearch(transport_class=DummyTransport)
        client.cluster.state(index=index, metric=metric)
        url = "/_cluster/state"
        if url_suffix:
            url += url_suffix
        assert_helper(client, "GET", url)

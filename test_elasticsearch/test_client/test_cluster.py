# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from test_elasticsearch.test_cases import ElasticsearchTestCase


class TestCluster(ElasticsearchTestCase):
    def test_stats_without_node_id(self):
        self.client.cluster.stats()
        self.assert_url_called("GET", "/_cluster/stats")

    def test_stats_with_node_id(self):
        self.client.cluster.stats("node-1")
        self.assert_url_called("GET", "/_cluster/stats/nodes/node-1")

        self.client.cluster.stats(node_id="node-2")
        self.assert_url_called("GET", "/_cluster/stats/nodes/node-2")

    def test_state_with_index_without_metric_defaults_to_all(self):
        self.client.cluster.state()
        self.assert_url_called("GET", "/_cluster/state")

        self.client.cluster.state(metric="cluster_name")
        self.assert_url_called("GET", "/_cluster/state/cluster_name")

        self.client.cluster.state(index="index-1")
        self.assert_url_called("GET", "/_cluster/state/_all/index-1")

        self.client.cluster.state(index="index-1", metric="cluster_name")
        self.assert_url_called("GET", "/_cluster/state/cluster_name/index-1")

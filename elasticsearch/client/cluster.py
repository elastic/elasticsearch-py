from .utils import NamespacedClient, query_params, _make_path

class ClusterClient(NamespacedClient):
    @query_params('level', 'local', 'master_timeout', 'timeout', 'wait_for_active_shards', 'wait_for_nodes', 'wait_for_relocating_shards', 'wait_for_status')
    def health(self, index=None, params=None):
        """
        The cluster health API allows to get a very simple status on the health of the cluster.
        http://elasticsearch.org/guide/reference/api/admin-cluster-health/

        :arg index: Limit the information returned to a specific index
        :arg level: Specify the level of detail for returned information, default u'cluster'
        :arg local: Return local information, do not retrieve the state from master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master node
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Wait until the specified number of shards is active
        :arg wait_for_nodes: Wait until the specified number of nodes is available
        :arg wait_for_relocating_shards: Wait until the specified number of relocating shards is finished
        :arg wait_for_status: Wait until cluster is in a specific state, default None
        """
        status, data = self.transport.perform_request('GET', _make_path('_cluster', 'health', index), params=params)
        return data

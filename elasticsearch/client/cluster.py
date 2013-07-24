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

    @query_params('filter_blocks', 'filter_index_templates', 'filter_indices', 'filter_metadata', 'filter_nodes', 'filter_routing_table', 'local', 'master_timeout')
    def state(self, params=None):
        """
        The cluster state API allows to get a comprehensive state information of the whole cluster.
        http://elasticsearch.org/guide/reference/api/admin-cluster-state/

        :arg filter_blocks: Do not return information about blocks
        :arg filter_index_templates: Do not return information about index templates
        :arg filter_indices: Limit returned metadata information to specific indices
        :arg filter_metadata: Do not return information about indices metadata
        :arg filter_nodes: Do not return information about nodes
        :arg filter_routing_table: Do not return information about shard allocation (`routing_table` and `routing_nodes`)
        :arg local: Return local information, do not retrieve the state from master node (default: false)
        :arg master_timeout: Specify timeout for connection to master
        """
        status, data = self.transport.perform_request('GET', _make_path('_cluster', 'state'), params=params)
        return data


    @query_params('dry_run', 'filter_metadata')
    def reroute(self, body=None, params=None):
        """
        The reroute command allows to explicitly execute a cluster reroute allocation command including specific commands.
        http://elasticsearch.org/guide/reference/api/admin-cluster-reroute/

        :arg body: The definition of `commands` to perform (`move`, `cancel`, `allocate`)
        :arg dry_run: Simulate the operation only and return the resulting state
        :arg filter_metadata: Don't return cluster state metadata (default: false)
        """
        status, data = self.transport.perform_request('POST', _make_path('_cluster', 'reroute'), params=params, body=body)
        return data

    @query_params()
    def get_settings(self, params=None):
        """
        Allows to update cluster wide specific settings.
        http://elasticsearch.org/guide/reference/api/admin-cluster-update-settings/
        """
        status, data = self.transport.perform_request('GET', _make_path('_cluster', 'settings'), params=params)
        return data

    @query_params()
    def put_settings(self, body, params=None):
        """
        Allows to update cluster wide specific settings.
        http://elasticsearch.org/guide/reference/api/admin-cluster-update-settings/

        :arg body: The settings to be updated. Can be either `transient` or `persistent` (survives cluster restart).
        """
        status, data = self.transport.perform_request('PUT', _make_path('_cluster', 'settings'), params=params, body=body)
        return data

    @query_params('all', 'clear', 'fields', 'fs', 'http', 'indices', 'jvm', 'network', 'os', 'process', 'thread_pool', 'transport')
    def node_stats(self, node_id=None, metric=None, fields=None, params=None):
        """
        The cluster nodes stats API allows to retrieve one or more (or all) of the cluster nodes statistics.
        http://elasticsearch.org/guide/reference/api/admin-cluster-nodes-stats/

        :arg node_id: A comma-separated list of node IDs or names to limit the returned information; use `_local` to return information from the node you're connecting to, leave empty to get information from all nodes
        :arg metric: Limit the information returned for `indices` family to a specific metric
        :arg fields: A comma-separated list of fields to return detailed information for, when returning the `indices` metric family (supports wildcards)
        :arg all: Return all available information
        :arg clear: Reset the default level of detail
        :arg fields: A comma-separated list of fields for `fielddata` metric (supports wildcards)
        :arg fs: Return information about the filesystem
        :arg http: Return information about HTTP
        :arg indices: Return information about indices
        :arg jvm: Return information about the JVM
        :arg network: Return information about network
        :arg os: Return information about the operating system
        :arg process: Return information about the Elasticsearch process
        :arg thread_pool: Return information about the thread pool
        :arg transport: Return information about transport
        """
        status, data = self.transport.perform_request('GET', _make_path('_nodes', node_id, 'stats', metric, fields), params=params)
        return data

    @query_params('all', 'clear', 'http', 'jvm', 'network', 'os', 'plugin', 'process', 'settings', 'thread_pool', 'timeout', 'transport')
    def node_info(self, node_id=None, params=None):
        """
        The cluster nodes info API allows to retrieve one or more (or all) of the cluster nodes information.
        http://elasticsearch.org/guide/reference/api/admin-cluster-nodes-info/

        :arg node_id: A comma-separated list of node IDs or names to limit the returned information; use `_local` to return information from the node you're connecting to, leave empty to get information from all nodes
        :arg all: Return all available information
        :arg clear: Reset the default settings
        :arg http: Return information about HTTP
        :arg jvm: Return information about the JVM
        :arg network: Return information about network
        :arg os: Return information about the operating system
        :arg plugin: Return information about plugins
        :arg process: Return information about the Elasticsearch process
        :arg settings: Return information about node settings
        :arg thread_pool: Return information about the thread pool
        :arg timeout: Explicit operation timeout
        :arg transport: Return information about transport
        """
        status, data = self.transport.perform_request('GET', _make_path('_cluster', 'nodes', node_id), params=params)
        return data

    @query_params('delay', 'exit')
    def node_shutdown(self, node_id=None, params=None):
        """
        The nodes shutdown API allows to shutdown one or more (or all) nodes in the cluster.
        http://elasticsearch.org/guide/reference/api/admin-cluster-nodes-shutdown/

        :arg node_id: A comma-separated list of node IDs or names to perform the operation on; use `_local` to perform the operation on the node you're connected to, leave empty to perform the operation on all nodes
        :arg delay: Set the delay for the operation (default: 1s)
        :arg exit: Exit the JVM as well (default: true)
        """
        status, data = self.transport.perform_request('POST', _make_path('_cluster', 'nodes', node_id, '_shutdown'), params=params)
        return data


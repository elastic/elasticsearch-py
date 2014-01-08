from .utils import NamespacedClient, query_params, _make_path

class ClusterClient(NamespacedClient):
    @query_params('level', 'local', 'master_timeout', 'timeout',
        'wait_for_active_shards', 'wait_for_nodes', 'wait_for_relocating_shards',
        'wait_for_status')
    def health(self, index=None, params=None):
        """
        Get a very simple status on the health of the cluster.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-health/>`_

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
        _, data = self.transport.perform_request('GET', _make_path('_cluster', 'health', index),
            params=params)
        return data

    @query_params('filter_blocks', 'filter_index_templates', 'filter_indices',
        'filter_metadata', 'filter_nodes', 'filter_routing_table', 'local',
        'master_timeout', 'flat_settings')
    def state(self, params=None):
        """
        Get a comprehensive state information of the whole cluster.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-state/>`_

        :arg filter_blocks: Do not return information about blocks
        :arg filter_index_templates: Do not return information about index templates
        :arg filter_indices: Limit returned metadata information to specific indices
        :arg filter_metadata: Do not return information about indices metadata
        :arg filter_nodes: Do not return information about nodes
        :arg filter_routing_table: Do not return information about shard allocation (`routing_table` and `routing_nodes`)
        :arg local: Return local information, do not retrieve the state from master node (default: false)
        :arg master_timeout: Specify timeout for connection to master
        :arg flat_settings: Return settings in flat format (default: false)
        """
        _, data = self.transport.perform_request('GET', '/_cluster/state', params=params)
        return data


    @query_params('dry_run', 'filter_metadata')
    def reroute(self, body=None, params=None):
        """
        Explicitly execute a cluster reroute allocation command including specific commands.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-reroute/>`_

        :arg body: The definition of `commands` to perform (`move`, `cancel`, `allocate`)
        :arg dry_run: Simulate the operation only and return the resulting state
        :arg filter_metadata: Don't return cluster state metadata (default: false)
        """
        _, data = self.transport.perform_request('POST', '/_cluster/reroute', params=params, body=body)
        return data

    @query_params('flat_settings')
    def get_settings(self, params=None):
        """
        Get cluster settings.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-update-settings/>`_

        :arg flat_settings: Return settings in flat format (default: false)
        """
        _, data = self.transport.perform_request('GET', '/_cluster/settings', params=params)
        return data

    @query_params('flat_settings')
    def put_settings(self, body, params=None):
        """
        Update cluster wide specific settings.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-update-settings/>`_

        :arg body: The settings to be updated. Can be either `transient` or
            `persistent` (survives cluster restart).
        :arg flat_settings: Return settings in flat format (default: false)
        """
        _, data = self.transport.perform_request('PUT', '/_cluster/settings', params=params, body=body)
        return data

    @query_params('all', 'clear', 'fields', 'fs', 'http', 'indices', 'jvm',
        'network', 'os', 'process', 'thread_pool', 'transport')
    def node_stats(self, node_id=None, metric=None, fields=None, params=None):
        """
        Retrieve one or more (or all) of the cluster nodes statistics.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-nodes-stats/>`_

        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the node
            you're connecting to, leave empty to get information from all nodes
        :arg metric: Limit the information returned for `indices` family to a specific metric
        :arg fields: A comma-separated list of fields to return detailed information
            for, when returning the `indices` metric family (supports wildcards)
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
        _, data = self.transport.perform_request('GET',
            _make_path('_nodes', node_id, 'stats', metric, fields), params=params)
        return data

    @query_params('flat_settings')
    def node_info(self, node_id=None, metric=None, params=None):
        """
        Retrieve one or more (or all) of the cluster nodes' information.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-nodes-info/>`_

        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the node
            you're connecting to, leave empty to get information from all nodes
        :arg metric: A comma-separated list of metrics you wish returned. Leave
            empty to return all. Possible options are "settings", "os",
            "process", "jvm", "thread_pool", "network", "transport", "http" and
            "plugin"
        :arg flat_settings: Return settings in flat format (default: false)
        """
        if not node_id and metric:
            node_id = '_all'
        _, data = self.transport.perform_request('GET',
            _make_path('_nodes', node_id, metric), params=params)
        return data

    @query_params('delay', 'exit')
    def node_shutdown(self, node_id=None, params=None):
        """
        Shutdown one or more (or all) nodes in the cluster.
        `<http://elasticsearch.org/guide/reference/api/admin-cluster-nodes-shutdown/>`_

        :arg node_id: A comma-separated list of node IDs or names to perform
            the operation on; use `_local` to perform the operation on the node
            you're connected to, leave empty to perform the operation on all nodes
        :arg delay: Set the delay for the operation (default: 1s)
        :arg exit: Exit the JVM as well (default: true)
        """
        _, data = self.transport.perform_request('POST',
            _make_path('_cluster', 'nodes', node_id, '_shutdown'), params=params)
        return data


from .utils import NamespacedClient, query_params, _make_path

class CatClient(NamespacedClient):
    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def aliases(self, name=None, params=None):
        """
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-alias.html>`_

        :arg name: A comma-separated list of alias names to return
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'aliases', name), params=params)
        return data

    @query_params('bytes', 'h', 'help', 'local', 'master_timeout', 'v')
    def allocation(self, node_id=None, params=None):
        """
        Allocation provides a snapshot of how shards have located around the
        cluster and the state of disk usage.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-allocation.html>`_

        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information
        :arg bytes: The unit in which to display byte values
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'allocation', node_id), params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def count(self, index=None, params=None):
        """
        Count provides quick access to the document count of the entire cluster,
        or individual indices.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-count.html>`_

        :arg index: A comma-separated list of index names to limit the returned
            information
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'count', index), params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'ts', 'v')
    def health(self, params=None):
        """
        health is a terse, one-line representation of the same information from
        :meth:`~elasticsearch.client.cluster.ClusterClient.health` API
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-health.html>`_

        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg ts: Set to false to disable timestamping, default True
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', '/_cat/health',
            params=params)
        return data

    @query_params('help')
    def help(self, params=None):
        """
        A simple help for the cat api.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat.html>`_

        :arg help: Return help information, default False
        """
        _, data = self.transport.perform_request('GET', '/_cat', params=params)
        return data

    @query_params('bytes', 'h', 'help', 'local', 'master_timeout', 'pri', 'v')
    def indices(self, index=None, params=None):
        """
        The indices command provides a cross-section of each index.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-indices.html>`_

        :arg index: A comma-separated list of index names to limit the returned
            information
        :arg bytes: The unit in which to display byte values
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg pri: Set to true to return stats only for primary shards, default
            False
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'indices', index), params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def master(self, params=None):
        """
        Displays the master's node ID, bound IP address, and node name.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-master.html>`_

        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', '/_cat/master',
            params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def nodes(self, params=None):
        """
        The nodes command shows the cluster topology.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-nodes.html>`_

        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', '/_cat/nodes',
            params=params)
        return data

    @query_params('bytes', 'h', 'help', 'local', 'master_timeout', 'v')
    def recovery(self, index=None, params=None):
        """
        recovery is a view of shard replication.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-recovery.html>`_

        :arg index: A comma-separated list of index names to limit the returned
            information
        :arg bytes: The unit in which to display byte values
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'recovery', index), params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def shards(self, index=None, params=None):
        """
        The shards command is the detailed view of what nodes contain which shards.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-shards.html>`_

        :arg index: A comma-separated list of index names to limit the returned
            information
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'shards', index), params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def segments(self, index=None, params=None):
        """
        The segments command is the detailed view of Lucene segments per index.

        :arg index: A comma-separated list of index names to limit the returned
            information
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'segments', index), params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def pending_tasks(self, params=None):
        """
        pending_tasks provides the same information as the
        :meth:`~elasticsearch.client.cluster.ClusterClient.pending_tasks` API
        in a convenient tabular format.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-pending-tasks.html>`_

        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', '/_cat/pending_tasks',
            params=params)
        return data

    @query_params('full_id', 'h', 'help', 'local', 'master_timeout', 'v')
    def thread_pool(self, params=None):
        """
        Get information about thread pools.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-thread-pool.html>`_

        :arg full_id: Enables displaying the complete node ids (default: 'false')
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information (default: 'false')
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers (default: 'false')

        """
        _, data = self.transport.perform_request('GET', '/_cat/thread_pool',
            params=params)
        return data

    @query_params('bytes', 'fields', 'h', 'help', 'local', 'master_timeout',
        'v')
    def fielddata(self, fields=None, params=None):
        """
        Shows information about currently loaded fielddata on a per-node basis.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/cat-fielddata.html>`_

        :arg fields: A comma-separated list of fields to return the fielddata
            size
        :arg bytes: The unit in which to display byte values
        :arg fields: A comma-separated list of fields to return the fielddata
            size
        :arg h: Comma-separated list of column names to display
        :arg help: Return help information (default: 'false')
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers (default: 'false')

        """
        _, data = self.transport.perform_request('GET', _make_path('_cat',
            'fielddata', fields), params=params)
        return data

    @query_params('h', 'help', 'local', 'master_timeout', 'v')
    def plugins(self, params=None):
        """
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/cat-plugins.html>`_

        :arg h: Comma-separated list of column names to display
        :arg help: Return help information, default False
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg v: Verbose mode. Display column headers, default False
        """
        _, data = self.transport.perform_request('GET', '/_cat/plugins',
            params=params)
        return data


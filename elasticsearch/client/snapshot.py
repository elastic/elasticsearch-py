from .utils import NamespacedClient, query_params, _make_path

class SnapshotClient(NamespacedClient):
    @query_params('master_timeout', 'wait_for_completion')
    def create(self, repository, snapshot, body=None, params=None):
        """
        Create a snapshot in repository
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg body: The snapshot definition
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg wait_for_completion: Should this request wait until the operation
            has completed before returning, default False    
        """
        _, data = self.transport.perform_request('PUT', _make_path('_snapshot',
            repository, snapshot), params=params, body=body)
        return data
    
    @query_params('master_timeout')
    def delete(self, repository, snapshot, params=None):
        """
        Deletes a snapshot from a repository.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg master_timeout: Explicit operation timeout for connection to master
            node    
        """
        _, data = self.transport.perform_request('DELETE',
            _make_path('_snapshot', repository, snapshot), params=params)
        return data
    
    @query_params('master_timeout')
    def get(self, repository, snapshot, params=None):
        """
        Retrieve information about a snapshot.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A comma-separated list of repository names
        :arg snapshot: A comma-separated list of snapshot names
        :arg master_timeout: Explicit operation timeout for connection to master
            node    
        """
        _, data = self.transport.perform_request('GET', _make_path('_snapshot',
            repository, snapshot), params=params)
        return data
    
    @query_params('master_timeout', 'timeout')
    def delete_repository(self, repository, params=None):
        """
        Removes a shared file system repository.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A comma-separated list of repository names
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg timeout: Explicit operation timeout    
        """
        _, data = self.transport.perform_request('DELETE',
            _make_path('_snapshot', repository), params=params)
        return data
    
    @query_params('local', 'master_timeout')
    def get_repository(self, repository=None, params=None):
        """
        Return information about registered repositories.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A comma-separated list of repository names
        :arg master_timeout: Explicit operation timeout for connection to master
            node    
        :arg local: Return local information, do not retrieve the state from
            master node (default: false)
        """
        _, data = self.transport.perform_request('GET', _make_path('_snapshot',
            repository), params=params)
        return data
    
    @query_params('master_timeout', 'timeout')
    def create_repository(self, repository, body, params=None):
        """
        Registers a shared file system repository.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg body: The repository definition
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg timeout: Explicit operation timeout    
        """
        _, data = self.transport.perform_request('PUT', _make_path('_snapshot',
            repository), params=params, body=body)
        return data
    
    @query_params('master_timeout', 'wait_for_completion')
    def restore(self, repository, snapshot, body=None, params=None):
        """
        Restore a snapshot.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/master/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A snapshot name
        :arg body: Details of what to restore
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg wait_for_completion: Should this request wait until the operation
            has completed before returning, default False    
        """
        _, data = self.transport.perform_request('POST', _make_path('_snapshot',
            repository, snapshot, '_restore'), params=params, body=body)
        return data

    @query_params('master_timeout')
    def status(self, repository=None, snapshot=None, params=None):
        """
        Return information about all currently running snapshots. By specifying
        a repository name, it’s possible to limit the results to a particular
        repository.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg snapshot: A comma-separated list of snapshot names
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        """
        _, data = self.transport.perform_request('GET', _make_path('_snapshot',
            repository, snapshot, '_status'), params=params)
        return data

    @query_params('master_timeout', 'timeout')
    def verify_repository(self, repository, params=None):
        """
        Returns a list of nodes where repository was successfully verified or
        an error message if verification process failed.
        `<http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-snapshots.html>`_

        :arg repository: A repository name
        :arg master_timeout: Explicit operation timeout for connection to master
            node
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('POST', _make_path('_snapshot',
            repository, '_verify'), params=params)
        return data


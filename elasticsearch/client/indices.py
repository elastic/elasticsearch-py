from .utils import NamespacedClient, query_params, _make_path
from ..exceptions import NotFoundError

class IndicesClient(NamespacedClient):
    @query_params('analyzer', 'field', 'filters', 'format', 'index',
        'prefer_local', 'text', 'tokenizer')
    def analyze(self, index=None, body=None, params=None):
        """
        Perform the analysis process on a text and return the tokens breakdown of the text.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-analyze/

        :arg index: The name of the index to scope the operation
        :arg body: The text on which the analysis should be performed
        :arg analyzer: The name of the analyzer to use
        :arg field: Use the analyzer configured for this field (instead of
            passing the analyzer name)
        :arg filters: A comma-separated list of filters to use for the analysis
        :arg format: Format of the output, default u'detailed'
        :arg index: The name of the index to scope the operation
        :arg prefer_local: With `true`, specify that a local shard should be
            used if available, with `false`, use a random shard (default: true)
        :arg text: The text on which the analysis should be performed (when
            request body is not used)
        :arg tokenizer: The name of the tokenizer to use for the analysis
        """
        _, data = self.transport.perform_request('GET', _make_path(index, '_analyze'),
            params=params, body=body)
        return data

    @query_params('ignore_indices')
    def refresh(self, index=None, params=None):
        """
        Explicitly refresh one or more index, making all operations performed
        since the last refresh available for search.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-refresh/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones, default u'none'
        """
        _, data = self.transport.perform_request('POST', _make_path(index, '_refresh'),
            params=params)
        return data

    @query_params('force', 'full', 'ignore_indices', 'refresh')
    def flush(self, index=None, params=None):
        """
        Explicitly flush one or more indices.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-flush/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string for all indices
        :arg force: TODO: ?
        :arg full: TODO: ?
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        :arg refresh: Refresh the index after performing the operation
        """
        _, data = self.transport.perform_request('POST', _make_path(index, '_flush'),
            params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def create(self, index, body=None, params=None):
        """
        Create an index in Elasticsearch.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index/

        :arg index: The name of the index
        :arg body: The configuration for the index (`settings` and `mappings`)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('PUT', _make_path(index),
            params=params, body=body)
        return data

    @query_params('timeout', 'master_timeout')
    def open(self, index, params=None):
        """
        Open a closed index to make it available for search.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-open-close/

        :arg index: The name of the index
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('POST', _make_path(index, '_open'),
            params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def close(self, index, params=None):
        """
        Close an index to remove it's overhead from the cluster. Closed index
        is blocked for read/write operations.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-open-close/

        :arg index: The name of the index
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('POST', _make_path(index, '_close'),
            params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def delete(self, index=None, params=None):
        """
        Delete an index in Elasticsearch
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-index/

        :arg index: A comma-separated list of indices to delete; use `_all` or
            empty string to delete all indices
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('DELETE', _make_path(index),
            params=params)
        return data

    @query_params()
    def exists(self, index, params=None):
        """
        Return a boolean indicating whether given index exists.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-indices-exists/

        :arg index: A list of indices to check
        """
        try:
            self.transport.perform_request('HEAD', _make_path(index), params=params)
        except NotFoundError:
            return False
        return True

    @query_params('ignore_indices')
    def exists_type(self, index, doc_type, params=None):
        """
        Check if a type/types exists in an index/indices.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-types-exists/

        :arg index: A comma-separated list of index names; use `_all` to check
            the types across all indices
        :arg doc_type: A comma-separated list of document types to check
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        """
        try:
            self.transport.perform_request('HEAD', _make_path(index, doc_type), params=params)
        except NotFoundError:
            return False
        return True

    @query_params('ignore_indices')
    def snapshot_index(self, index=None, params=None):
        """
        Explicitly perform a snapshot through the gateway of one or more indices (backup them).
        http://www.elasticsearch.org/guide/reference/api/admin-indices-gateway-snapshot/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string for all indices
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        """
        _, data = self.transport.perform_request('POST',
            _make_path(index, '_gateway', 'snapshot'), params=params)
        return data

    @query_params('ignore_conflicts', 'timeout', 'master_timeout')
    def put_mapping(self, index, doc_type, body, params=None):
        """
        Register specific mapping definition for a specific type.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-put-mapping/

        :arg index: A comma-separated list of index names; use `_all` to
            perform the operation on all indices
        :arg doc_type: The name of the document type
        :arg body: The mapping definition
        :arg ignore_conflicts: Specify whether to ignore conflicts while
            updating the mapping (default: false)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('PUT', _make_path(index, doc_type, '_mapping'),
            params=params, body=body)
        return data

    @query_params()
    def get_mapping(self, index=None, doc_type=None, params=None):
        """
        Retrieve mapping definition of index or index/type.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-get-mapping/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string for all indices
        :arg doc_type: A comma-separated list of document types
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_mapping'),
            params=params)
        return data

    @query_params('master_timeout')
    def delete_mapping(self, index, doc_type, params=None):
        """
        Delete a mapping (type) along with its data.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-mapping/

        :arg index: A comma-separated list of index names; use `_all` for all indices
        :arg doc_type: The name of the document type to delete
        :arg master_timeout: Specify timeout for connection to master
        """
        _, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, '_mapping'),
            params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def put_alias(self, index, name, body=None, params=None):
        """
        Create an alias for a specific index/indices.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg index: The name of the index with an alias
        :arg name: The name of the alias to be created or updated
        :arg body: The settings for the alias, such as `routing` or `filter`
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        _, data = self.transport.perform_request('PUT', _make_path(index, '_alias', name),
            params=params, body=body)
        return data

    @query_params('ignore_indices')
    def exists_alias(self, name, index=None, params=None):
        """
        Return a boolean indicating whether given alias exists.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg name: A comma-separated list of alias names to return
        :arg index: A comma-separated list of index names to filter aliases
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        """
        try:
            self.transport.perform_request('HEAD', _make_path(index, '_alias', name),
                params=params)
        except NotFoundError:
            return False
        return True

    @query_params('ignore_indices')
    def get_alias(self, name, index=None, params=None):
        """
        Retrieve a specified alias.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg name: A comma-separated list of alias names to return
        :arg index: A comma-separated list of index names to filter aliases
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones, default u'none'
        """
        _, data = self.transport.perform_request('GET', _make_path(index, '_alias', name),
            params=params)
        return data

    @query_params('timeout')
    def get_aliases(self, index=None, params=None):
        """
        Retrieve specified aliases
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg index: A comma-separated list of index names to filter aliases
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('GET', _make_path(index, '_aliases'),
            params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def update_aliases(self, body, params=None):
        """
        Update specified aliases.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg body: The definition of `actions` to perform
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Request timeout
        """
        _, data = self.transport.perform_request('POST', '/_aliases',
            params=params, body=body)
        return data

    @query_params('timeout', 'master_timeout')
    def delete_alias(self, index, name, params=None):
        """
        Delete specific alias.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg index: The name of the index with an alias
        :arg name: The name of the alias to be deleted
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        _, data = self.transport.perform_request('DELETE', _make_path(index, '_alias', name),
            params=params)
        return data

    @query_params('order', 'timeout', 'master_timeout')
    def put_template(self, name, body, params=None):
        """
        Create an index template that will automatically be applied to new
        indices created.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-templates/

        :arg name: The name of the template
        :arg body: The template definition
        :arg order: The order for this template when merging multiple matching
            ones (higher numbers are merged later, overriding the lower numbers)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('PUT', _make_path('_template', name),
            params=params, body=body)
        return data

    @query_params()
    def get_template(self, name, params=None):
        """
        Retrieve an index template by its name.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-templates/

        :arg name: The name of the template
        """
        _, data = self.transport.perform_request('GET', _make_path('_template', name),
            params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def delete_template(self, name, params=None):
        """
        Delete an index template by its name.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-templates/

        :arg name: The name of the template
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        _, data = self.transport.perform_request('DELETE', _make_path('_template', name),
            params=params)
        return data

    @query_params()
    def get_settings(self, index=None, params=None):
        """
        Retrieve settings for one or more (or all) indices.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-get-settings/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        """
        _, data = self.transport.perform_request('GET', _make_path(index, '_settings'),
            params=params)
        return data

    @query_params('master_timeout')
    def put_settings(self, body, index=None, params=None):
        """
        Change specific index level settings in real time.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-update-settings/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg master_timeout: Specify timeout for connection to master
        :arg body: The index settings to be updated
        """
        _, data = self.transport.perform_request('PUT', _make_path(index, '_settings'),
            params=params, body=body)
        return data

    @query_params('master_timeout')
    def put_warmer(self, index, name, body, doc_type=None, params=None):
        """
        Create an index warmer to run registered search requests to warm up the
        index before it is available for search.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-warmers/

        :arg index: A comma-separated list of index names to register the warmer for;
            use `_all` or empty string to perform the operation on all indices
        :arg name: The name of the warmer
        :arg doc_type: A comma-separated list of document types to register the
            warmer for; leave empty to perform the operation on all types
        :arg body: The search request definition for the warmer (query, filters, facets, sorting, etc)
        :arg master_timeout: Specify timeout for connection to master
        """
        _, data = self.transport.perform_request('PUT', _make_path(index, doc_type, '_warmer', name),
            params=params, body=body)
        return data

    @query_params()
    def get_warmer(self, index, doc_type=None, name=None, params=None):
        """
        Retreieve an index warmer.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-warmers/

        :arg index: A comma-separated list of index names to restrict the
            operation; use `_all` to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to restrict the
            operation; leave empty to perform the operation on all types
        :arg name: The name of the warmer (supports wildcards); leave empty to get all warmers
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_warmer', name), params=params)
        return data

    @query_params('master_timeout')
    def delete_warmer(self, index, doc_type=None, name=None, params=None):
        """
        Delete an index warmer.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-warmers/

        :arg index: A comma-separated list of index names to register warmer
            for; use `_all` or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to register warmer for;
            use `_all` or empty string to perform the operation on all types
        :arg name: The name of the warmer (supports wildcards); leave empty to delete all warmers
        :arg master_timeout: Specify timeout for connection to master
        """
        _, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, '_warmer', name),
            params=params)
        return data

    @query_params('ignore_indices', 'operation_threading', 'recovery', 'snapshot')
    def status(self, index=None, params=None):
        """
        Get a comprehensive status information of one or more indices.
        http://elasticsearch.org/guide/reference/api/admin-indices-_/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones, default u'none'
        :arg operation_threading: TODO: ?
        :arg recovery: Return information about shard recovery
        :arg snapshot: TODO: ?
        """
        _, data = self.transport.perform_request('GET', _make_path(index, '_status'),
            params=params)
        return data

    @query_params('all', 'clear', 'docs', 'fielddata', 'fields',
        'filter_cache', 'flush', 'get', 'groups', 'id_cache', 'ignore_indices',
        'indexing', 'merge', 'refresh', 'search', 'store', 'warmer')
    def stats(self, index=None, metric_family=None, params=None):
        """
        Retrieve statistics on different operations happening on an index.
        http://elasticsearch.org/guide/reference/api/admin-indices-stats/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg metric_family: Limit the information returned to a specific metric
        :arg all: Return all available information
        :arg clear: Reset the default level of detail
        :arg docs: Return information about indexed and deleted documents
        :arg fielddata: Return information about field data
        :arg fields: A comma-separated list of fields for `fielddata` metric
            (supports wildcards)
        :arg filter_cache: Return information about filter cache
        :arg flush: Return information about flush operations
        :arg get: Return information about get operations
        :arg groups: A comma-separated list of search groups for `search` statistics
        :arg id_cache: Return information about ID cache
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        :arg indexing: Return information about indexing operations
        :arg merge: Return information about merge operations
        :arg refresh: Return information about refresh operations
        :arg search: Return information about search operations; use the
            `groups` parameter to include information for specific search groups
        :arg store: Return information about the size of the index
        :arg warmer: Return information about warmers
        """
        _, data = self.transport.perform_request('GET', _make_path(index, '_stats', metric_family),
            params=params)
        return data

    @query_params('ignore_indices', 'operation_threading')
    def segments(self, index=None, params=None):
        """
        Provide low level segments information that a Lucene index (shard level) is built with.
        http://elasticsearch.org/guide/reference/api/admin-indices-segments/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones, default u'none'
        :arg operation_threading: TODO: ?
        """
        _, data = self.transport.perform_request('GET', _make_path(index, '_segments'), params=params)
        return data

    @query_params('flush', 'ignore_indices', 'max_num_segments',
        'only_expunge_deletes', 'operation_threading', 'refresh', 'wait_for_merge')
    def optimize(self, index=None, params=None):
        """
        Explicitly optimize one or more indices through an API.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-optimize/

        :arg index: A comma-separated list of index names; use `_all` or empty
            string to perform the operation on all indices
        :arg flush: Specify whether the index should be flushed after
            performing the operation (default: true)
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones, default u'none'
        :arg max_num_segments: The number of segments the index should be
            merged into (default: dynamic)
        :arg only_expunge_deletes: Specify whether the operation should only
            expunge deleted documents
        :arg operation_threading: TODO: ?
        :arg refresh: Specify whether the index should be refreshed after
            performing the operation (default: true)
        :arg wait_for_merge: Specify whether the request should block until the
            merge process is finished (default: true)
        """
        _, data = self.transport.perform_request('POST', _make_path(index, '_optimize'), params=params)
        return data

    @query_params('explain', 'ignore_indices', 'operation_threading', 'q', 'source')
    def validate_query(self, index=None, doc_type=None, body=None, params=None):
        """
        Validate a potentially expensive query without executing it.
        http://www.elasticsearch.org/guide/reference/api/validate/

        :arg index: A comma-separated list of index names to restrict the operation;
            use `_all` or empty string to perform the operation on all indices
        :arg doc_type: A comma-separated list of document types to restrict the
            operation; leave empty to perform the operation on all types
        :arg body: The query definition
        :arg explain: Return detailed information about the error
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        :arg operation_threading: TODO: ?
        :arg q: Query in the Lucene query string syntax
        :arg source: The URL-encoded query definition (instead of using the
            request body)
        """
        _, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_validate', 'query'),
            params=params, body=body)
        return data

    @query_params('field_data', 'fielddata', 'fields', 'filter',
        'filter_cache', 'filter_keys', 'id', 'id_cache', 'ignore_indices', 'index',
        'recycler')
    def clear_cache(self, index=None, params=None):
        """
        Clear either all caches or specific cached associated with one ore more indices.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-clearcache/

        :arg index: A comma-separated list of index name to limit the operation
        :arg field_data: Clear field data
        :arg fielddata: Clear field data
        :arg fields: A comma-separated list of fields to clear when using the
            `field_data` parameter (default: all)
        :arg filter: Clear filter caches
        :arg filter_cache: Clear filter caches
        :arg filter_keys: A comma-separated list of keys to clear when using
            the `filter_cache` parameter (default: all)
        :arg id: Clear ID caches for parent/child
        :arg id_cache: Clear ID caches for parent/child
        :arg ignore_indices: When performed on multiple indices, allows to
            ignore `missing` ones (default: none)
        :arg index: A comma-separated list of index name to limit the operation
        :arg recycler: Clear the recycler cache
        """
        _, data = self.transport.perform_request('POST', _make_path(index, '_cache', 'clear'),
            params=params)
        return data


from .utils import NamespacedClient, query_params, _make_path
from ..exceptions import NotFoundError

class IndicesClient(NamespacedClient):
    @query_params('analyzer', 'field', 'filters', 'format', 'index', 'prefer_local', 'text', 'tokenizer')
    def analyze(self, index=None, body=None, params=None):
        """
        Performs the analysis process on a text and return the tokens breakdown of the text.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-analyze/

        :arg index: The name of the index to scope the operation
        :arg body: The text on which the analysis should be performed
        :arg analyzer: The name of the analyzer to use
        :arg field: Use the analyzer configured for this field (instead of passing the analyzer name)
        :arg filters: A comma-separated list of filters to use for the analysis
        :arg format: Format of the output, default u'detailed'
        :arg index: The name of the index to scope the operation
        :arg prefer_local: With `true`, specify that a local shard should be used if available, with `false`, use a random shard (default: true)
        :arg text: The text on which the analysis should be performed (when request body is not used)
        :arg tokenizer: The name of the tokenizer to use for the analysis
        """
        status, data = self.transport.perform_request('GET', _make_path(index, '_analyze'), params=params, body=body)
        return data

    @query_params('ignore_indices')
    def refresh(self, index=None, params=None):
        """
        The refresh API allows to explicitly refresh one or more index, making all operations performed since the last refresh available for search.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-refresh/

        :arg index: A comma-separated list of index names; use `_all` or empty string to perform the operation on all indices
        :arg ignore_indices: When performed on multiple indices, allows to ignore `missing` ones, default u'none'
        """
        status, data = self.transport.perform_request('POST', _make_path(index, '_refresh'), params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def create(self, index, body=None, params=None):
        """
        Create index in Elasticsearch.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index/

        :arg index: The name of the index
        :arg body: The configuration for the index (`settings` and `mappings`)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('PUT', _make_path(index), params=params, body=body)
        return data

    @query_params('timeout', 'master_timeout')
    def delete(self, index=None, params=None):
        """
        Delete index in Elasticsearch
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-index/

        :arg index: A comma-separated list of indices to delete; use `_all` or empty string to delete all indices
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('DELETE', _make_path(index), params=params)
        return data

    @query_params()
    def exists(self, index, params=None):
        """
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
        Used to check if a type/types exists in an index/indices (available since 0.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-types-exists/

        :arg index: A comma-separated list of index names; use `_all` to check the types across all indices
        :arg doc_type: A comma-separated list of document types to check
        :arg ignore_indices: When performed on multiple indices, allows to ignore `missing` ones, default u'none'
        """
        try:
            self.transport.perform_request('HEAD', _make_path(index, doc_type), params=params)
        except NotFoundError:
            return False
        return True

    @query_params('ignore_conflicts', 'timeout', 'master_timeout')
    def put_mapping(self, index, doc_type, body, params=None):
        """
        The put mapping API allows to register specific mapping definition for a specific type.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-put-mapping/

        :arg index: A comma-separated list of index names; use `_all` to perform the operation on all indices
        :arg doc_type: The name of the document type
        :arg body: The mapping definition
        :arg ignore_conflicts: Specify whether to ignore conflicts while updating the mapping (default: false)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('PUT', _make_path(index, doc_type, '_mapping'), params=params, body=body)
        return data

    @query_params()
    def get_mapping(self, index=None, doc_type=None, params=None):
        """
        The get mapping API allows to retrieve mapping definition of index or index/type.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-get-mapping/

        :arg index: A comma-separated list of index names; use `_all` or empty string for all indices
        :arg doc_type: A comma-separated list of document types
        """
        status, data = self.transport.perform_request('GET', _make_path(index, doc_type, '_mapping'), params=params)
        return data

    @query_params('master_timeout')
    def delete_mapping(self, index, doc_type, params=None):
        """
        Allow to delete a mapping (type) along with its data.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-mapping/

        :arg index: A comma-separated list of index names; use `_all` for all indices
        :arg doc_type: The name of the document type to delete
        :arg master_timeout: Specify timeout for connection to master
        """
        status, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, '_mapping'), params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def put_alias(self, index, name, body=None, params=None):
        """
        APIs in elasticsearch accept an index name when working against a specific index, and several indices when applicable.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg index: The name of the index with an alias
        :arg name: The name of the alias to be created or updated
        :arg body: The settings for the alias, such as `routing` or `filter`
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        status, data = self.transport.perform_request('PUT', _make_path(index, '_alias', name), params=params, body=body)
        return data

    @query_params('ignore_indices')
    def exists_alias(self, name, index=None, params=None):
        """
        APIs in elasticsearch accept an index name when working against a specific index, and several indices when applicable.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg name: A comma-separated list of alias names to return
        :arg index: A comma-separated list of index names to filter aliases
        :arg ignore_indices: When performed on multiple indices, allows to ignore `missing` ones, default u'none'
        """
        try:
            self.transport.perform_request('HEAD', _make_path(index, '_alias', name), params=params)
        except NotFoundError:
            return False
        return True

    @query_params('ignore_indices')
    def get_alias(self, name, index=None, params=None):
        """
        APIs in elasticsearch accept an index name when working against a specific index, and several indices when applicable.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg name: A comma-separated list of alias names to return
        :arg index: A comma-separated list of index names to filter aliases
        :arg ignore_indices: When performed on multiple indices, allows to ignore `missing` ones, default u'none'
        """
        status, data = self.transport.perform_request('GET', _make_path(index, '_alias', name), params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def delete_alias(self, index, name, params=None):
        """
        APIs in elasticsearch accept an index name when working against a specific index, and several indices when applicable.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-aliases/

        :arg index: The name of the index with an alias
        :arg name: The name of the alias to be deleted
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        status, data = self.transport.perform_request('DELETE', _make_path(index, '_alias', name), params=params)
        return data

    @query_params('timeout', 'master_timeout')
    def delete_template(self, name, params=None):
        """
        Index templates allow to define templates that will automatically be applied to new indices created.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-templates/

        :arg name: The name of the template
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('DELETE', _make_path('_template', name), params=params)
        return data

    @query_params('order', 'timeout', 'master_timeout')
    def put_template(self, name, body, params=None):
        """
        Index templates allow to define templates that will automatically be applied to new indices created.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-templates/

        :arg name: The name of the template
        :arg body: The template definition
        :arg order: The order for this template when merging multiple matching ones (higher numbers are merged later, overriding the lower numbers)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('PUT', _make_path('_template', name), params=params, body=body)
        return data

    @query_params()
    def get_template(self, name, params=None):
        """
        Index templates allow to define templates that will automatically be applied to new indices created.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-templates/

        :arg name: The name of the template
        """
        status, data = self.transport.perform_request('GET', _make_path('_template', name), params=params)
        return data

    @query_params()
    def get_settings(self, index=None, params=None):
        """
        The get settings API allows to retrieve settings of index/indices.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-get-settings/

        :arg index: A comma-separated list of index names; use `_all` or empty string to perform the operation on all indices
        """
        status, data = self.transport.perform_request('GET', _make_path(index, '_settings'), params=params)
        return data

    @query_params('master_timeout')
    def put_settings(self, body, index=None, params=None):
        """
        Change specific index level settings in real time.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-update-settings/

        :arg index: A comma-separated list of index names; use `_all` or empty string to perform the operation on all indices
        :arg master_timeout: Specify timeout for connection to master
        :arg body: The index settings to be updated
        """
        status, data = self.transport.perform_request('PUT', _make_path(index, '_settings'), params=params, body=body)
        return data


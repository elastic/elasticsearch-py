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
        :arg field: The name of the field to
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

    @query_params('timeout')
    def create(self, index, body=None, params=None):
        """
        Create index in Elasticsearch.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-create-index/

        :arg index: The name of the index
        :arg body: The configuration for the index (`settings` and `mappings`)
        :arg timeout: Explicit operation timeout
        """
        status, data = self.transport.perform_request('PUT', _make_path(index), params=params, body=body)
        return data

    @query_params('timeout')
    def delete(self, index=None, params=None):
        """
        Delete index in Elasticsearch
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-index/

        :arg index: A list of indices to delete, `None` if all indices should be removed.
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

    @query_params('ignore_conflicts', 'timeout')
    def put_mapping(self, index, body, doc_type=None, params=None):
        """
        The put mapping API allows to register specific mapping definition for a specific type.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-put-mapping/

        :arg index: A comma-separated list of index names; use `_all` to perform the operation on all indices
        :arg doc_type: The name of the document type
        :arg body: The mapping definition
        :arg ignore_conflicts: Specify whether to ignore conflicts while updating the mapping (default: false)
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

    @query_params()
    def delete_mapping(self, index, doc_type, params=None):
        """
        Allow to delete a mapping (type) along with its data.
        http://www.elasticsearch.org/guide/reference/api/admin-indices-delete-mapping/

        :arg index: A comma-separated list of index names; use `_all` for all indices
        :arg doc_type: The name of the document type to delete
        """
        status, data = self.transport.perform_request('DELETE', _make_path(index, doc_type, '_mapping'), params=params)
        return data

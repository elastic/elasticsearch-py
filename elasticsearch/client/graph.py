# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class GraphClient(NamespacedClient):
    @query_params("routing", "timeout")
    def explore(self, index, body=None, params=None, headers=None):
        """
        Explore extracted and summarized information about the documents and terms in
        an index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/graph-explore-api.html>`_

        :arg index: A comma-separated list of index names to search; use
            `_all` or empty string to perform the operation on all indices
        :arg body: Graph Query DSL
        :arg routing: Specific routing value
        :arg timeout: Explicit operation timeout
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "POST",
            _make_path(index, "_graph", "explore"),
            params=params,
            headers=headers,
            body=body,
        )

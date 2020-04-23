# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params, _make_path


class MigrationClient(NamespacedClient):
    @query_params()
    def deprecations(self, index=None, params=None, headers=None):
        """
        Retrieves information about different cluster, node, and index level settings
        that use deprecated features that will be removed or changed in the next major
        version.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/migration-api-deprecation.html>`_

        :arg index: Index pattern
        """
        return self.transport.perform_request(
            "GET",
            _make_path(index, "_migration", "deprecations"),
            params=params,
            headers=headers,
        )

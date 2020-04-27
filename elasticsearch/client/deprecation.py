# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params, _make_path


class DeprecationClient(NamespacedClient):
    @query_params()
    def info(self, index=None, params=None, headers=None):
        """
        `<http://www.elastic.co/guide/en/migration/7.x/migration-api-deprecation.html>`_

        :arg index: Index pattern
        """
        return self.transport.perform_request(
            "GET",
            _make_path(index, "_xpack", "migration", "deprecations"),
            params=params,
            headers=headers,
        )

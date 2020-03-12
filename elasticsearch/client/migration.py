from .utils import NamespacedClient, query_params, _make_path


class MigrationClient(NamespacedClient):
    @query_params()
    def deprecations(self, index=None, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/migration-api-deprecation.html>`_

        :arg index: Index pattern
        """
        return self.transport.perform_request(
            "GET",
            _make_path(index, "_migration", "deprecations"),
            params=params,
            headers=headers,
        )

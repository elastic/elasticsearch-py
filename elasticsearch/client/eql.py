from .utils import NamespacedClient, SKIP_IN_PATH, query_params, _make_path


class EqlClient(NamespacedClient):
    @query_params()
    def search(self, index, body, params=None, headers=None):
        """
        Returns results matching a query expressed in Event Query Language (EQL)
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/eql.html>`_

        :arg index: The name of the index to scope the operation
        :arg body: Eql request body. Use the `query` to limit the query
            scope.
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "POST",
            _make_path(index, "_eql", "search"),
            params=params,
            headers=headers,
            body=body,
        )

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class SqlClient(NamespacedClient):
    @query_params()
    def clear_cursor(self, body, params=None):
        """
        `<Clear SQL cursor>`_

        :arg body: Specify the cursor value in the `cursor` element to
            clean the cursor.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST", "/_sql/close", params=params, body=body
        )

    @query_params("format")
    def query(self, body, params=None):
        """
        `<Execute SQL>`_

        :arg body: Use the `query` element to start a query. Use the
            `cursor` element to continue a query.
        :arg format: a short version of the Accept header, e.g. json,
            yaml
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request("POST", "/_sql", params=params, body=body)

    @query_params()
    def translate(self, body, params=None):
        """
        `<Translate SQL into Elasticsearch queries>`_

        :arg body: Specify the query in the `query` element.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST", "/_sql/translate", params=params, body=body
        )

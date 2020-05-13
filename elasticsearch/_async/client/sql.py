# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params, SKIP_IN_PATH


class SqlClient(NamespacedClient):
    @query_params()
    async def clear_cursor(self, body, params=None, headers=None):
        """
        Clears the SQL cursor
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/sql-pagination.html>`_

        :arg body: Specify the cursor value in the `cursor` element to
            clean the cursor.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST", "/_sql/close", params=params, headers=headers, body=body
        )

    @query_params("format")
    async def query(self, body, params=None, headers=None):
        """
        Executes a SQL request
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/sql-rest-overview.html>`_

        :arg body: Use the `query` element to start a query. Use the
            `cursor` element to continue a query.
        :arg format: a short version of the Accept header, e.g. json,
            yaml
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST", "/_sql", params=params, headers=headers, body=body
        )

    @query_params()
    async def translate(self, body, params=None, headers=None):
        """
        Translates SQL into Elasticsearch queries
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/sql-translate.html>`_

        :arg body: Specify the query in the `query` element.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST", "/_sql/translate", params=params, headers=headers, body=body
        )

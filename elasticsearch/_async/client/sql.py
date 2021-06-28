#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from .utils import SKIP_IN_PATH, NamespacedClient, query_params


class SqlClient(NamespacedClient):
    @query_params()
    async def clear_cursor(self, body, params=None, headers=None):
        """
        Clears the SQL cursor

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/sql-pagination.html>`_

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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/sql-rest-overview.html>`_

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

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.13/sql-translate.html>`_

        :arg body: Specify the query in the `query` element.
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST", "/_sql/translate", params=params, headers=headers, body=body
        )

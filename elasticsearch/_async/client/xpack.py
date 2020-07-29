# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params


class XPackClient(NamespacedClient):
    def __getattr__(self, attr_name):
        return getattr(self.client, attr_name)

    # AUTO-GENERATED-API-DEFINITIONS #
    @query_params("accept_enterprise", "categories")
    async def info(self, params=None, headers=None):
        """
        Retrieves information about the installed X-Pack features.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/info-api.html>`_

        :arg accept_enterprise: If an enterprise license is installed,
            return the type and mode as 'enterprise' (default: false)
        :arg categories: Comma-separated list of info categories. Can be
            any of: build, license, features
        """
        return await self.transport.perform_request(
            "GET", "/_xpack", params=params, headers=headers
        )

    @query_params("master_timeout")
    async def usage(self, params=None, headers=None):
        """
        Retrieves usage information about the installed X-Pack features.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/usage-api.html>`_

        :arg master_timeout: Specify timeout for watch write operation
        """
        return await self.transport.perform_request(
            "GET", "/_xpack/usage", params=params, headers=headers
        )

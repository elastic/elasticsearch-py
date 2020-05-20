# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params


class RemoteClient(NamespacedClient):
    @query_params()
    async def info(self, params=None, headers=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/7.x/cluster-remote-info.html>`_
        """
        return await self.transport.perform_request(
            "GET", "/_remote/info", params=params, headers=headers
        )

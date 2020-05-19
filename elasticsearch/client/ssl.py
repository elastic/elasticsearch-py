# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params


class SslClient(NamespacedClient):
    @query_params()
    def certificates(self, params=None, headers=None):
        """
        Retrieves information about the X.509 certificates used to encrypt
        communications in the cluster.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/security-api-ssl.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_ssl/certificates", params=params, headers=headers
        )

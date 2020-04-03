from .utils import NamespacedClient, query_params


class SslClient(NamespacedClient):
    @query_params()
    def certificates(self, params=None, headers=None):
        """
        Retrieves information about the X.509 certificates used to encrypt
        communications in the cluster.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-ssl.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_ssl/certificates", params=params, headers=headers
        )

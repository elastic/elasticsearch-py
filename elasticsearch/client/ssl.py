from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class SslClient(NamespacedClient):
    @query_params()
    def certificates(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-ssl.html>`_

        """
        return self.transport.perform_request(
            "GET", "/_ssl/certificates", params=params
        )

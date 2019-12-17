from .utils import NamespacedClient, query_params


class XPackClient(NamespacedClient):
    def __getattr__(self, attr_name):
        return getattr(self.client, attr_name)

    # AUTO-GENERATED-API-DEFINITIONS #
    @query_params("categories")
    def info(self, params=None):
        """
        Retrieve information about xpack, including build number/timestamp and license
        status
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/info-api.html>`_

        :arg categories: Comma-separated list of info categories. Can be
            any of: build, license, features
        """
        return self.transport.perform_request("GET", "/_xpack", params=params)

    @query_params("master_timeout")
    def usage(self, params=None):
        """
        Retrieve information about xpack features usage          :arg master_timeout:
        Specify timeout for watch write operation
        `<Retrieve information about xpack features usage>`_

        :arg master_timeout: Specify timeout for watch write operation
        """
        return self.transport.perform_request("GET", "/_xpack/usage", params=params)

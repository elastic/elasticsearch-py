from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class EnrichClient(NamespacedClient):
    @query_params()
    def delete_policy(self, name, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-delete-policy.html>`_

        :arg name: The name of the enrich policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_enrich", "policy", name),
            params=params,
            headers=headers,
        )

    @query_params("wait_for_completion")
    def execute_policy(self, name, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-execute-policy.html>`_

        :arg name: The name of the enrich policy
        :arg wait_for_completion: Should the request should block until
            the execution is complete.  Default: True
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_enrich", "policy", name, "_execute"),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_policy(self, name=None, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-get-policy.html>`_

        :arg name: A comma-separated list of enrich policy names
        """
        return self.transport.perform_request(
            "GET", _make_path("_enrich", "policy", name), params=params, headers=headers
        )

    @query_params()
    def put_policy(self, name, body, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-put-policy.html>`_

        :arg name: The name of the enrich policy
        :arg body: The enrich policy to register
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_enrich", "policy", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def stats(self, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-stats.html>`_

        """
        return self.transport.perform_request(
            "GET", "/_enrich/_stats", params=params, headers=headers
        )

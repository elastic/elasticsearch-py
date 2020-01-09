from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class SlmClient(NamespacedClient):
    @query_params()
    def delete_lifecycle(self, policy_id, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-api-delete.html>`_

        :arg policy_id: The id of the snapshot lifecycle policy to
            remove
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy_id'.")

        return self.transport.perform_request(
            "DELETE", _make_path("_slm", "policy", policy_id), params=params
        )

    @query_params()
    def execute_lifecycle(self, policy_id, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-api-execute.html>`_

        :arg policy_id: The id of the snapshot lifecycle policy to be
            executed
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy_id'.")

        return self.transport.perform_request(
            "PUT", _make_path("_slm", "policy", policy_id, "_execute"), params=params
        )

    @query_params()
    def execute_retention(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-api-execute-retention.html>`_

        """
        return self.transport.perform_request(
            "POST", "/_slm/_execute_retention", params=params
        )

    @query_params()
    def get_lifecycle(self, policy_id=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-api-get.html>`_

        :arg policy_id: Comma-separated list of snapshot lifecycle
            policies to retrieve
        """
        return self.transport.perform_request(
            "GET", _make_path("_slm", "policy", policy_id), params=params
        )

    @query_params()
    def get_stats(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/slm-get-stats.html>`_

        """
        return self.transport.perform_request("GET", "/_slm/stats", params=params)

    @query_params()
    def put_lifecycle(self, policy_id, body=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-api-put.html>`_

        :arg policy_id: The id of the snapshot lifecycle policy
        :arg body: The snapshot lifecycle policy definition to register
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy_id'.")

        return self.transport.perform_request(
            "PUT", _make_path("_slm", "policy", policy_id), params=params, body=body
        )

    @query_params()
    def get_status(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-get-status.html>`_

        """
        return self.transport.perform_request("GET", "/_slm/status", params=params)

    @query_params()
    def start(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-start.html>`_

        """
        return self.transport.perform_request("POST", "/_slm/start", params=params)

    @query_params()
    def stop(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/slm-stop.html>`_

        """
        return self.transport.perform_request("POST", "/_slm/stop", params=params)

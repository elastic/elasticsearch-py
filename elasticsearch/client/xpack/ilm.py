from ..utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class IlmClient(NamespacedClient):
    @query_params()
    def delete_lifecycle(self, policy=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-delete-lifecycle.html>`_

        :arg policy: The name of the index lifecycle policy
        """
        return self.transport.perform_request(
            "DELETE", _make_path("_ilm", "policy", policy), params=params
        )

    @query_params("human")
    def explain_lifecycle(self, index=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-explain-lifecycle.html>`_

        :arg index: The name of the index to explain
        :arg human: Return data such as dates in a human readable format,
            default 'false'
        """
        return self.transport.perform_request(
            "GET", _make_path(index, "_ilm", "explain"), params=params
        )

    @query_params()
    def get_lifecycle(self, policy=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-get-lifecycle.html>`_

        :arg policy: The name of the index lifecycle policy
        """
        return self.transport.perform_request(
            "GET", _make_path("_ilm", "policy", policy), params=params
        )

    @query_params()
    def get_status(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-get-status.html>`_
        """
        return self.transport.perform_request("GET", "/_ilm/status", params=params)

    @query_params()
    def move_to_step(self, index=None, body=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-move-to-step.html>`_

        :arg index: The name of the index whose lifecycle step is to change
        :arg body: The new lifecycle step to move to
        """
        return self.transport.perform_request(
            "POST", _make_path("_ilm", "move", index), params=params, body=body
        )

    @query_params()
    def put_lifecycle(self, policy=None, body=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-put-lifecycle.html>`_

        :arg policy: The name of the index lifecycle policy
        :arg body: The lifecycle policy definition to register
        """
        return self.transport.perform_request(
            "PUT", _make_path("_ilm", "policy", policy), params=params, body=body
        )

    @query_params()
    def remove_policy(self, index=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-remove-policy.html>`_

        :arg index: The name of the index to remove policy on
        """
        return self.transport.perform_request(
            "POST", _make_path(index, "_ilm", "remove"), params=params
        )

    @query_params()
    def retry(self, index=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-retry-policy.html>`_

        :arg index: The name of the indices (comma-separated) whose failed
            lifecycle step is to be retry
        """
        return self.transport.perform_request(
            "POST", _make_path(index, "_ilm", "retry"), params=params
        )

    @query_params()
    def start(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-start.html>`_
        """
        return self.transport.perform_request("POST", "/_ilm/start", params=params)

    @query_params()
    def stop(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-stop.html>`_
        """
        return self.transport.perform_request("POST", "/_ilm/stop", params=params)

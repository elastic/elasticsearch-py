from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class IlmClient(NamespacedClient):
    @query_params()
    def delete_lifecycle(self, policy, params=None, headers=None):
        """
        Deletes the specified lifecycle policy definition. A currently used policy
        cannot be deleted.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-delete-lifecycle.html>`_

        :arg policy: The name of the index lifecycle policy
        """
        if policy in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ilm", "policy", policy),
            params=params,
            headers=headers,
        )

    @query_params("only_errors", "only_managed")
    def explain_lifecycle(self, index, params=None, headers=None):
        """
        Retrieves information about the index's current lifecycle state, such as the
        currently executing phase, action, and step.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-explain-lifecycle.html>`_

        :arg index: The name of the index to explain
        :arg only_errors: filters the indices included in the response
            to ones in an ILM error state, implies only_managed
        :arg only_managed: filters the indices included in the response
            to ones managed by ILM
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "GET", _make_path(index, "_ilm", "explain"), params=params, headers=headers
        )

    @query_params()
    def get_lifecycle(self, policy=None, params=None, headers=None):
        """
        Returns the specified policy definition. Includes the policy version and last
        modified date.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-get-lifecycle.html>`_

        :arg policy: The name of the index lifecycle policy
        """
        return self.transport.perform_request(
            "GET", _make_path("_ilm", "policy", policy), params=params, headers=headers
        )

    @query_params()
    def get_status(self, params=None, headers=None):
        """
        Retrieves the current index lifecycle management (ILM) status.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-get-status.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_ilm/status", params=params, headers=headers
        )

    @query_params()
    def move_to_step(self, index, body=None, params=None, headers=None):
        """
        Manually moves an index into the specified step and executes that step.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-move-to-step.html>`_

        :arg index: The name of the index whose lifecycle step is to
            change
        :arg body: The new lifecycle step to move to
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ilm", "move", index),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def put_lifecycle(self, policy, body=None, params=None, headers=None):
        """
        Creates a lifecycle policy
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-put-lifecycle.html>`_

        :arg policy: The name of the index lifecycle policy
        :arg body: The lifecycle policy definition to register
        """
        if policy in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ilm", "policy", policy),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def remove_policy(self, index, params=None, headers=None):
        """
        Removes the assigned lifecycle policy and stops managing the specified index
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-remove-policy.html>`_

        :arg index: The name of the index to remove policy on
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "POST", _make_path(index, "_ilm", "remove"), params=params, headers=headers
        )

    @query_params()
    def retry(self, index, params=None, headers=None):
        """
        Retries executing the policy for an index that is in the ERROR step.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-retry-policy.html>`_

        :arg index: The name of the indices (comma-separated) whose
            failed lifecycle step is to be retry
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "POST", _make_path(index, "_ilm", "retry"), params=params, headers=headers
        )

    @query_params()
    def start(self, params=None, headers=None):
        """
        Start the index lifecycle management (ILM) plugin.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-start.html>`_
        """
        return self.transport.perform_request(
            "POST", "/_ilm/start", params=params, headers=headers
        )

    @query_params()
    def stop(self, params=None, headers=None):
        """
        Halts all lifecycle management operations and stops the index lifecycle
        management (ILM) plugin
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-stop.html>`_
        """
        return self.transport.perform_request(
            "POST", "/_ilm/stop", params=params, headers=headers
        )

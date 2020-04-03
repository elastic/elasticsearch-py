from .utils import NamespacedClient, query_params, SKIP_IN_PATH, _make_path


class AutoscalingClient(NamespacedClient):
    @query_params()
    def get_autoscaling_decision(self, params=None, headers=None):
        """
        Gets the current autoscaling decision based on the configured autoscaling
        policy, indicating whether or not autoscaling is needed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-get-autoscaling-decision.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_autoscaling/decision", params=params, headers=headers
        )

    @query_params()
    def delete_autoscaling_policy(self, name, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-delete-autoscaling-policy.html>`_

        :arg name: the name of the autoscaling policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_autoscaling", "policy", name),
            params=params,
            headers=headers,
        )

    @query_params()
    def put_autoscaling_policy(self, name, body, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-put-autoscaling-policy.html>`_

        :arg name: the name of the autoscaling policy
        :arg body: the specification of the autoscaling policy
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_autoscaling", "policy", name),
            params=params,
            headers=headers,
            body=body,
        )

from .utils import NamespacedClient, query_params


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

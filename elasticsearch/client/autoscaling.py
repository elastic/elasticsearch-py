from .utils import NamespacedClient, query_params


class AutoscalingClient(NamespacedClient):
    @query_params()
    def get_autoscaling_decision(self, params=None, headers=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-get-autoscaling-decision.html>`_

        """
        return self.transport.perform_request(
            "GET", "/_autoscaling/decision", params=params, headers=headers
        )

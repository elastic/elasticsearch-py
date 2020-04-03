from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH, _bulk_body


class MonitoringClient(NamespacedClient):
    @query_params("interval", "system_api_version", "system_id")
    def bulk(self, body, doc_type=None, params=None, headers=None):
        """
        Used by the monitoring features to send monitoring data.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/monitor-elasticsearch-cluster.html>`_

        :arg body: The operation definition and data (action-data
            pairs), separated by newlines
        :arg doc_type: Default document type for items which don't
            provide one
        :arg interval: Collection interval (e.g., '10s' or '10000ms') of
            the payload
        :arg system_api_version: API Version of the monitored system
        :arg system_id: Identifier of the monitored system
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        body = _bulk_body(self.transport.serializer, body)
        return self.transport.perform_request(
            "POST",
            _make_path("_monitoring", doc_type, "bulk"),
            params=params,
            headers=headers,
            body=body,
        )

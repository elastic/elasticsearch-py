from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class IngestClient(NamespacedClient):
    @query_params("master_timeout")
    def get_pipeline(self, id=None, params=None, headers=None):
        """
        Returns a pipeline.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/get-pipeline-api.html>`_

        :arg id: Comma separated list of pipeline ids. Wildcards
            supported
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        return self.transport.perform_request(
            "GET", _make_path("_ingest", "pipeline", id), params=params, headers=headers
        )

    @query_params("master_timeout", "timeout")
    def put_pipeline(self, id, body, params=None, headers=None):
        """
        Creates or updates a pipeline.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/put-pipeline-api.html>`_

        :arg id: Pipeline ID
        :arg body: The ingest definition
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_ingest", "pipeline", id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("master_timeout", "timeout")
    def delete_pipeline(self, id, params=None, headers=None):
        """
        Deletes a pipeline.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/delete-pipeline-api.html>`_

        :arg id: Pipeline ID
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg timeout: Explicit operation timeout
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_ingest", "pipeline", id),
            params=params,
            headers=headers,
        )

    @query_params("verbose")
    def simulate(self, body, id=None, params=None, headers=None):
        """
        Allows to simulate a pipeline with example documents.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/simulate-pipeline-api.html>`_

        :arg body: The simulate definition
        :arg id: Pipeline ID
        :arg verbose: Verbose mode. Display data output for each
            processor in executed pipeline
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return self.transport.perform_request(
            "POST",
            _make_path("_ingest", "pipeline", id, "_simulate"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def processor_grok(self, params=None, headers=None):
        """
        Returns a list of the built-in patterns.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/grok-processor.html#grok-processor-rest-get>`_
        """
        return self.transport.perform_request(
            "GET", "/_ingest/processor/grok", params=params, headers=headers
        )

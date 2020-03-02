from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class RollupClient(NamespacedClient):
    @query_params()
    def delete_job(self, id, params=None):
        """

        :arg id: The ID of the job to delete
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "DELETE", _make_path("_rollup", "job", id), params=params
        )

    @query_params()
    def get_jobs(self, id=None, params=None):
        """

        :arg id: The ID of the job(s) to fetch. Accepts glob patterns,
            or left blank for all jobs
        """
        return self.transport.perform_request(
            "GET", _make_path("_rollup", "job", id), params=params
        )

    @query_params()
    def get_rollup_caps(self, id=None, params=None):
        """

        :arg id: The ID of the index to check rollup capabilities on, or
            left blank for all jobs
        """
        return self.transport.perform_request(
            "GET", _make_path("_rollup", "data", id), params=params
        )

    @query_params()
    def get_rollup_index_caps(self, index, params=None):
        """

        :arg index: The rollup index or index pattern to obtain rollup
            capabilities from.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "GET", _make_path(index, "_rollup", "data"), params=params
        )

    @query_params()
    def put_job(self, id, body, params=None):
        """

        :arg id: The ID of the job to create
        :arg body: The job configuration
        """
        for param in (id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT", _make_path("_rollup", "job", id), params=params, body=body
        )

    @query_params("rest_total_hits_as_int", "typed_keys")
    def rollup_search(self, index, body, doc_type=None, params=None):
        """

        :arg index: The indices or index-pattern(s) (containing rollup
            or regular data) that should be searched
        :arg body: The search request body
        :arg doc_type: The doc type inside the index
        :arg rest_total_hits_as_int: Indicates whether hits.total should
            be rendered as an integer or an object in the rest search response
        :arg typed_keys: Specify whether aggregation and suggester names
            should be prefixed by their respective types in the response
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "GET",
            _make_path(index, doc_type, "_rollup_search"),
            params=params,
            body=body,
        )

    @query_params()
    def start_job(self, id, params=None):
        """

        :arg id: The ID of the job to start
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "POST", _make_path("_rollup", "job", id, "_start"), params=params
        )

    @query_params("timeout", "wait_for_completion")
    def stop_job(self, id, params=None):
        """

        :arg id: The ID of the job to stop
        :arg timeout: Block for (at maximum) the specified duration
            while waiting for the job to stop.  Defaults to 30s.
        :arg wait_for_completion: True if the API should block until the
            job has fully stopped, false if should be executed async. Defaults to
            false.
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "POST", _make_path("_rollup", "job", id, "_stop"), params=params
        )

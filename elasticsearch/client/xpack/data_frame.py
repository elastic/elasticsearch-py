from ..utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class Data_FrameClient(NamespacedClient):
    @query_params()
    def delete_data_frame_transform(self, transform_id, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/delete-data-frame-transform.html>`_

        :arg transform_id: The id of the transform to delete
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'transform_id'."
            )
        return self.transport.perform_request(
            "DELETE",
            _make_path("_data_frame", "transforms", transform_id),
            params=params,
        )

    @query_params("from_", "size")
    def get_data_frame_transform(self, transform_id=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/get-data-frame-transform.html>`_

        :arg transform_id: The id or comma delimited list of id expressions of
            the transforms to get, '_all' or '*' implies get all transforms
        :arg from_: skips a number of transform configs, defaults to 0
        :arg size: specifies a max number of transforms to get, defaults to 100
        """
        return self.transport.perform_request(
            "GET", _make_path("_data_frame", "transforms", transform_id), params=params
        )

    @query_params()
    def get_data_frame_transform_stats(self, transform_id=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/get-data-frame-transform-stats.html>`_

        :arg transform_id: The id of the transform for which to get stats.
            '_all' or '*' implies all transforms
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_data_frame", "transforms", transform_id, "_stats"),
            params=params,
        )

    @query_params()
    def preview_data_frame_transform(self, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/preview-data-frame-transform.html>`_

        :arg body: The definition for the data_frame transform to preview
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")
        return self.transport.perform_request(
            "POST", "/_data_frame/transforms/_preview", params=params, body=body
        )

    @query_params()
    def put_data_frame_transform(self, transform_id, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/put-data-frame-transform.html>`_

        :arg transform_id: The id of the new transform.
        :arg body: The data frame transform definition
        """
        for param in (transform_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT",
            _make_path("_data_frame", "transforms", transform_id),
            params=params,
            body=body,
        )

    @query_params("timeout")
    def start_data_frame_transform(self, transform_id, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/start-data-frame-transform.html>`_

        :arg transform_id: The id of the transform to start
        :arg timeout: Controls the time to wait for the transform to start
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'transform_id'."
            )
        return self.transport.perform_request(
            "POST",
            _make_path("_data_frame", "transforms", transform_id, "_start"),
            params=params,
        )

    @query_params("timeout", "wait_for_completion")
    def stop_data_frame_transform(self, transform_id, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/stop-data-frame-transform.html>`_

        :arg transform_id: The id of the transform to stop
        :arg timeout: Controls the time to wait until the transform has stopped.
            Default to 30 seconds
        :arg wait_for_completion: Whether to wait for the transform to fully
            stop before returning or not. Default to false
        """
        if transform_id in SKIP_IN_PATH:
            raise ValueError(
                "Empty value passed for a required argument 'transform_id'."
            )
        return self.transport.perform_request(
            "POST",
            _make_path("_data_frame", "transforms", transform_id, "_stop"),
            params=params,
        )

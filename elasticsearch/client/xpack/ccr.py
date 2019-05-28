from ..utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class CcrClient(NamespacedClient):
    @query_params()
    def delete_auto_follow_pattern(self, name, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-delete-auto-follow-pattern.html>`_

        :arg name: The name of the auto follow pattern.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")
        return self.transport.perform_request(
            "DELETE", _make_path("_ccr", "auto_follow", name), params=params
        )

    @query_params("wait_for_active_shards")
    def follow(self, index, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-put-follow.html>`_

        :arg index: The name of the follower index
        :arg body: The name of the leader index and other optional ccr related
            parameters
        :arg wait_for_active_shards: Sets the number of shard copies that must
            be active before returning. Defaults to 0. Set to `all` for all
            shard copies, otherwise set to any non-negative value less than or
            equal to the total number of copies for the shard (number of
            replicas + 1), default '0'
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT", _make_path(index, "_ccr", "follow"), params=params, body=body
        )

    @query_params()
    def follow_info(self, index=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-follow-info.html>`_

        :arg index: A comma-separated list of index patterns; use `_all` to
            perform the operation on all indices
        """
        return self.transport.perform_request(
            "GET", _make_path(index, "_ccr", "info"), params=params
        )

    @query_params()
    def follow_stats(self, index=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-follow-stats.html>`_

        :arg index: A comma-separated list of index patterns; use `_all` to
            perform the operation on all indices
        """
        return self.transport.perform_request(
            "GET", _make_path(index, "_ccr", "stats"), params=params
        )

    @query_params()
    def forget_follower(self, index, body, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        :arg index: the name of the leader index for which specified follower
            retention leases should be removed
        :arg body: the name and UUID of the follower index, the name of the
            cluster containing the follower index, and the alias from the
            perspective of that cluster for the remote cluster containing the
            leader index
        """
        for param in (index, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "POST",
            _make_path(index, "_ccr", "forget_follower"),
            params=params,
            body=body,
        )

    @query_params()
    def get_auto_follow_pattern(self, name=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-auto-follow-pattern.html>`_

        :arg name: The name of the auto follow pattern.
        """
        return self.transport.perform_request(
            "GET", _make_path("_ccr", "auto_follow", name), params=params
        )

    @query_params()
    def pause_follow(self, index, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-pause-follow.html>`_

        :arg index: The name of the follower index that should pause following
            its leader index.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")
        return self.transport.perform_request(
            "POST", _make_path(index, "_ccr", "pause_follow"), params=params
        )

    @query_params()
    def put_auto_follow_pattern(self, name, body, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-put-auto-follow-pattern.html>`_

        :arg name: The name of the auto follow pattern.
        :arg body: The specification of the auto follow pattern
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")
        return self.transport.perform_request(
            "PUT", _make_path("_ccr", "auto_follow", name), params=params, body=body
        )

    @query_params()
    def resume_follow(self, index, body=None, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-post-resume-follow.html>`_

        :arg index: The name of the follow index to resume following.
        :arg body: The name of the leader index and other optional ccr related
            parameters
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")
        return self.transport.perform_request(
            "POST", _make_path(index, "_ccr", "resume_follow"), params=params, body=body
        )

    @query_params()
    def stats(self, params=None):
        """
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-get-stats.html>`_
        """
        return self.transport.perform_request("GET", "/_ccr/stats", params=params)

    @query_params()
    def unfollow(self, index, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        :arg index: The name of the follower index that should be turned into a
            regular index.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")
        return self.transport.perform_request(
            "POST", _make_path(index, "_ccr", "unfollow"), params=params
        )

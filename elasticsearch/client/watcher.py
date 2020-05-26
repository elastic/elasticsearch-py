from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class WatcherClient(NamespacedClient):
    @query_params()
    def ack_watch(self, watch_id, action_id=None, params=None, headers=None):
        """
        Acknowledges a watch, manually throttling the execution of the watch's actions.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-ack-watch.html>`_

        :arg watch_id: Watch ID
        :arg action_id: A comma-separated list of the action ids to be
            acked
        """
        if watch_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'watch_id'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_watcher", "watch", watch_id, "_ack", action_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def activate_watch(self, watch_id, params=None, headers=None):
        """
        Activates a currently inactive watch.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-activate-watch.html>`_

        :arg watch_id: Watch ID
        """
        if watch_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'watch_id'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_watcher", "watch", watch_id, "_activate"),
            params=params,
            headers=headers,
        )

    @query_params()
    def deactivate_watch(self, watch_id, params=None, headers=None):
        """
        Deactivates a currently active watch.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-deactivate-watch.html>`_

        :arg watch_id: Watch ID
        """
        if watch_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'watch_id'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_watcher", "watch", watch_id, "_deactivate"),
            params=params,
            headers=headers,
        )

    @query_params()
    def delete_watch(self, id, params=None, headers=None):
        """
        Removes a watch from Watcher.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-delete-watch.html>`_

        :arg id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_watcher", "watch", id),
            params=params,
            headers=headers,
        )

    @query_params("debug")
    def execute_watch(self, body=None, id=None, params=None, headers=None):
        """
        Forces the execution of a stored watch.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-execute-watch.html>`_

        :arg body: Execution control
        :arg id: Watch ID
        :arg debug: indicates whether the watch should execute in debug
            mode
        """
        return self.transport.perform_request(
            "PUT",
            _make_path("_watcher", "watch", id, "_execute"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_watch(self, id, params=None, headers=None):
        """
        Retrieves a watch by its ID.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-get-watch.html>`_

        :arg id: Watch ID
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "GET", _make_path("_watcher", "watch", id), params=params, headers=headers
        )

    @query_params("active", "if_primary_term", "if_seq_no", "version")
    def put_watch(self, id, body=None, params=None, headers=None):
        """
        Creates a new watch, or updates an existing one.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-put-watch.html>`_

        :arg id: Watch ID
        :arg body: The watch
        :arg active: Specify whether the watch is in/active by default
        :arg if_primary_term: only update the watch if the last
            operation that has changed the watch has the specified primary term
        :arg if_seq_no: only update the watch if the last operation that
            has changed the watch has the specified sequence number
        :arg version: Explicit version number for concurrency control
        """
        if id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'id'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_watcher", "watch", id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def start(self, params=None, headers=None):
        """
        Starts Watcher if it is not already running.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-start.html>`_
        """
        return self.transport.perform_request(
            "POST", "/_watcher/_start", params=params, headers=headers
        )

    @query_params("emit_stacktraces")
    def stats(self, metric=None, params=None, headers=None):
        """
        Retrieves the current Watcher metrics.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-stats.html>`_

        :arg metric: Controls what additional stat metrics should be
            include in the response   Valid choices: _all, queued_watches,
            current_watches, pending_watches
        :arg emit_stacktraces: Emits stack traces of currently running
            watches
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_watcher", "stats", metric),
            params=params,
            headers=headers,
        )

    @query_params()
    def stop(self, params=None, headers=None):
        """
        Stops Watcher if it is running.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api-stop.html>`_
        """
        return self.transport.perform_request(
            "POST", "/_watcher/_stop", params=params, headers=headers
        )

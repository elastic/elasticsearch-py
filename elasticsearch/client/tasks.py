import warnings
from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class TasksClient(NamespacedClient):
    @query_params(
        "actions",
        "detailed",
        "group_by",
        "nodes",
        "parent_task_id",
        "timeout",
        "wait_for_completion",
    )
    def list(self, params=None, headers=None):
        """
        Returns a list of tasks.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/tasks.html>`_

        :arg actions: A comma-separated list of actions that should be
            returned. Leave empty to return all.
        :arg detailed: Return detailed task information (default: false)
        :arg group_by: Group tasks by nodes or parent/child
            relationships  Valid choices: nodes, parents, none  Default: nodes
        :arg nodes: A comma-separated list of node IDs or names to limit
            the returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from all nodes
        :arg parent_task_id: Return tasks with specified parent task id
            (node_id:task_number). Set to -1 to return all.
        :arg timeout: Explicit operation timeout
        :arg wait_for_completion: Wait for the matching tasks to
            complete (default: false)
        """
        return self.transport.perform_request(
            "GET", "/_tasks", params=params, headers=headers
        )

    @query_params("actions", "nodes", "parent_task_id")
    def cancel(self, task_id=None, params=None, headers=None):
        """
        Cancels a task, if it can be cancelled through an API.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/tasks.html>`_

        :arg task_id: Cancel the task with specified task id
            (node_id:task_number)
        :arg actions: A comma-separated list of actions that should be
            cancelled. Leave empty to cancel all.
        :arg nodes: A comma-separated list of node IDs or names to limit
            the returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from all nodes
        :arg parent_task_id: Cancel tasks with specified parent task id
            (node_id:task_number). Set to -1 to cancel all.
        """
        return self.transport.perform_request(
            "POST",
            _make_path("_tasks", task_id, "_cancel"),
            params=params,
            headers=headers,
        )

    @query_params("timeout", "wait_for_completion")
    def get(self, task_id=None, params=None, headers=None):
        """
        Returns information about a task.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/master/tasks.html>`_

        :arg task_id: Return the task with specified id
            (node_id:task_number)
        :arg timeout: Explicit operation timeout
        :arg wait_for_completion: Wait for the matching tasks to
            complete (default: false)
        """
        if task_id in SKIP_IN_PATH:
            warnings.warn(
                "Calling client.tasks.get() without a task_id is deprecated "
                "and will be removed in v8.0. Use client.tasks.list() instead.",
                DeprecationWarning,
            )

        return self.transport.perform_request(
            "GET", _make_path("_tasks", task_id), params=params, headers=headers
        )

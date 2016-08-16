from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH

class TasksClient(NamespacedClient):
    @query_params('actions', 'node_id', 'parent_node', 'parent_task')
    def cancel(self, task_id=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/tasks-cancel.html>`_

        :arg task_id: Cancel the task with specified id
        :arg actions: A comma-separated list of actions that should be
            cancelled. Leave empty to cancel all.
        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from all
            nodes
        :arg parent_node: Cancel tasks with specified parent node.
        :arg parent_task: Cancel tasks with specified parent task id
            (node_id:task_number). Set to -1 to cancel all.
        """
        return self.transport.perform_request('POST', _make_path('_tasks',
            task_id, '_cancel'), params=params)

    @query_params('actions', 'detailed', 'node_id', 'parent_node',
        'parent_task', 'wait_for_completion')
    def list(self, task_id=None, params=None):
        """
        `<http://www.elastic.co/guide/en/elasticsearch/reference/current/tasks-list.html>`_

        :arg task_id: Return the task with specified id (node_id:task_number)
        :arg actions: A comma-separated list of actions that should be returned.
            Leave empty to return all.
        :arg detailed: Return detailed task information (default: false)
        :arg node_id: A comma-separated list of node IDs or names to limit the
            returned information; use `_local` to return information from the
            node you're connecting to, leave empty to get information from all
            nodes
        :arg parent_node: Return tasks with specified parent node.
        :arg parent_task: Return tasks with specified parent task id
            (node_id:task_number). Set to -1 to return all.
        :arg wait_for_completion: Wait for the matching tasks to complete
            (default: false)
        """
        return self.transport.perform_request('GET', _make_path('_tasks',
            task_id), params=params)


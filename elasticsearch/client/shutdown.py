#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from .utils import SKIP_IN_PATH, NamespacedClient, _make_path, query_params


class ShutdownClient(NamespacedClient):
    @query_params()
    def delete_node(self, node_id, params=None, headers=None):
        """
        Removes a node from the shutdown list

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg node_id: The node id of node to be removed from the
            shutdown state
        """
        if node_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'node_id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_nodes", node_id, "shutdown"),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_node(self, node_id=None, params=None, headers=None):
        """
        Retrieve status of a node or nodes that are currently marked as shutting down

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg node_id: Which node for which to retrieve the shutdown
            status
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_nodes", node_id, "shutdown"),
            params=params,
            headers=headers,
        )

    @query_params()
    def put_node(self, node_id, body, params=None, headers=None):
        """
        Adds a node to be shut down

        `<https://www.elastic.co/guide/en/elasticsearch/reference/current>`_

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg node_id: The node id of node to be shut down
        :arg body: The shutdown type definition to register
        """
        for param in (node_id, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_nodes", node_id, "shutdown"),
            params=params,
            headers=headers,
            body=body,
        )

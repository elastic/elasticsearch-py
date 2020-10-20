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

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class SlmClient(NamespacedClient):
    @query_params()
    def delete_lifecycle(self, policy_id, params=None, headers=None):
        """
        Deletes an existing snapshot lifecycle policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-delete-policy.html>`_

        :arg policy_id: The id of the snapshot lifecycle policy to
            remove
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy_id'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_slm", "policy", policy_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def execute_lifecycle(self, policy_id, params=None, headers=None):
        """
        Immediately creates a snapshot according to the lifecycle policy, without
        waiting for the scheduled time.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-execute-lifecycle.html>`_

        :arg policy_id: The id of the snapshot lifecycle policy to be
            executed
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy_id'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_slm", "policy", policy_id, "_execute"),
            params=params,
            headers=headers,
        )

    @query_params()
    def execute_retention(self, params=None, headers=None):
        """
        Deletes any snapshots that are expired according to the policy's retention
        rules.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-execute-retention.html>`_
        """
        return self.transport.perform_request(
            "POST", "/_slm/_execute_retention", params=params, headers=headers
        )

    @query_params()
    def get_lifecycle(self, policy_id=None, params=None, headers=None):
        """
        Retrieves one or more snapshot lifecycle policy definitions and information
        about the latest snapshot attempts.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-get-policy.html>`_

        :arg policy_id: Comma-separated list of snapshot lifecycle
            policies to retrieve
        """
        return self.transport.perform_request(
            "GET",
            _make_path("_slm", "policy", policy_id),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_stats(self, params=None, headers=None):
        """
        Returns global and policy-level statistics about actions taken by snapshot
        lifecycle management.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-get-stats.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_slm/stats", params=params, headers=headers
        )

    @query_params()
    def put_lifecycle(self, policy_id, body=None, params=None, headers=None):
        """
        Creates or updates a snapshot lifecycle policy.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-put-policy.html>`_

        :arg policy_id: The id of the snapshot lifecycle policy
        :arg body: The snapshot lifecycle policy definition to register
        """
        if policy_id in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'policy_id'.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_slm", "policy", policy_id),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    def get_status(self, params=None, headers=None):
        """
        Retrieves the status of snapshot lifecycle management (SLM).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-get-status.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_slm/status", params=params, headers=headers
        )

    @query_params()
    def start(self, params=None, headers=None):
        """
        Turns on snapshot lifecycle management (SLM).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-start.html>`_
        """
        return self.transport.perform_request(
            "POST", "/_slm/start", params=params, headers=headers
        )

    @query_params()
    def stop(self, params=None, headers=None):
        """
        Turns off snapshot lifecycle management (SLM).

        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.10/slm-api-stop.html>`_
        """
        return self.transport.perform_request(
            "POST", "/_slm/stop", params=params, headers=headers
        )

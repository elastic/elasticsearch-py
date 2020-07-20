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

from .utils import NamespacedClient, query_params, SKIP_IN_PATH, _make_path


class AutoscalingClient(NamespacedClient):
    @query_params()
    def get_autoscaling_decision(self, params=None, headers=None):
        """
        Gets the current autoscaling decision based on the configured autoscaling
        policy, indicating whether or not autoscaling is needed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-get-autoscaling-decision.html>`_
        """
        return self.transport.perform_request(
            "GET", "/_autoscaling/decision", params=params, headers=headers
        )

    @query_params()
    def delete_autoscaling_policy(self, name, params=None, headers=None):
        """
        Deletes an autoscaling policy.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-delete-autoscaling-policy.html>`_

        :arg name: the name of the autoscaling policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "DELETE",
            _make_path("_autoscaling", "policy", name),
            params=params,
            headers=headers,
        )

    @query_params()
    def get_autoscaling_policy(self, name, params=None, headers=None):
        """
        Retrieves an autoscaling policy.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-get-autoscaling-policy.html>`_

        :arg name: the name of the autoscaling policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return self.transport.perform_request(
            "GET",
            _make_path("_autoscaling", "policy", name),
            params=params,
            headers=headers,
        )

    @query_params()
    def put_autoscaling_policy(self, name, body, params=None, headers=None):
        """
        Creates a new autoscaling policy.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/autoscaling-put-autoscaling-policy.html>`_

        :arg name: the name of the autoscaling policy
        :arg body: the specification of the autoscaling policy
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return self.transport.perform_request(
            "PUT",
            _make_path("_autoscaling", "policy", name),
            params=params,
            headers=headers,
            body=body,
        )

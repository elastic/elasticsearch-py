# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class EnrichClient(NamespacedClient):
    @query_params()
    async def delete_policy(self, name, params=None, headers=None):
        """
        Deletes an existing enrich policy and its enrich index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/delete-enrich-policy-api.html>`_

        :arg name: The name of the enrich policy
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_enrich", "policy", name),
            params=params,
            headers=headers,
        )

    @query_params("wait_for_completion")
    async def execute_policy(self, name, params=None, headers=None):
        """
        Creates the enrich index for an existing enrich policy.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/execute-enrich-policy-api.html>`_

        :arg name: The name of the enrich policy
        :arg wait_for_completion: Should the request should block until
            the execution is complete.  Default: True
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_enrich", "policy", name, "_execute"),
            params=params,
            headers=headers,
        )

    @query_params()
    async def get_policy(self, name=None, params=None, headers=None):
        """
        Gets information about an enrich policy.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/get-enrich-policy-api.html>`_

        :arg name: A comma-separated list of enrich policy names
        """
        return await self.transport.perform_request(
            "GET", _make_path("_enrich", "policy", name), params=params, headers=headers
        )

    @query_params()
    async def put_policy(self, name, body, params=None, headers=None):
        """
        Creates a new enrich policy.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/put-enrich-policy-api.html>`_

        :arg name: The name of the enrich policy
        :arg body: The enrich policy to register
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_enrich", "policy", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def stats(self, params=None, headers=None):
        """
        Gets enrich coordinator statistics and information about enrich policies that
        are currently executing.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/enrich-stats-api.html>`_
        """
        return await self.transport.perform_request(
            "GET", "/_enrich/_stats", params=params, headers=headers
        )

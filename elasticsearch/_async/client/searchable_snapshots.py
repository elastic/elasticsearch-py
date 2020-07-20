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


class SearchableSnapshotsClient(NamespacedClient):
    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable")
    async def clear_cache(self, index=None, params=None, headers=None):
        """
        Clear the cache of searchable snapshots.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/searchable-snapshots-api-clear-cache.html>`_

        :arg index: A comma-separated list of index name to limit the
            operation
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        """
        return await self.transport.perform_request(
            "POST",
            _make_path(index, "_searchable_snapshots", "cache", "clear"),
            params=params,
            headers=headers,
        )

    @query_params("master_timeout", "wait_for_completion")
    async def mount(self, repository, snapshot, body, params=None, headers=None):
        """
        Mount a snapshot as a searchable index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/searchable-snapshots-api-mount-snapshot.html>`_

        :arg repository: The name of the repository containing the
            snapshot of the index to mount
        :arg snapshot: The name of the snapshot of the index to mount
        :arg body: The restore configuration for mounting the snapshot
            as searchable
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        :arg wait_for_completion: Should this request wait until the
            operation has completed before returning
        """
        for param in (repository, snapshot, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "POST",
            _make_path("_snapshot", repository, snapshot, "_mount"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def repository_stats(self, repository, params=None, headers=None):
        """
        Retrieve usage statistics about a snapshot repository.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/searchable-snapshots-repository-stats.html>`_

        :arg repository: The repository for which to get the stats for
        """
        if repository in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'repository'.")

        return await self.transport.perform_request(
            "GET",
            _make_path("_snapshot", repository, "_stats"),
            params=params,
            headers=headers,
        )

    @query_params()
    async def stats(self, index=None, params=None, headers=None):
        """
        Retrieve various statistics about searchable snapshots.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/current/searchable-snapshots-api-stats.html>`_

        :arg index: A comma-separated list of index names
        """
        return await self.transport.perform_request(
            "GET",
            _make_path(index, "_searchable_snapshots", "stats"),
            params=params,
            headers=headers,
        )

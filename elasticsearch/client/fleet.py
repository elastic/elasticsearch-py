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


class FleetClient(NamespacedClient):
    @query_params("checkpoints", "timeout", "wait_for_advance", "wait_for_index")
    def global_checkpoints(self, index, params=None, headers=None):
        """
        Returns the current global checkpoints for an index. This API is design for
        internal use by the fleet server project.

        .. warning::

            This API is **experimental** so may include breaking changes
            or be removed in a future version

        :arg index: The name of the index.
        :arg checkpoints: Comma separated list of checkpoints
        :arg timeout: Timeout to wait for global checkpoint to advance
            Default: 30s
        :arg wait_for_advance: Whether to wait for the global checkpoint
            to advance past the specified current checkpoints  Default: false
        :arg wait_for_index: Whether to wait for the target index to
            exist and all primary shards be active  Default: false
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return self.transport.perform_request(
            "GET",
            _make_path(index, "_fleet", "global_checkpoints"),
            params=params,
            headers=headers,
        )

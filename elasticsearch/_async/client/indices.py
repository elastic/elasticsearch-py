# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from .utils import NamespacedClient, query_params, _make_path, SKIP_IN_PATH


class IndicesClient(NamespacedClient):
    @query_params()
    async def analyze(self, body=None, index=None, params=None, headers=None):
        """
        Performs the analysis process on a text and return the tokens breakdown of the
        text.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-analyze.html>`_

        :arg body: Define analyzer/tokenizer parameters and the text on
            which the analysis should be performed
        :arg index: The name of the index to scope the operation
        """
        return await self.transport.perform_request(
            "POST",
            _make_path(index, "_analyze"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable")
    async def refresh(self, index=None, params=None, headers=None):
        """
        Performs the refresh operation in one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-refresh.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        """
        return await self.transport.perform_request(
            "POST", _make_path(index, "_refresh"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "force",
        "ignore_unavailable",
        "wait_if_ongoing",
    )
    async def flush(self, index=None, params=None, headers=None):
        """
        Performs the flush operation on one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-flush.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string for all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg force: Whether a flush should be forced even if it is not
            necessarily needed ie. if no changes will be committed to the index.
            This is useful if transaction log IDs should be incremented even if no
            uncommitted changes are present. (This setting can be considered as
            internal)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg wait_if_ongoing: If set to true the flush operation will
            block until the flush can be executed if another flush operation is
            already executing. The default is true. If set to false the flush will
            be skipped iff if another flush operation is already running.
        """
        return await self.transport.perform_request(
            "POST", _make_path(index, "_flush"), params=params, headers=headers
        )

    @query_params(
        "include_type_name", "master_timeout", "timeout", "wait_for_active_shards"
    )
    async def create(self, index, body=None, params=None, headers=None):
        """
        Creates an index with optional settings and mappings.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-create-index.html>`_

        :arg index: The name of the index
        :arg body: The configuration for the index (`settings` and
            `mappings`)
        :arg include_type_name: Whether a type should be expected in the
            body of the mappings.
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to
            wait for before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "PUT", _make_path(index), params=params, headers=headers, body=body
        )

    @query_params("master_timeout", "timeout", "wait_for_active_shards")
    async def clone(self, index, target, body=None, params=None, headers=None):
        """
        Clones an index
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-clone-index.html>`_

        :arg index: The name of the source index to clone
        :arg target: The name of the target index to clone into
        :arg body: The configuration for the target index (`settings`
            and `aliases`)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to
            wait for on the cloned index before the operation returns.
        """
        for param in (index, target):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path(index, "_clone", target),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "flat_settings",
        "ignore_unavailable",
        "include_defaults",
        "include_type_name",
        "local",
        "master_timeout",
    )
    async def get(self, index, params=None, headers=None):
        """
        Returns information about one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-get-index.html>`_

        :arg index: A comma-separated list of index names
        :arg allow_no_indices: Ignore if a wildcard expression resolves
            to no concrete indices (default: false)
        :arg expand_wildcards: Whether wildcard expressions should get
            expanded to open or closed indices (default: open)  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg ignore_unavailable: Ignore unavailable indexes (default:
            false)
        :arg include_defaults: Whether to return all default setting for
            each of the indices.
        :arg include_type_name: Whether to add the type name to the
            response (default: false)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Specify timeout for connection to master
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "GET", _make_path(index), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "master_timeout",
        "timeout",
        "wait_for_active_shards",
    )
    async def open(self, index, params=None, headers=None):
        """
        Opens an index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-open-close.html>`_

        :arg index: A comma separated list of indices to open
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: closed
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Sets the number of active shards to
            wait for before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "POST", _make_path(index, "_open"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "master_timeout",
        "timeout",
        "wait_for_active_shards",
    )
    async def close(self, index, params=None, headers=None):
        """
        Closes an index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-open-close.html>`_

        :arg index: A comma separated list of indices to close
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Sets the number of active shards to
            wait for before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "POST", _make_path(index, "_close"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "master_timeout",
        "timeout",
    )
    async def delete(self, index, params=None, headers=None):
        """
        Deletes an index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-delete-index.html>`_

        :arg index: A comma-separated list of indices to delete; use
            `_all` or `*` string to delete all indices
        :arg allow_no_indices: Ignore if a wildcard expression resolves
            to no concrete indices (default: false)
        :arg expand_wildcards: Whether wildcard expressions should get
            expanded to open or closed indices (default: open)  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Ignore unavailable indexes (default:
            false)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "DELETE", _make_path(index), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "flat_settings",
        "ignore_unavailable",
        "include_defaults",
        "local",
    )
    async def exists(self, index, params=None, headers=None):
        """
        Returns information about whether a particular index exists.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-exists.html>`_

        :arg index: A comma-separated list of index names
        :arg allow_no_indices: Ignore if a wildcard expression resolves
            to no concrete indices (default: false)
        :arg expand_wildcards: Whether wildcard expressions should get
            expanded to open or closed indices (default: open)  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg ignore_unavailable: Ignore unavailable indexes (default:
            false)
        :arg include_defaults: Whether to return all default setting for
            each of the indices.
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "HEAD", _make_path(index), params=params, headers=headers
        )

    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable", "local")
    async def exists_type(self, index, doc_type, params=None, headers=None):
        """
        Returns information about whether a particular document type exists.
        (DEPRECATED)
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-types-exists.html>`_

        :arg index: A comma-separated list of index names; use `_all` to
            check the types across all indices
        :arg doc_type: A comma-separated list of document types to check
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        """
        for param in (index, doc_type):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "HEAD",
            _make_path(index, "_mapping", doc_type),
            params=params,
            headers=headers,
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "include_type_name",
        "master_timeout",
        "timeout",
    )
    async def put_mapping(
        self, body, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Updates the index mappings.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-put-mapping.html>`_

        :arg body: The mapping definition
        :arg index: A comma-separated list of index names the mapping
            should be added to (supports wildcards); use `_all` or omit to add the
            mapping on all indices.
        :arg doc_type: The name of the document type
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg include_type_name: Whether a type should be expected in the
            body of the mappings.
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        if doc_type not in SKIP_IN_PATH and index in SKIP_IN_PATH:
            index = "_all"

        return await self.transport.perform_request(
            "PUT",
            _make_path(index, doc_type, "_mapping"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "include_type_name",
        "local",
        "master_timeout",
    )
    async def get_mapping(self, index=None, doc_type=None, params=None, headers=None):
        """
        Returns mappings for one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-get-mapping.html>`_

        :arg index: A comma-separated list of index names
        :arg doc_type: A comma-separated list of document types
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg include_type_name: Whether to add the type name to the
            response (default: false)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Specify timeout for connection to master
        """
        return await self.transport.perform_request(
            "GET",
            _make_path(index, "_mapping", doc_type),
            params=params,
            headers=headers,
        )

    @query_params("master_timeout", "timeout")
    async def put_alias(self, index, name, body=None, params=None, headers=None):
        """
        Creates or updates an alias.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-aliases.html>`_

        :arg index: A comma-separated list of index names the alias
            should point to (supports wildcards); use `_all` to perform the
            operation on all indices.
        :arg name: The name of the alias to be created or updated
        :arg body: The settings for the alias, such as `routing` or
            `filter`
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        for param in (index, name):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path(index, "_alias", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable", "local")
    async def exists_alias(self, name, index=None, params=None, headers=None):
        """
        Returns information about whether a particular alias exists.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-aliases.html>`_

        :arg name: A comma-separated list of alias names to return
        :arg index: A comma-separated list of index names to filter
            aliases
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: all
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "HEAD", _make_path(index, "_alias", name), params=params, headers=headers
        )

    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable", "local")
    async def get_alias(self, index=None, name=None, params=None, headers=None):
        """
        Returns an alias.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-aliases.html>`_

        :arg index: A comma-separated list of index names to filter
            aliases
        :arg name: A comma-separated list of alias names to return
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: all
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_alias", name), params=params, headers=headers
        )

    @query_params("master_timeout", "timeout")
    async def update_aliases(self, body, params=None, headers=None):
        """
        Updates index aliases.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-aliases.html>`_

        :arg body: The definition of `actions` to perform
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Request timeout
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "POST", "/_aliases", params=params, headers=headers, body=body
        )

    @query_params("master_timeout", "timeout")
    async def delete_alias(self, index, name, params=None, headers=None):
        """
        Deletes an alias.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-aliases.html>`_

        :arg index: A comma-separated list of index names (supports
            wildcards); use `_all` for all indices
        :arg name: A comma-separated list of aliases to delete (supports
            wildcards); use `_all` to delete all aliases for the specified indices.
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit timestamp for the document
        """
        for param in (index, name):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "DELETE", _make_path(index, "_alias", name), params=params, headers=headers
        )

    @query_params("create", "include_type_name", "master_timeout", "order")
    async def put_template(self, name, body, params=None, headers=None):
        """
        Creates or updates an index template.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The name of the template
        :arg body: The template definition
        :arg create: Whether the index template should only be added if
            new or can also replace an existing one
        :arg include_type_name: Whether a type should be returned in the
            body of the mappings.
        :arg master_timeout: Specify timeout for connection to master
        :arg order: The order for this template when merging multiple
            matching ones (higher numbers are merged later, overriding the lower
            numbers)
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_template", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("flat_settings", "local", "master_timeout")
    async def exists_template(self, name, params=None, headers=None):
        """
        Returns information about whether a particular index template exists.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The comma separated names of the index templates
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "HEAD", _make_path("_template", name), params=params, headers=headers
        )

    @query_params("flat_settings", "include_type_name", "local", "master_timeout")
    async def get_template(self, name=None, params=None, headers=None):
        """
        Returns an index template.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The comma separated names of the index templates
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg include_type_name: Whether a type should be returned in the
            body of the mappings.
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        return await self.transport.perform_request(
            "GET", _make_path("_template", name), params=params, headers=headers
        )

    @query_params("master_timeout", "timeout")
    async def delete_template(self, name, params=None, headers=None):
        """
        Deletes an index template.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The name of the template
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "DELETE", _make_path("_template", name), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "flat_settings",
        "ignore_unavailable",
        "include_defaults",
        "local",
        "master_timeout",
    )
    async def get_settings(self, index=None, name=None, params=None, headers=None):
        """
        Returns settings for one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-get-settings.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg name: The name of the settings that should be included
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: all
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg include_defaults: Whether to return all default setting for
            each of the indices.
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Specify timeout for connection to master
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_settings", name), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "flat_settings",
        "ignore_unavailable",
        "master_timeout",
        "preserve_existing",
        "timeout",
    )
    async def put_settings(self, body, index=None, params=None, headers=None):
        """
        Updates the index settings.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-update-settings.html>`_

        :arg body: The index settings to be updated
        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg master_timeout: Specify timeout for connection to master
        :arg preserve_existing: Whether to update existing settings. If
            set to `true` existing settings on an index remain unchanged, the
            default is `false`
        :arg timeout: Explicit operation timeout
        """
        if body in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'body'.")

        return await self.transport.perform_request(
            "PUT",
            _make_path(index, "_settings"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "completion_fields",
        "expand_wildcards",
        "fielddata_fields",
        "fields",
        "forbid_closed_indices",
        "groups",
        "include_segment_file_sizes",
        "include_unloaded_segments",
        "level",
        "types",
    )
    async def stats(self, index=None, metric=None, params=None, headers=None):
        """
        Provides statistics on operations happening in an index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-stats.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg metric: Limit the information returned the specific
            metrics.  Valid choices: _all, completion, docs, fielddata, query_cache,
            flush, get, indexing, merge, request_cache, refresh, search, segments,
            store, warmer, suggest
        :arg completion_fields: A comma-separated list of fields for
            `fielddata` and `suggest` index metric (supports wildcards)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg fielddata_fields: A comma-separated list of fields for
            `fielddata` index metric (supports wildcards)
        :arg fields: A comma-separated list of fields for `fielddata`
            and `completion` index metric (supports wildcards)
        :arg forbid_closed_indices: If set to false stats will also
            collected from closed indices if explicitly specified or if
            expand_wildcards expands to closed indices  Default: True
        :arg groups: A comma-separated list of search groups for
            `search` index metric
        :arg include_segment_file_sizes: Whether to report the
            aggregated disk usage of each one of the Lucene index files (only
            applies if segment stats are requested)
        :arg include_unloaded_segments: If set to true segment stats
            will include stats for segments that are not currently loaded into
            memory
        :arg level: Return stats aggregated at cluster, index or shard
            level  Valid choices: cluster, indices, shards  Default: indices
        :arg types: A comma-separated list of document types for the
            `indexing` index metric
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_stats", metric), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices", "expand_wildcards", "ignore_unavailable", "verbose"
    )
    async def segments(self, index=None, params=None, headers=None):
        """
        Provides low-level information about segments in a Lucene index.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-segments.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg verbose: Includes detailed memory usage by Lucene.
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_segments"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "fielddata",
        "fields",
        "ignore_unavailable",
        "query",
        "request",
    )
    async def clear_cache(self, index=None, params=None, headers=None):
        """
        Clears all or specific caches for one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-clearcache.html>`_

        :arg index: A comma-separated list of index name to limit the
            operation
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg fielddata: Clear field data
        :arg fields: A comma-separated list of fields to clear when
            using the `fielddata` parameter (default: all)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg query: Clear query caches
        :arg request: Clear request cache
        """
        return await self.transport.perform_request(
            "POST", _make_path(index, "_cache", "clear"), params=params, headers=headers
        )

    @query_params("active_only", "detailed")
    async def recovery(self, index=None, params=None, headers=None):
        """
        Returns information about ongoing index shard recoveries.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-recovery.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg active_only: Display only those recoveries that are
            currently on-going
        :arg detailed: Whether to display detailed information about
            shard recovery
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_recovery"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "only_ancient_segments",
        "wait_for_completion",
    )
    async def upgrade(self, index=None, params=None, headers=None):
        """
        The _upgrade API is no longer useful and will be removed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-upgrade.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg only_ancient_segments: If true, only ancient (an older
            Lucene major release) segments will be upgraded
        :arg wait_for_completion: Specify whether the request should
            block until the all segments are upgraded (default: false)
        """
        return await self.transport.perform_request(
            "POST", _make_path(index, "_upgrade"), params=params, headers=headers
        )

    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable")
    async def get_upgrade(self, index=None, params=None, headers=None):
        """
        The _upgrade API is no longer useful and will be removed.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-upgrade.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_upgrade"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices", "expand_wildcards", "ignore_unavailable", "status"
    )
    async def shard_stores(self, index=None, params=None, headers=None):
        """
        Provides store information for shard copies of indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-shards-stores.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg status: A comma-separated list of statuses used to filter
            on shards to get store information for  Valid choices: green, yellow,
            red, all
        """
        return await self.transport.perform_request(
            "GET", _make_path(index, "_shard_stores"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "flush",
        "ignore_unavailable",
        "max_num_segments",
        "only_expunge_deletes",
    )
    async def forcemerge(self, index=None, params=None, headers=None):
        """
        Performs the force merge operation on one or more indices.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-forcemerge.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string to perform the operation on all indices
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg flush: Specify whether the index should be flushed after
            performing the operation (default: true)
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg max_num_segments: The number of segments the index should
            be merged into (default: dynamic)
        :arg only_expunge_deletes: Specify whether the operation should
            only expunge deleted documents
        """
        return await self.transport.perform_request(
            "POST", _make_path(index, "_forcemerge"), params=params, headers=headers
        )

    @query_params(
        "copy_settings", "master_timeout", "timeout", "wait_for_active_shards"
    )
    async def shrink(self, index, target, body=None, params=None, headers=None):
        """
        Allow to shrink an existing index into a new index with fewer primary shards.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-shrink-index.html>`_

        :arg index: The name of the source index to shrink
        :arg target: The name of the target index to shrink into
        :arg body: The configuration for the target index (`settings`
            and `aliases`)
        :arg copy_settings: whether or not to copy settings from the
            source index (defaults to false)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to
            wait for on the shrunken index before the operation returns.
        """
        for param in (index, target):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path(index, "_shrink", target),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "copy_settings", "master_timeout", "timeout", "wait_for_active_shards"
    )
    async def split(self, index, target, body=None, params=None, headers=None):
        """
        Allows you to split an existing index into a new index with more primary
        shards.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-split-index.html>`_

        :arg index: The name of the source index to split
        :arg target: The name of the target index to split into
        :arg body: The configuration for the target index (`settings`
            and `aliases`)
        :arg copy_settings: whether or not to copy settings from the
            source index (defaults to false)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to
            wait for on the shrunken index before the operation returns.
        """
        for param in (index, target):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path(index, "_split", target),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "dry_run",
        "include_type_name",
        "master_timeout",
        "timeout",
        "wait_for_active_shards",
    )
    async def rollover(
        self, alias, body=None, new_index=None, params=None, headers=None
    ):
        """
        Updates an alias to point to a new index when the existing index is considered
        to be too large or too old.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-rollover-index.html>`_

        :arg alias: The name of the alias to rollover
        :arg body: The conditions that needs to be met for executing
            rollover
        :arg new_index: The name of the rollover index
        :arg dry_run: If set to true the rollover action will only be
            validated but not actually performed even if a condition matches. The
            default is false
        :arg include_type_name: Whether a type should be included in the
            body of the mappings.
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Set the number of active shards to
            wait for on the newly created rollover index before the operation
            returns.
        """
        if alias in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'alias'.")

        return await self.transport.perform_request(
            "POST",
            _make_path(alias, "_rollover", new_index),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "master_timeout",
        "timeout",
        "wait_for_active_shards",
    )
    async def freeze(self, index, params=None, headers=None):
        """
        Freezes an index. A frozen index has almost no overhead on the cluster (except
        for maintaining its metadata in memory) and is read-only.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/freeze-index-api.html>`_

        :arg index: The name of the index to freeze
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: closed
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Sets the number of active shards to
            wait for before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "POST", _make_path(index, "_freeze"), params=params, headers=headers
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "master_timeout",
        "timeout",
        "wait_for_active_shards",
    )
    async def unfreeze(self, index, params=None, headers=None):
        """
        Unfreezes an index. When a frozen index is unfrozen, the index goes through the
        normal recovery process and becomes writeable again.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/unfreeze-index-api.html>`_

        :arg index: The name of the index to unfreeze
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: closed
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        :arg wait_for_active_shards: Sets the number of active shards to
            wait for before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "POST", _make_path(index, "_unfreeze"), params=params, headers=headers
        )

    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable")
    async def reload_search_analyzers(self, index, params=None, headers=None):
        """
        Reloads an index's search analyzers and their resources.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-reload-analyzers.html>`_

        :arg index: A comma-separated list of index names to reload
            analyzers for
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'index'.")

        return await self.transport.perform_request(
            "GET",
            _make_path(index, "_reload_search_analyzers"),
            params=params,
            headers=headers,
        )

    @query_params(
        "allow_no_indices",
        "expand_wildcards",
        "ignore_unavailable",
        "include_defaults",
        "include_type_name",
        "local",
    )
    async def get_field_mapping(
        self, fields, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Returns mapping for one or more fields.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-get-field-mapping.html>`_

        :arg fields: A comma-separated list of fields
        :arg index: A comma-separated list of index names
        :arg doc_type: A comma-separated list of document types
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg include_defaults: Whether the default mapping values should
            be returned as well
        :arg include_type_name: Whether a type should be returned in the
            body of the mappings.
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        """
        if fields in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'fields'.")

        return await self.transport.perform_request(
            "GET",
            _make_path(index, "_mapping", doc_type, "field", fields),
            params=params,
            headers=headers,
        )

    @query_params(
        "all_shards",
        "allow_no_indices",
        "analyze_wildcard",
        "analyzer",
        "default_operator",
        "df",
        "expand_wildcards",
        "explain",
        "ignore_unavailable",
        "lenient",
        "q",
        "rewrite",
    )
    async def validate_query(
        self, body=None, index=None, doc_type=None, params=None, headers=None
    ):
        """
        Allows a user to validate a potentially expensive query without executing it.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/search-validate.html>`_

        :arg body: The query definition specified with the Query DSL
        :arg index: A comma-separated list of index names to restrict
            the operation; use `_all` or empty string to perform the operation on
            all indices
        :arg doc_type: A comma-separated list of document types to
            restrict the operation; leave empty to perform the operation on all
            types
        :arg all_shards: Execute validation on all shards instead of one
            random shard per index
        :arg allow_no_indices: Whether to ignore if a wildcard indices
            expression resolves into no concrete indices. (This includes `_all`
            string or when no indices have been specified)
        :arg analyze_wildcard: Specify whether wildcard and prefix
            queries should be analyzed (default: false)
        :arg analyzer: The analyzer to use for the query string
        :arg default_operator: The default operator for query string
            query (AND or OR)  Valid choices: AND, OR  Default: OR
        :arg df: The field to use as default where no field prefix is
            given in the query string
        :arg expand_wildcards: Whether to expand wildcard expression to
            concrete indices that are open, closed or both.  Valid choices: open,
            closed, hidden, none, all  Default: open
        :arg explain: Return detailed information about the error
        :arg ignore_unavailable: Whether specified concrete indices
            should be ignored when unavailable (missing or closed)
        :arg lenient: Specify whether format-based query failures (such
            as providing text to a numeric field) should be ignored
        :arg q: Query in the Lucene query string syntax
        :arg rewrite: Provide a more detailed explanation showing the
            actual Lucene query that will be executed.
        """
        return await self.transport.perform_request(
            "POST",
            _make_path(index, doc_type, "_validate", "query"),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def create_data_stream(self, name, body, params=None, headers=None):
        """
        Creates or updates a data stream
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/data-streams.html>`_

        :arg name: The name of the data stream
        :arg body: The data stream definition
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_data_stream", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params()
    async def delete_data_stream(self, name, params=None, headers=None):
        """
        Deletes a data stream.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/data-streams.html>`_

        :arg name: The name of the data stream
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "DELETE", _make_path("_data_stream", name), params=params, headers=headers
        )

    @query_params()
    async def get_data_streams(self, name=None, params=None, headers=None):
        """
        Returns data streams.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/data-streams.html>`_

        :arg name: The name or wildcard expression of the requested data
            streams
        """
        return await self.transport.perform_request(
            "GET", _make_path("_data_streams", name), params=params, headers=headers
        )

    @query_params("master_timeout", "timeout")
    async def delete_index_template(self, name, params=None, headers=None):
        """
        Deletes an index template.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The name of the template
        :arg master_timeout: Specify timeout for connection to master
        :arg timeout: Explicit operation timeout
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "DELETE",
            _make_path("_index_template", name),
            params=params,
            headers=headers,
        )

    @query_params("flat_settings", "local", "master_timeout")
    async def get_index_template(self, name=None, params=None, headers=None):
        """
        Returns an index template.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The comma separated names of the index templates
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        return await self.transport.perform_request(
            "GET", _make_path("_index_template", name), params=params, headers=headers
        )

    @query_params("cause", "create", "master_timeout")
    async def put_index_template(self, name, body, params=None, headers=None):
        """
        Creates or updates an index template.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The name of the template
        :arg body: The template definition
        :arg cause: User defined reason for creating/updating the index
            template
        :arg create: Whether the index template should only be added if
            new or can also replace an existing one
        :arg master_timeout: Specify timeout for connection to master
        """
        for param in (name, body):
            if param in SKIP_IN_PATH:
                raise ValueError("Empty value passed for a required argument.")

        return await self.transport.perform_request(
            "PUT",
            _make_path("_index_template", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("flat_settings", "local", "master_timeout")
    async def exists_index_template(self, name, params=None, headers=None):
        """
        Returns information about whether a particular index template exists.
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The name of the template
        :arg flat_settings: Return settings in flat format (default:
            false)
        :arg local: Return local information, do not retrieve the state
            from master node (default: false)
        :arg master_timeout: Explicit operation timeout for connection
            to master node
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "HEAD", _make_path("_index_template", name), params=params, headers=headers
        )

    @query_params("cause", "create", "master_timeout")
    async def simulate_index_template(self, name, body=None, params=None, headers=None):
        """
        Simulate matching the given index name against the index templates in the
        system
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-templates.html>`_

        :arg name: The name of the index (it must be a concrete index
            name)
        :arg body: New index template definition, which will be included
            in the simulation, as if it already exists in the system
        :arg cause: User defined reason for dry-run creating the new
            template for simulation purposes
        :arg create: Whether the index template we optionally defined in
            the body should only be dry-run added if new or can also replace an
            existing one
        :arg master_timeout: Specify timeout for connection to master
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for a required argument 'name'.")

        return await self.transport.perform_request(
            "POST",
            _make_path("_index_template", "_simulate_index", name),
            params=params,
            headers=headers,
            body=body,
        )

    @query_params("allow_no_indices", "expand_wildcards", "ignore_unavailable")
    async def flush_synced(self, index=None, params=None, headers=None):
        """
        Performs a synced flush operation on one or more indices. Synced flush is
        deprecated and will be removed in 8.0. Use flush instead
        `<https://www.elastic.co/guide/en/elasticsearch/reference/7.8/indices-synced-flush-api.html>`_

        :arg index: A comma-separated list of index names; use `_all` or
            empty string for all indices
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
            _make_path(index, "_flush", "synced"),
            params=params,
            headers=headers,
        )

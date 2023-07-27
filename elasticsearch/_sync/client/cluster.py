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

import typing as t

from elastic_transport import HeadApiResponse, ObjectApiResponse

from ._base import NamespacedClient
from .utils import SKIP_IN_PATH, _quote, _rewrite_parameters


class ClusterClient(NamespacedClient):
    @_rewrite_parameters(
        body_fields=True,
    )
    def allocation_explain(
        self,
        *,
        current_node: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        include_disk_info: t.Optional[bool] = None,
        include_yes_decisions: t.Optional[bool] = None,
        index: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        primary: t.Optional[bool] = None,
        shard: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Provides explanations for shard allocations in the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-allocation-explain.html>`_

        :param current_node: Specifies the node ID or the name of the node to only explain
            a shard that is currently located on the specified node.
        :param include_disk_info: If true, returns information about disk usage and shard
            sizes.
        :param include_yes_decisions: If true, returns YES decisions in explanation.
        :param index: Specifies the name of the index that you would like an explanation
            for.
        :param primary: If true, returns explanation for the primary shard for the given
            shard ID.
        :param shard: Specifies the ID of the shard that you would like an explanation
            for.
        """
        __path = "/_cluster/allocation/explain"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if current_node is not None:
            __body["current_node"] = current_node
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if include_disk_info is not None:
            __query["include_disk_info"] = include_disk_info
        if include_yes_decisions is not None:
            __query["include_yes_decisions"] = include_yes_decisions
        if index is not None:
            __body["index"] = index
        if pretty is not None:
            __query["pretty"] = pretty
        if primary is not None:
            __body["primary"] = primary
        if shard is not None:
            __body["shard"] = shard
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def delete_component_template(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a component template

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-component-template.html>`_

        :param name: Comma-separated list or wildcard expression of component template
            names used to limit the request.
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_component_template/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_voting_config_exclusions(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        wait_for_removal: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Clears cluster voting config exclusions.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/voting-config-exclusions.html>`_

        :param wait_for_removal: Specifies whether to wait for all excluded nodes to
            be removed from the cluster before clearing the voting configuration exclusions
            list. Defaults to true, meaning that all excluded nodes must be removed from
            the cluster before this API takes any action. If set to false then the voting
            configuration exclusions list is cleared even if some excluded nodes are
            still in the cluster.
        """
        __path = "/_cluster/voting_config_exclusions"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_for_removal is not None:
            __query["wait_for_removal"] = wait_for_removal
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def exists_component_template(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> HeadApiResponse:
        """
        Returns information about whether a particular component template exist

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-component-template.html>`_

        :param name: Comma-separated list of component template names used to limit the
            request. Wildcard (*) expressions are supported.
        :param local: If true, the request retrieves information from the local node
            only. Defaults to false, which means information is retrieved from the master
            node.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_component_template/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if local is not None:
            __query["local"] = local
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "HEAD", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_component_template(
        self,
        *,
        name: t.Optional[str] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        include_defaults: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns one or more component templates

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-component-template.html>`_

        :param name: The comma separated names of the component templates
        :param flat_settings:
        :param include_defaults: Return all default configurations for the component
            template (default: false)
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Explicit operation timeout for connection to master node
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_component_template/{_quote(name)}"
        else:
            __path = "/_component_template"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if local is not None:
            __query["local"] = local
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_settings(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        include_defaults: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns cluster settings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-get-settings.html>`_

        :param flat_settings: Return settings in flat format (default: false)
        :param include_defaults: Whether to return all default clusters setting.
        :param master_timeout: Explicit operation timeout for connection to master node
        :param timeout: Explicit operation timeout
        """
        __path = "/_cluster/settings"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def health(
        self,
        *,
        index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        expand_wildcards: t.Optional[
            t.Union[
                t.Union["t.Literal['all', 'closed', 'hidden', 'none', 'open']", str],
                t.Union[
                    t.List[
                        t.Union[
                            "t.Literal['all', 'closed', 'hidden', 'none', 'open']", str
                        ]
                    ],
                    t.Tuple[
                        t.Union[
                            "t.Literal['all', 'closed', 'hidden', 'none', 'open']", str
                        ],
                        ...,
                    ],
                ],
            ]
        ] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        level: t.Optional[
            t.Union["t.Literal['cluster', 'indices', 'shards']", str]
        ] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
        wait_for_events: t.Optional[
            t.Union[
                "t.Literal['high', 'immediate', 'languid', 'low', 'normal', 'urgent']",
                str,
            ]
        ] = None,
        wait_for_no_initializing_shards: t.Optional[bool] = None,
        wait_for_no_relocating_shards: t.Optional[bool] = None,
        wait_for_nodes: t.Optional[t.Union[int, str]] = None,
        wait_for_status: t.Optional[
            t.Union["t.Literal['green', 'red', 'yellow']", str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns basic information about the health of the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-health.html>`_

        :param index: Comma-separated list of data streams, indices, and index aliases
            used to limit the request. Wildcard expressions (*) are supported. To target
            all data streams and indices in a cluster, omit this parameter or use _all
            or *.
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param level: Can be one of cluster, indices or shards. Controls the details
            level of the health information returned.
        :param local: If true, the request retrieves information from the local node
            only. Defaults to false, which means information is retrieved from the master
            node.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        :param wait_for_active_shards: A number controlling to how many active shards
            to wait for, all to wait for all shards in the cluster to be active, or 0
            to not wait.
        :param wait_for_events: Can be one of immediate, urgent, high, normal, low, languid.
            Wait until all currently queued events with the given priority are processed.
        :param wait_for_no_initializing_shards: A boolean value which controls whether
            to wait (until the timeout provided) for the cluster to have no shard initializations.
            Defaults to false, which means it will not wait for initializing shards.
        :param wait_for_no_relocating_shards: A boolean value which controls whether
            to wait (until the timeout provided) for the cluster to have no shard relocations.
            Defaults to false, which means it will not wait for relocating shards.
        :param wait_for_nodes: The request waits until the specified number N of nodes
            is available. It also accepts >=N, <=N, >N and <N. Alternatively, it is possible
            to use ge(N), le(N), gt(N) and lt(N) notation.
        :param wait_for_status: One of green, yellow or red. Will wait (until the timeout
            provided) until the status of the cluster changes to the one provided or
            better, i.e. green > yellow > red. By default, will not wait for any status.
        """
        if index not in SKIP_IN_PATH:
            __path = f"/_cluster/health/{_quote(index)}"
        else:
            __path = "/_cluster/health"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if level is not None:
            __query["level"] = level
        if local is not None:
            __query["local"] = local
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        if wait_for_events is not None:
            __query["wait_for_events"] = wait_for_events
        if wait_for_no_initializing_shards is not None:
            __query["wait_for_no_initializing_shards"] = wait_for_no_initializing_shards
        if wait_for_no_relocating_shards is not None:
            __query["wait_for_no_relocating_shards"] = wait_for_no_relocating_shards
        if wait_for_nodes is not None:
            __query["wait_for_nodes"] = wait_for_nodes
        if wait_for_status is not None:
            __query["wait_for_status"] = wait_for_status
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def info(
        self,
        *,
        target: t.Union[
            t.Union[
                "t.Literal['_all', 'http', 'ingest', 'script', 'thread_pool']", str
            ],
            t.Union[
                t.List[
                    t.Union[
                        "t.Literal['_all', 'http', 'ingest', 'script', 'thread_pool']",
                        str,
                    ]
                ],
                t.Tuple[
                    t.Union[
                        "t.Literal['_all', 'http', 'ingest', 'script', 'thread_pool']",
                        str,
                    ],
                    ...,
                ],
            ],
        ],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns different information about the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-info.html>`_

        :param target: Limits the information returned to the specific target. Supports
            a comma-separated list, such as http,ingest.
        """
        if target in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'target'")
        __path = f"/_info/{_quote(target)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def pending_tasks(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns a list of any cluster-level changes (e.g. create index, update mapping,
        allocate or fail shard) which have not yet been executed.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-pending.html>`_

        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Specify timeout for connection to master
        """
        __path = "/_cluster/pending_tasks"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if local is not None:
            __query["local"] = local
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def post_voting_config_exclusions(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        node_ids: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        node_names: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the cluster voting config exclusions by node ids or node names.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/voting-config-exclusions.html>`_

        :param node_ids: A comma-separated list of the persistent ids of the nodes to
            exclude from the voting configuration. If specified, you may not also specify
            node_names.
        :param node_names: A comma-separated list of the names of the nodes to exclude
            from the voting configuration. If specified, you may not also specify node_ids.
        :param timeout: When adding a voting configuration exclusion, the API waits for
            the specified nodes to be excluded from the voting configuration before returning.
            If the timeout expires before the appropriate condition is satisfied, the
            request fails and returns an error.
        """
        __path = "/_cluster/voting_config_exclusions"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if node_ids is not None:
            __query["node_ids"] = node_ids
        if node_names is not None:
            __query["node_names"] = node_names
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"_meta": "meta"},
    )
    def put_component_template(
        self,
        *,
        name: str,
        template: t.Mapping[str, t.Any],
        allow_auto_create: t.Optional[bool] = None,
        create: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        meta: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        version: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates or updates a component template

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-component-template.html>`_

        :param name: The name of the template
        :param template: The template to be applied which includes mappings, settings,
            or aliases configuration.
        :param allow_auto_create: This setting overrides the value of the `action.auto_create_index`
            cluster setting. If set to `true` in a template, then indices can be automatically
            created using that template even if auto-creation of indices is disabled
            via `actions.auto_create_index`. If set to `false` then data streams matching
            the template must always be explicitly created.
        :param create: Whether the index template should only be added if new or can
            also replace an existing one
        :param master_timeout: Specify timeout for connection to master
        :param meta: Optional user metadata about the component template. May have any
            contents. This map is not automatically generated by Elasticsearch.
        :param version: Version number used to manage component templates externally.
            This number isn't automatically generated or incremented by Elasticsearch.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        if template is None:
            raise ValueError("Empty value passed for parameter 'template'")
        __path = f"/_component_template/{_quote(name)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if template is not None:
            __body["template"] = template
        if allow_auto_create is not None:
            __body["allow_auto_create"] = allow_auto_create
        if create is not None:
            __query["create"] = create
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if meta is not None:
            __body["_meta"] = meta
        if pretty is not None:
            __query["pretty"] = pretty
        if version is not None:
            __body["version"] = version
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_settings(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        persistent: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        transient: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the cluster settings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-update-settings.html>`_

        :param flat_settings: Return settings in flat format (default: false)
        :param master_timeout: Explicit operation timeout for connection to master node
        :param persistent:
        :param timeout: Explicit operation timeout
        :param transient:
        """
        __path = "/_cluster/settings"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if persistent is not None:
            __body["persistent"] = persistent
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if transient is not None:
            __body["transient"] = transient
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def remote_info(
        self,
        *,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns the information about configured remote clusters.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-remote-info.html>`_
        """
        __path = "/_remote/info"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def reroute(
        self,
        *,
        commands: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
        dry_run: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        explain: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        metric: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        pretty: t.Optional[bool] = None,
        retry_failed: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Allows to manually change the allocation of individual shards in the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-reroute.html>`_

        :param commands: Defines the commands to perform.
        :param dry_run: If true, then the request simulates the operation only and returns
            the resulting state.
        :param explain: If true, then the response contains an explanation of why the
            commands can or cannot be executed.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param metric: Limits the information returned to the specified metrics.
        :param retry_failed: If true, then retries allocation of shards that are blocked
            due to too many subsequent allocation failures.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        __path = "/_cluster/reroute"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if commands is not None:
            __body["commands"] = commands
        if dry_run is not None:
            __query["dry_run"] = dry_run
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if explain is not None:
            __query["explain"] = explain
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if metric is not None:
            __query["metric"] = metric
        if pretty is not None:
            __query["pretty"] = pretty
        if retry_failed is not None:
            __query["retry_failed"] = retry_failed
        if timeout is not None:
            __query["timeout"] = timeout
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def state(
        self,
        *,
        metric: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        allow_no_indices: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        expand_wildcards: t.Optional[
            t.Union[
                t.Union["t.Literal['all', 'closed', 'hidden', 'none', 'open']", str],
                t.Union[
                    t.List[
                        t.Union[
                            "t.Literal['all', 'closed', 'hidden', 'none', 'open']", str
                        ]
                    ],
                    t.Tuple[
                        t.Union[
                            "t.Literal['all', 'closed', 'hidden', 'none', 'open']", str
                        ],
                        ...,
                    ],
                ],
            ]
        ] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        wait_for_metadata_version: t.Optional[int] = None,
        wait_for_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns a comprehensive information about the state of the cluster.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-state.html>`_

        :param metric: Limit the information returned to the specified metrics
        :param index: A comma-separated list of index names; use `_all` or empty string
            to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param flat_settings: Return settings in flat format (default: false)
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Specify timeout for connection to master
        :param wait_for_metadata_version: Wait for the metadata version to be equal or
            greater than the specified metadata version
        :param wait_for_timeout: The maximum time to wait for wait_for_metadata_version
            before timing out
        """
        if metric not in SKIP_IN_PATH and index not in SKIP_IN_PATH:
            __path = f"/_cluster/state/{_quote(metric)}/{_quote(index)}"
        elif metric not in SKIP_IN_PATH:
            __path = f"/_cluster/state/{_quote(metric)}"
        elif index not in SKIP_IN_PATH:
            __path = f"/_cluster/state/_all/{_quote(index)}"
        else:
            __path = "/_cluster/state"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if local is not None:
            __query["local"] = local
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_for_metadata_version is not None:
            __query["wait_for_metadata_version"] = wait_for_metadata_version
        if wait_for_timeout is not None:
            __query["wait_for_timeout"] = wait_for_timeout
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def stats(
        self,
        *,
        node_id: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns high-level overview of cluster statistics.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/cluster-stats.html>`_

        :param node_id: Comma-separated list of node filters used to limit returned information.
            Defaults to all nodes in the cluster.
        :param flat_settings: Return settings in flat format (default: false)
        :param timeout: Period to wait for each node to respond. If a node does not respond
            before its timeout expires, the response does not include its stats. However,
            timed out nodes are included in the response’s _nodes.failed property. Defaults
            to no timeout.
        """
        if node_id not in SKIP_IN_PATH:
            __path = f"/_cluster/stats/nodes/{_quote(node_id)}"
        else:
            __path = "/_cluster/stats"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

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


class IndicesClient(NamespacedClient):
    @_rewrite_parameters()
    def add_block(
        self,
        *,
        index: str,
        block: t.Union["t.Literal['metadata', 'read', 'read_only', 'write']", str],
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Adds a block to an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/index-modules-blocks.html>`_

        :param index: A comma separated list of indices to add a block to
        :param block: The block to add (one of read, write, read_only or metadata)
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if block in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'block'")
        __path = f"/{_quote(index)}/_block/{_quote(block)}"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def analyze(
        self,
        *,
        index: t.Optional[str] = None,
        analyzer: t.Optional[str] = None,
        attributes: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        char_filter: t.Optional[
            t.Union[
                t.List[t.Union[str, t.Mapping[str, t.Any]]],
                t.Tuple[t.Union[str, t.Mapping[str, t.Any]], ...],
            ]
        ] = None,
        error_trace: t.Optional[bool] = None,
        explain: t.Optional[bool] = None,
        field: t.Optional[str] = None,
        filter: t.Optional[
            t.Union[
                t.List[t.Union[str, t.Mapping[str, t.Any]]],
                t.Tuple[t.Union[str, t.Mapping[str, t.Any]], ...],
            ]
        ] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        normalizer: t.Optional[str] = None,
        pretty: t.Optional[bool] = None,
        text: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        tokenizer: t.Optional[t.Union[str, t.Mapping[str, t.Any]]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Performs the analysis process on a text and return the tokens breakdown of the
        text.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-analyze.html>`_

        :param index: The name of the index to scope the operation
        :param analyzer:
        :param attributes:
        :param char_filter:
        :param explain:
        :param field:
        :param filter:
        :param normalizer:
        :param text:
        :param tokenizer:
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_analyze"
        else:
            __path = "/_analyze"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if analyzer is not None:
            __body["analyzer"] = analyzer
        if attributes is not None:
            __body["attributes"] = attributes
        if char_filter is not None:
            __body["char_filter"] = char_filter
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if explain is not None:
            __body["explain"] = explain
        if field is not None:
            __body["field"] = field
        if filter is not None:
            __body["filter"] = filter
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if normalizer is not None:
            __body["normalizer"] = normalizer
        if pretty is not None:
            __query["pretty"] = pretty
        if text is not None:
            __body["text"] = text
        if tokenizer is not None:
            __body["tokenizer"] = tokenizer
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def clear_cache(
        self,
        *,
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
        fielddata: t.Optional[bool] = None,
        fields: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        query: t.Optional[bool] = None,
        request: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Clears all or specific caches for one or more indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-clearcache.html>`_

        :param index: A comma-separated list of index name to limit the operation
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param fielddata: Clear field data
        :param fields: A comma-separated list of fields to clear when using the `fielddata`
            parameter (default: all)
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param query: Clear query caches
        :param request: Clear request cache
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_cache/clear"
        else:
            __path = "/_cache/clear"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if fielddata is not None:
            __query["fielddata"] = fielddata
        if fields is not None:
            __query["fields"] = fields
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        if query is not None:
            __query["query"] = query
        if request is not None:
            __query["request"] = request
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def clone(
        self,
        *,
        index: str,
        target: str,
        aliases: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        settings: t.Optional[t.Mapping[str, t.Any]] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Clones an index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-clone-index.html>`_

        :param index: The name of the source index to clone
        :param target: The name of the target index to clone into
        :param aliases:
        :param master_timeout: Specify timeout for connection to master
        :param settings:
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Set the number of active shards to wait for on
            the cloned index before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if target in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'target'")
        __path = f"/{_quote(index)}/_clone/{_quote(target)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if aliases is not None:
            __body["aliases"] = aliases
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
        if settings is not None:
            __body["settings"] = settings
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def close(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Closes an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-open-close.html>`_

        :param index: A comma separated list of indices to close
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Sets the number of active shards to wait for before
            the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_close"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def create(
        self,
        *,
        index: str,
        aliases: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        mappings: t.Optional[t.Mapping[str, t.Any]] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        settings: t.Optional[t.Mapping[str, t.Any]] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates an index with optional settings and mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-create-index.html>`_

        :param index: The name of the index
        :param aliases:
        :param mappings: Mapping for fields in the index. If specified, this mapping
            can include: - Field names - Field data types - Mapping parameters
        :param master_timeout: Specify timeout for connection to master
        :param settings:
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Set the number of active shards to wait for before
            the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if aliases is not None:
            __body["aliases"] = aliases
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if mappings is not None:
            __body["mappings"] = mappings
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if settings is not None:
            __body["settings"] = settings
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def create_data_stream(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates a data stream

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/data-streams.html>`_

        :param name: The name of the data stream
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_data_stream/{_quote(name)}"
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
            "PUT", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def data_streams_stats(
        self,
        *,
        name: t.Optional[str] = None,
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
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Provides statistics on operations happening in a data stream.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/data-streams.html>`_

        :param name: A comma-separated list of data stream names; use `_all` or empty
            string to perform the operation on all data streams
        :param expand_wildcards:
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_data_stream/{_quote(name)}/_stats"
        else:
            __path = "/_data_stream/_stats"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
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
    def delete(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-delete-index.html>`_

        :param index: A comma-separated list of indices to delete; use `_all` or `*`
            string to delete all indices
        :param allow_no_indices: Ignore if a wildcard expression resolves to no concrete
            indices (default: false)
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open, closed, or hidden indices
        :param ignore_unavailable: Ignore unavailable indexes (default: false)
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
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
    def delete_alias(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        Deletes an alias.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-aliases.html>`_

        :param index: A comma-separated list of index names (supports wildcards); use
            `_all` for all indices
        :param name: A comma-separated list of aliases to delete (supports wildcards);
            use `_all` to delete all aliases for the specified indices.
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit timestamp for the document
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/{_quote(index)}/_alias/{_quote(name)}"
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
    def delete_data_lifecycle(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes the data lifecycle of the selected data streams.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/dlm-delete-lifecycle.html>`_

        :param name: A comma-separated list of data streams of which the data lifecycle
            will be deleted; use `*` to get all data streams
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open or closed indices (default: open)
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit timestamp for the document
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_data_stream/{_quote(name)}/_lifecycle"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
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
    def delete_data_stream(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Deletes a data stream.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/data-streams.html>`_

        :param name: A comma-separated list of data streams to delete; use `*` to delete
            all data streams
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open or closed indices (default: open)
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_data_stream/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "DELETE", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def delete_index_template(
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
        Deletes an index template.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: Comma-separated list of index template names used to limit the request.
            Wildcard (*) expressions are supported.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_index_template/{_quote(name)}"
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
    def delete_template(
        self,
        *,
        name: str,
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
        Deletes an index template.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: The name of the template
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_template/{_quote(name)}"
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
    def disk_usage(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        flush: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        run_expensive_tasks: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Analyzes the disk usage of each field of an index or data stream

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-disk-usage.html>`_

        :param index: Comma-separated list of data streams, indices, and aliases used
            to limit the request. It’s recommended to execute this API with a single
            index (or the latest backing index of a data stream) as the API consumes
            resources significantly.
        :param allow_no_indices: If false, the request returns an error if any wildcard
            expression, index alias, or _all value targets only missing or closed indices.
            This behavior applies even if the request targets other open indices. For
            example, a request targeting foo*,bar* returns an error if an index starts
            with foo but no index starts with bar.
        :param expand_wildcards: Type of index that wildcard patterns can match. If the
            request can target data streams, this argument determines whether wildcard
            expressions match hidden data streams. Supports comma-separated values, such
            as open,hidden.
        :param flush: If true, the API performs a flush before analysis. If false, the
            response may not include uncommitted data.
        :param ignore_unavailable: If true, missing or closed indices are not included
            in the response.
        :param run_expensive_tasks: Analyzing field disk usage is resource-intensive.
            To use the API, this parameter must be set to true.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_disk_usage"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flush is not None:
            __query["flush"] = flush
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        if run_expensive_tasks is not None:
            __query["run_expensive_tasks"] = run_expensive_tasks
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_name="config",
    )
    def downsample(
        self,
        *,
        index: str,
        target_index: str,
        config: t.Mapping[str, t.Any],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Downsample an index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/xpack-rollup.html>`_

        :param index: The index to downsample
        :param target_index: The name of the target index to store downsampled data
        :param config:
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if target_index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'target_index'")
        if config is None:
            raise ValueError("Empty value passed for parameter 'config'")
        __path = f"/{_quote(index)}/_downsample/{_quote(target_index)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __body = config
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def exists(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        include_defaults: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> HeadApiResponse:
        """
        Returns information about whether a particular index exists.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-exists.html>`_

        :param index: A comma-separated list of index names
        :param allow_no_indices: Ignore if a wildcard expression resolves to no concrete
            indices (default: false)
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open or closed indices (default: open)
        :param flat_settings: Return settings in flat format (default: false)
        :param ignore_unavailable: Ignore unavailable indexes (default: false)
        :param include_defaults: Whether to return all default setting for each of the
            indices.
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}"
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
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if local is not None:
            __query["local"] = local
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "HEAD", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def exists_alias(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> HeadApiResponse:
        """
        Returns information about whether a particular alias exists.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-aliases.html>`_

        :param name: A comma-separated list of alias names to return
        :param index: A comma-separated list of index names to filter aliases
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        if index not in SKIP_IN_PATH and name not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_alias/{_quote(name)}"
        elif name not in SKIP_IN_PATH:
            __path = f"/_alias/{_quote(name)}"
        else:
            raise ValueError("Couldn't find a path for the given parameters")
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if local is not None:
            __query["local"] = local
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "HEAD", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def exists_index_template(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> HeadApiResponse:
        """
        Returns information about whether a particular index template exists.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: Comma-separated list of index template names used to limit the request.
            Wildcard (*) expressions are supported.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_index_template/{_quote(name)}"
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
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "HEAD", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def exists_template(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> HeadApiResponse:
        """
        Returns information about whether a particular index template exists.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: The comma separated names of the index templates
        :param flat_settings: Return settings in flat format (default: false)
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Explicit operation timeout for connection to master node
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_template/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
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
    def explain_data_lifecycle(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        include_defaults: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Retrieves information about the index's current DLM lifecycle, such as any potential
        encountered error, time since creation etc.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/dlm-explain-lifecycle.html>`_

        :param index: The name of the index to explain
        :param include_defaults: indicates if the API should return the default values
            the system uses for the index's lifecycle
        :param master_timeout: Specify timeout for connection to master
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_lifecycle/explain"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def field_usage_stats(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        fields: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns the field usage stats for each field of an index

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/field-usage-stats.html>`_

        :param index: Comma-separated list or wildcard expression of index names used
            to limit the request.
        :param allow_no_indices: If false, the request returns an error if any wildcard
            expression, index alias, or _all value targets only missing or closed indices.
            This behavior applies even if the request targets other open indices. For
            example, a request targeting `foo*,bar*` returns an error if an index starts
            with `foo` but no index starts with `bar`.
        :param expand_wildcards: Type of index that wildcard patterns can match. If the
            request can target data streams, this argument determines whether wildcard
            expressions match hidden data streams. Supports comma-separated values, such
            as `open,hidden`.
        :param fields: Comma-separated list or wildcard expressions of fields to include
            in the statistics.
        :param ignore_unavailable: If true, missing or closed indices are not included
            in the response.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param timeout: Period to wait for a response. If no response is received before
            the timeout expires, the request fails and returns an error.
        :param wait_for_active_shards: The number of shard copies that must be active
            before proceeding with the operation. Set to all or any positive integer
            up to the total number of shards in the index (`number_of_replicas+1`).
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_field_usage_stats"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if fields is not None:
            __query["fields"] = fields
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def flush(
        self,
        *,
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
        force: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        wait_if_ongoing: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Performs the flush operation on one or more indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-flush.html>`_

        :param index: A comma-separated list of index names; use `_all` or empty string
            for all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param force: Whether a flush should be forced even if it is not necessarily
            needed ie. if no changes will be committed to the index. This is useful if
            transaction log IDs should be incremented even if no uncommitted changes
            are present. (This setting can be considered as internal)
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param wait_if_ongoing: If set to true the flush operation will block until the
            flush can be executed if another flush operation is already executing. The
            default is true. If set to false the flush will be skipped iff if another
            flush operation is already running.
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_flush"
        else:
            __path = "/_flush"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if force is not None:
            __query["force"] = force
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_if_ongoing is not None:
            __query["wait_if_ongoing"] = wait_if_ongoing
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def forcemerge(
        self,
        *,
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
        flush: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        max_num_segments: t.Optional[int] = None,
        only_expunge_deletes: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        wait_for_completion: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Performs the force merge operation on one or more indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-forcemerge.html>`_

        :param index: A comma-separated list of index names; use `_all` or empty string
            to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param flush: Specify whether the index should be flushed after performing the
            operation (default: true)
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param max_num_segments: The number of segments the index should be merged into
            (default: dynamic)
        :param only_expunge_deletes: Specify whether the operation should only expunge
            deleted documents
        :param wait_for_completion: Should the request wait until the force merge is
            completed.
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_forcemerge"
        else:
            __path = "/_forcemerge"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flush is not None:
            __query["flush"] = flush
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if max_num_segments is not None:
            __query["max_num_segments"] = max_num_segments
        if only_expunge_deletes is not None:
            __query["only_expunge_deletes"] = only_expunge_deletes
        if pretty is not None:
            __query["pretty"] = pretty
        if wait_for_completion is not None:
            __query["wait_for_completion"] = wait_for_completion
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        features: t.Optional[
            t.Union[
                t.Union["t.Literal['aliases', 'mappings', 'settings']", str],
                t.Union[
                    t.List[
                        t.Union["t.Literal['aliases', 'mappings', 'settings']", str]
                    ],
                    t.Tuple[
                        t.Union["t.Literal['aliases', 'mappings', 'settings']", str],
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
        include_defaults: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns information about one or more indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-get-index.html>`_

        :param index: Comma-separated list of data streams, indices, and index aliases
            used to limit the request. Wildcard expressions (*) are supported.
        :param allow_no_indices: If false, the request returns an error if any wildcard
            expression, index alias, or _all value targets only missing or closed indices.
            This behavior applies even if the request targets other open indices. For
            example, a request targeting foo*,bar* returns an error if an index starts
            with foo but no index starts with bar.
        :param expand_wildcards: Type of index that wildcard expressions can match. If
            the request can target data streams, this argument determines whether wildcard
            expressions match hidden data streams. Supports comma-separated values, such
            as open,hidden.
        :param features: Return only information on specified index features
        :param flat_settings: If true, returns settings in flat format.
        :param ignore_unavailable: If false, requests that target a missing index return
            an error.
        :param include_defaults: If true, return all default settings in the response.
        :param local: If true, the request retrieves information from the local node
            only. Defaults to false, which means information is retrieved from the master
            node.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if features is not None:
            __query["features"] = features
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
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
    def get_alias(
        self,
        *,
        index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns an alias.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-aliases.html>`_

        :param index: A comma-separated list of index names to filter aliases
        :param name: A comma-separated list of alias names to return
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        """
        if index not in SKIP_IN_PATH and name not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_alias/{_quote(name)}"
        elif index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_alias"
        elif name not in SKIP_IN_PATH:
            __path = f"/_alias/{_quote(name)}"
        else:
            __path = "/_alias"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if local is not None:
            __query["local"] = local
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_data_lifecycle(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        include_defaults: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns the data lifecycle of the selected data streams.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/dlm-get-lifecycle.html>`_

        :param name: A comma-separated list of data streams to get; use `*` to get all
            data streams
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open or closed indices (default: open)
        :param include_defaults: Return all relevant default configurations for the data
            stream (default: false)
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_data_stream/{_quote(name)}/_lifecycle"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_data_stream(
        self,
        *,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
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
        include_defaults: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns data streams.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/data-streams.html>`_

        :param name: A comma-separated list of data streams to get; use `*` to get all
            data streams
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open or closed indices (default: open)
        :param include_defaults: If true, returns all relevant default configurations
            for the index template.
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_data_stream/{_quote(name)}"
        else:
            __path = "/_data_stream"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_field_mapping(
        self,
        *,
        fields: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        include_defaults: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns mapping for one or more fields.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-get-field-mapping.html>`_

        :param fields: A comma-separated list of fields
        :param index: A comma-separated list of index names
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param include_defaults: Whether the default mapping values should be returned
            as well
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        """
        if fields in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'fields'")
        if index not in SKIP_IN_PATH and fields not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_mapping/field/{_quote(fields)}"
        elif fields not in SKIP_IN_PATH:
            __path = f"/_mapping/field/{_quote(fields)}"
        else:
            raise ValueError("Couldn't find a path for the given parameters")
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if local is not None:
            __query["local"] = local
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_index_template(
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
        Returns an index template.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: Comma-separated list of index template names used to limit the request.
            Wildcard (*) expressions are supported.
        :param flat_settings: If true, returns settings in flat format.
        :param include_defaults: If true, returns all relevant default configurations
            for the index template.
        :param local: If true, the request retrieves information from the local node
            only. Defaults to false, which means information is retrieved from the master
            node.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_index_template/{_quote(name)}"
        else:
            __path = "/_index_template"
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
    def get_mapping(
        self,
        *,
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns mappings for one or more indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-get-mapping.html>`_

        :param index: A comma-separated list of index names
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Specify timeout for connection to master
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_mapping"
        else:
            __path = "/_mapping"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
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
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def get_settings(
        self,
        *,
        index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
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
        include_defaults: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns settings for one or more indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-get-settings.html>`_

        :param index: A comma-separated list of index names; use `_all` or empty string
            to perform the operation on all indices
        :param name: The name of the settings that should be included
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param flat_settings: Return settings in flat format (default: false)
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param include_defaults: Whether to return all default setting for each of the
            indices.
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Specify timeout for connection to master
        """
        if index not in SKIP_IN_PATH and name not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_settings/{_quote(name)}"
        elif index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_settings"
        elif name not in SKIP_IN_PATH:
            __path = f"/_settings/{_quote(name)}"
        else:
            __path = "/_settings"
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
    def get_template(
        self,
        *,
        name: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        local: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns an index template.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: The comma separated names of the index templates
        :param flat_settings: Return settings in flat format (default: false)
        :param local: Return local information, do not retrieve the state from master
            node (default: false)
        :param master_timeout: Explicit operation timeout for connection to master node
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_template/{_quote(name)}"
        else:
            __path = "/_template"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
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
    def migrate_to_data_stream(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Migrates an alias to a data stream

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/data-streams.html>`_

        :param name: The name of the alias to migrate
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_data_stream/_migrate/{_quote(name)}"
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
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def modify_data_stream(
        self,
        *,
        actions: t.Union[
            t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]
        ],
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Modifies a data stream

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/data-streams.html>`_

        :param actions: Actions to perform.
        """
        if actions is None:
            raise ValueError("Empty value passed for parameter 'actions'")
        __path = "/_data_stream/_modify"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if actions is not None:
            __body["actions"] = actions
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def open(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Opens an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-open-close.html>`_

        :param index: A comma separated list of indices to open
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Sets the number of active shards to wait for before
            the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_open"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def promote_data_stream(
        self,
        *,
        name: str,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Promotes a data stream from a replicated data stream managed by CCR to a regular
        data stream

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/data-streams.html>`_

        :param name: The name of the data stream
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_data_stream/_promote/{_quote(name)}"
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
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_alias(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        name: str,
        error_trace: t.Optional[bool] = None,
        filter: t.Optional[t.Mapping[str, t.Any]] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        index_routing: t.Optional[str] = None,
        is_write_index: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        routing: t.Optional[str] = None,
        search_routing: t.Optional[str] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates or updates an alias.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-aliases.html>`_

        :param index: A comma-separated list of index names the alias should point to
            (supports wildcards); use `_all` to perform the operation on all indices.
        :param name: The name of the alias to be created or updated
        :param filter:
        :param index_routing:
        :param is_write_index:
        :param master_timeout: Specify timeout for connection to master
        :param routing:
        :param search_routing:
        :param timeout: Explicit timestamp for the document
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/{_quote(index)}/_alias/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter is not None:
            __body["filter"] = filter
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if index_routing is not None:
            __body["index_routing"] = index_routing
        if is_write_index is not None:
            __body["is_write_index"] = is_write_index
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if routing is not None:
            __body["routing"] = routing
        if search_routing is not None:
            __body["search_routing"] = search_routing
        if timeout is not None:
            __query["timeout"] = timeout
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_data_lifecycle(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        data_retention: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
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
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the data lifecycle of the selected data streams.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/dlm-put-lifecycle.html>`_

        :param name: A comma-separated list of data streams whose lifecycle will be updated;
            use `*` to set the lifecycle to all data streams
        :param data_retention:
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open or closed indices (default: open)
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit timestamp for the document
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_data_stream/{_quote(name)}/_lifecycle"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if data_retention is not None:
            __body["data_retention"] = data_retention
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
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
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"_meta": "meta"},
    )
    def put_index_template(
        self,
        *,
        name: str,
        composed_of: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        create: t.Optional[bool] = None,
        data_stream: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        index_patterns: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        meta: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        priority: t.Optional[int] = None,
        template: t.Optional[t.Mapping[str, t.Any]] = None,
        version: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates or updates an index template.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: Index or template name
        :param composed_of:
        :param create: Whether the index template should only be added if new or can
            also replace an existing one
        :param data_stream:
        :param index_patterns:
        :param meta:
        :param priority:
        :param template:
        :param version:
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_index_template/{_quote(name)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if composed_of is not None:
            __body["composed_of"] = composed_of
        if create is not None:
            __query["create"] = create
        if data_stream is not None:
            __body["data_stream"] = data_stream
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if index_patterns is not None:
            __body["index_patterns"] = index_patterns
        if meta is not None:
            __body["_meta"] = meta
        if pretty is not None:
            __query["pretty"] = pretty
        if priority is not None:
            __body["priority"] = priority
        if template is not None:
            __body["template"] = template
        if version is not None:
            __body["version"] = version
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={
            "_field_names": "field_names",
            "_meta": "meta",
            "_routing": "routing",
            "_source": "source",
        },
    )
    def put_mapping(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
        allow_no_indices: t.Optional[bool] = None,
        date_detection: t.Optional[bool] = None,
        dynamic: t.Optional[
            t.Union["t.Literal['false', 'runtime', 'strict', 'true']", str]
        ] = None,
        dynamic_date_formats: t.Optional[
            t.Union[t.List[str], t.Tuple[str, ...]]
        ] = None,
        dynamic_templates: t.Optional[
            t.Union[
                t.Mapping[str, t.Mapping[str, t.Any]],
                t.Union[
                    t.List[t.Mapping[str, t.Mapping[str, t.Any]]],
                    t.Tuple[t.Mapping[str, t.Mapping[str, t.Any]], ...],
                ],
            ]
        ] = None,
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
        field_names: t.Optional[t.Mapping[str, t.Any]] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        meta: t.Optional[t.Mapping[str, t.Any]] = None,
        numeric_detection: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        properties: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        routing: t.Optional[t.Mapping[str, t.Any]] = None,
        runtime: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        source: t.Optional[t.Mapping[str, t.Any]] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        write_index_only: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the index mappings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-put-mapping.html>`_

        :param index: A comma-separated list of index names the mapping should be added
            to (supports wildcards); use `_all` or omit to add the mapping on all indices.
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param date_detection: Controls whether dynamic date detection is enabled.
        :param dynamic: Controls whether new fields are added dynamically.
        :param dynamic_date_formats: If date detection is enabled then new string fields
            are checked against 'dynamic_date_formats' and if the value matches then
            a new date field is added instead of string.
        :param dynamic_templates: Specify dynamic templates for the mapping.
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param field_names: Control whether field names are enabled for the index.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param master_timeout: Specify timeout for connection to master
        :param meta: A mapping type can have custom meta data associated with it. These
            are not used at all by Elasticsearch, but can be used to store application-specific
            metadata.
        :param numeric_detection: Automatically map strings into numeric data types for
            all fields.
        :param properties: Mapping for a field. For new fields, this mapping can include:
            - Field name - Field data type - Mapping parameters
        :param routing: Enable making a routing value required on indexed documents.
        :param runtime: Mapping of runtime fields for the index.
        :param source: Control whether the _source field is enabled on the index.
        :param timeout: Explicit operation timeout
        :param write_index_only: When true, applies mappings only to the write index
            of an alias or data stream
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_mapping"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if date_detection is not None:
            __body["date_detection"] = date_detection
        if dynamic is not None:
            __body["dynamic"] = dynamic
        if dynamic_date_formats is not None:
            __body["dynamic_date_formats"] = dynamic_date_formats
        if dynamic_templates is not None:
            __body["dynamic_templates"] = dynamic_templates
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if field_names is not None:
            __body["_field_names"] = field_names
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if meta is not None:
            __body["_meta"] = meta
        if numeric_detection is not None:
            __body["numeric_detection"] = numeric_detection
        if pretty is not None:
            __query["pretty"] = pretty
        if properties is not None:
            __body["properties"] = properties
        if routing is not None:
            __body["_routing"] = routing
        if runtime is not None:
            __body["runtime"] = runtime
        if source is not None:
            __body["_source"] = source
        if timeout is not None:
            __query["timeout"] = timeout
        if write_index_only is not None:
            __query["write_index_only"] = write_index_only
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_name="settings",
    )
    def put_settings(
        self,
        *,
        settings: t.Mapping[str, t.Any],
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
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        preserve_existing: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates the index settings.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-update-settings.html>`_

        :param settings:
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
        :param master_timeout: Specify timeout for connection to master
        :param preserve_existing: Whether to update existing settings. If set to `true`
            existing settings on an index remain unchanged, the default is `false`
        :param timeout: Explicit operation timeout
        """
        if settings is None:
            raise ValueError("Empty value passed for parameter 'settings'")
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_settings"
        else:
            __path = "/_settings"
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
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if preserve_existing is not None:
            __query["preserve_existing"] = preserve_existing
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        __body = settings
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def put_template(
        self,
        *,
        name: str,
        aliases: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        create: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        flat_settings: t.Optional[bool] = None,
        human: t.Optional[bool] = None,
        index_patterns: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        mappings: t.Optional[t.Mapping[str, t.Any]] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        order: t.Optional[int] = None,
        pretty: t.Optional[bool] = None,
        settings: t.Optional[t.Mapping[str, t.Any]] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        version: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Creates or updates an index template.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: The name of the template
        :param aliases: Aliases for the index.
        :param create: If true, this request cannot replace or update existing index
            templates.
        :param flat_settings:
        :param index_patterns: Array of wildcard expressions used to match the names
            of indices during creation.
        :param mappings: Mapping for fields in the index.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param order: Order in which Elasticsearch applies this template if index matches
            multiple templates. Templates with lower 'order' values are merged first.
            Templates with higher 'order' values are merged later, overriding templates
            with lower values.
        :param settings: Configuration options for the index.
        :param timeout:
        :param version: Version number used to manage index templates externally. This
            number is not automatically generated by Elasticsearch.
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_template/{_quote(name)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if aliases is not None:
            __body["aliases"] = aliases
        if create is not None:
            __query["create"] = create
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if flat_settings is not None:
            __query["flat_settings"] = flat_settings
        if human is not None:
            __query["human"] = human
        if index_patterns is not None:
            __body["index_patterns"] = index_patterns
        if mappings is not None:
            __body["mappings"] = mappings
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if order is not None:
            __body["order"] = order
        if pretty is not None:
            __query["pretty"] = pretty
        if settings is not None:
            __body["settings"] = settings
        if timeout is not None:
            __query["timeout"] = timeout
        if version is not None:
            __body["version"] = version
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def recovery(
        self,
        *,
        index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        active_only: t.Optional[bool] = None,
        detailed: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns information about ongoing index shard recoveries.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-recovery.html>`_

        :param index: A comma-separated list of index names; use `_all` or empty string
            to perform the operation on all indices
        :param active_only: Display only those recoveries that are currently on-going
        :param detailed: Whether to display detailed information about shard recovery
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_recovery"
        else:
            __path = "/_recovery"
        __query: t.Dict[str, t.Any] = {}
        if active_only is not None:
            __query["active_only"] = active_only
        if detailed is not None:
            __query["detailed"] = detailed
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
    def refresh(
        self,
        *,
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Performs the refresh operation in one or more indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-refresh.html>`_

        :param index: A comma-separated list of index names; use `_all` or empty string
            to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_refresh"
        else:
            __path = "/_refresh"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def reload_search_analyzers(
        self,
        *,
        index: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Reloads an index's search analyzers and their resources.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-reload-analyzers.html>`_

        :param index: A comma-separated list of index names to reload analyzers for
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_reload_search_analyzers"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def resolve_index(
        self,
        *,
        name: t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]],
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
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Returns information about any matching indices, aliases, and data streams

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-resolve-index-api.html>`_

        :param name: A comma-separated list of names or wildcard expressions
        :param expand_wildcards: Whether wildcard expressions should get expanded to
            open or closed indices (default: open)
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_resolve/index/{_quote(name)}"
        __query: t.Dict[str, t.Any] = {}
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
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
    def rollover(
        self,
        *,
        alias: str,
        new_index: t.Optional[str] = None,
        aliases: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        conditions: t.Optional[t.Mapping[str, t.Any]] = None,
        dry_run: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        mappings: t.Optional[t.Mapping[str, t.Any]] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        settings: t.Optional[t.Mapping[str, t.Any]] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Updates an alias to point to a new index when the existing index is considered
        to be too large or too old.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-rollover-index.html>`_

        :param alias: The name of the alias to rollover
        :param new_index: The name of the rollover index
        :param aliases:
        :param conditions:
        :param dry_run: If set to true the rollover action will only be validated but
            not actually performed even if a condition matches. The default is false
        :param mappings:
        :param master_timeout: Specify timeout for connection to master
        :param settings:
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Set the number of active shards to wait for on
            the newly created rollover index before the operation returns.
        """
        if alias in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'alias'")
        if alias not in SKIP_IN_PATH and new_index not in SKIP_IN_PATH:
            __path = f"/{_quote(alias)}/_rollover/{_quote(new_index)}"
        elif alias not in SKIP_IN_PATH:
            __path = f"/{_quote(alias)}/_rollover"
        else:
            raise ValueError("Couldn't find a path for the given parameters")
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if aliases is not None:
            __body["aliases"] = aliases
        if conditions is not None:
            __body["conditions"] = conditions
        if dry_run is not None:
            __query["dry_run"] = dry_run
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if mappings is not None:
            __body["mappings"] = mappings
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if settings is not None:
            __body["settings"] = settings
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def segments(
        self,
        *,
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        verbose: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Provides low-level information about segments in a Lucene index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-segments.html>`_

        :param index: A comma-separated list of index names; use `_all` or empty string
            to perform the operation on all indices
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param verbose: Includes detailed memory usage by Lucene.
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_segments"
        else:
            __path = "/_segments"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        if verbose is not None:
            __query["verbose"] = verbose
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def shard_stores(
        self,
        *,
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        status: t.Optional[
            t.Union[
                t.Union["t.Literal['all', 'green', 'red', 'yellow']", str],
                t.Union[
                    t.List[t.Union["t.Literal['all', 'green', 'red', 'yellow']", str]],
                    t.Tuple[
                        t.Union["t.Literal['all', 'green', 'red', 'yellow']", str], ...
                    ],
                ],
            ]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Provides store information for shard copies of indices.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-shards-stores.html>`_

        :param index: List of data streams, indices, and aliases used to limit the request.
        :param allow_no_indices: If false, the request returns an error if any wildcard
            expression, index alias, or _all value targets only missing or closed indices.
            This behavior applies even if the request targets other open indices.
        :param expand_wildcards: Type of index that wildcard patterns can match. If the
            request can target data streams, this argument determines whether wildcard
            expressions match hidden data streams.
        :param ignore_unavailable: If true, missing or closed indices are not included
            in the response.
        :param status: List of shard health statuses used to limit the request.
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_shard_stores"
        else:
            __path = "/_shard_stores"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if pretty is not None:
            __query["pretty"] = pretty
        if status is not None:
            __query["status"] = status
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def shrink(
        self,
        *,
        index: str,
        target: str,
        aliases: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        settings: t.Optional[t.Mapping[str, t.Any]] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Allow to shrink an existing index into a new index with fewer primary shards.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-shrink-index.html>`_

        :param index: The name of the source index to shrink
        :param target: The name of the target index to shrink into
        :param aliases:
        :param master_timeout: Specify timeout for connection to master
        :param settings:
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Set the number of active shards to wait for on
            the shrunken index before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if target in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'target'")
        __path = f"/{_quote(index)}/_shrink/{_quote(target)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if aliases is not None:
            __body["aliases"] = aliases
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
        if settings is not None:
            __body["settings"] = settings
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
        parameter_aliases={"_meta": "meta"},
    )
    def simulate_index_template(
        self,
        *,
        name: str,
        allow_auto_create: t.Optional[bool] = None,
        composed_of: t.Optional[t.Union[t.List[str], t.Tuple[str, ...]]] = None,
        create: t.Optional[bool] = None,
        data_stream: t.Optional[t.Mapping[str, t.Any]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        include_defaults: t.Optional[bool] = None,
        index_patterns: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        meta: t.Optional[t.Mapping[str, t.Any]] = None,
        pretty: t.Optional[bool] = None,
        priority: t.Optional[int] = None,
        template: t.Optional[t.Mapping[str, t.Any]] = None,
        version: t.Optional[int] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Simulate matching the given index name against the index templates in the system

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: Index or template name to simulate
        :param allow_auto_create:
        :param composed_of:
        :param create: If `true`, the template passed in the body is only used if no
            existing templates match the same index patterns. If `false`, the simulation
            uses the template with the highest priority. Note that the template is not
            permanently added or updated in either case; it is only used for the simulation.
        :param data_stream:
        :param include_defaults: If true, returns all relevant default configurations
            for the index template.
        :param index_patterns:
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param meta:
        :param priority:
        :param template:
        :param version:
        """
        if name in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'name'")
        __path = f"/_index_template/_simulate_index/{_quote(name)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if allow_auto_create is not None:
            __body["allow_auto_create"] = allow_auto_create
        if composed_of is not None:
            __body["composed_of"] = composed_of
        if create is not None:
            __query["create"] = create
        if data_stream is not None:
            __body["data_stream"] = data_stream
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if index_patterns is not None:
            __body["index_patterns"] = index_patterns
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if meta is not None:
            __body["_meta"] = meta
        if pretty is not None:
            __query["pretty"] = pretty
        if priority is not None:
            __body["priority"] = priority
        if template is not None:
            __body["template"] = template
        if version is not None:
            __body["version"] = version
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_name="template",
    )
    def simulate_template(
        self,
        *,
        name: t.Optional[str] = None,
        create: t.Optional[bool] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        include_defaults: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        template: t.Optional[t.Mapping[str, t.Any]] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Simulate resolving the given template name or body

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-templates.html>`_

        :param name: Name of the index template to simulate. To test a template configuration
            before you add it to the cluster, omit this parameter and specify the template
            configuration in the request body.
        :param create: If true, the template passed in the body is only used if no existing
            templates match the same index patterns. If false, the simulation uses the
            template with the highest priority. Note that the template is not permanently
            added or updated in either case; it is only used for the simulation.
        :param include_defaults: If true, returns all relevant default configurations
            for the index template.
        :param master_timeout: Period to wait for a connection to the master node. If
            no response is received before the timeout expires, the request fails and
            returns an error.
        :param template:
        """
        if name not in SKIP_IN_PATH:
            __path = f"/_index_template/_simulate/{_quote(name)}"
        else:
            __path = "/_index_template/_simulate"
        __query: t.Dict[str, t.Any] = {}
        if create is not None:
            __query["create"] = create
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if include_defaults is not None:
            __query["include_defaults"] = include_defaults
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        __body = template
        if not __body:
            __body = None
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def split(
        self,
        *,
        index: str,
        target: str,
        aliases: t.Optional[t.Mapping[str, t.Mapping[str, t.Any]]] = None,
        error_trace: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        settings: t.Optional[t.Mapping[str, t.Any]] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[
            t.Union[int, t.Union["t.Literal['all', 'index-setting']", str]]
        ] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Allows you to split an existing index into a new index with more primary shards.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-split-index.html>`_

        :param index: The name of the source index to split
        :param target: The name of the target index to split into
        :param aliases:
        :param master_timeout: Specify timeout for connection to master
        :param settings:
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Set the number of active shards to wait for on
            the shrunken index before the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        if target in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'target'")
        __path = f"/{_quote(index)}/_split/{_quote(target)}"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if aliases is not None:
            __body["aliases"] = aliases
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
        if settings is not None:
            __body["settings"] = settings
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "PUT", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters()
    def stats(
        self,
        *,
        index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        metric: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        completion_fields: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
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
        fielddata_fields: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        fields: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        forbid_closed_indices: t.Optional[bool] = None,
        groups: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        include_segment_file_sizes: t.Optional[bool] = None,
        include_unloaded_segments: t.Optional[bool] = None,
        level: t.Optional[
            t.Union["t.Literal['cluster', 'indices', 'shards']", str]
        ] = None,
        pretty: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Provides statistics on operations happening in an index.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-stats.html>`_

        :param index: A comma-separated list of index names; use `_all` or empty string
            to perform the operation on all indices
        :param metric: Limit the information returned the specific metrics.
        :param completion_fields: Comma-separated list or wildcard expressions of fields
            to include in fielddata and suggest statistics.
        :param expand_wildcards: Type of index that wildcard patterns can match. If the
            request can target data streams, this argument determines whether wildcard
            expressions match hidden data streams. Supports comma-separated values, such
            as `open,hidden`.
        :param fielddata_fields: Comma-separated list or wildcard expressions of fields
            to include in fielddata statistics.
        :param fields: Comma-separated list or wildcard expressions of fields to include
            in the statistics.
        :param forbid_closed_indices: If true, statistics are not collected from closed
            indices.
        :param groups: Comma-separated list of search groups to include in the search
            statistics.
        :param include_segment_file_sizes: If true, the call reports the aggregated disk
            usage of each one of the Lucene index files (only applies if segment stats
            are requested).
        :param include_unloaded_segments: If true, the response includes information
            from segments that are not loaded into memory.
        :param level: Indicates whether statistics are aggregated at the cluster, index,
            or shard level.
        """
        if index not in SKIP_IN_PATH and metric not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_stats/{_quote(metric)}"
        elif index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_stats"
        elif metric not in SKIP_IN_PATH:
            __path = f"/_stats/{_quote(metric)}"
        else:
            __path = "/_stats"
        __query: t.Dict[str, t.Any] = {}
        if completion_fields is not None:
            __query["completion_fields"] = completion_fields
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if fielddata_fields is not None:
            __query["fielddata_fields"] = fielddata_fields
        if fields is not None:
            __query["fields"] = fields
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if forbid_closed_indices is not None:
            __query["forbid_closed_indices"] = forbid_closed_indices
        if groups is not None:
            __query["groups"] = groups
        if human is not None:
            __query["human"] = human
        if include_segment_file_sizes is not None:
            __query["include_segment_file_sizes"] = include_segment_file_sizes
        if include_unloaded_segments is not None:
            __query["include_unloaded_segments"] = include_unloaded_segments
        if level is not None:
            __query["level"] = level
        if pretty is not None:
            __query["pretty"] = pretty
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "GET", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters()
    def unfreeze(
        self,
        *,
        index: str,
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
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        master_timeout: t.Optional[
            t.Union["t.Literal[-1]", "t.Literal[0]", str]
        ] = None,
        pretty: t.Optional[bool] = None,
        timeout: t.Optional[t.Union["t.Literal[-1]", "t.Literal[0]", str]] = None,
        wait_for_active_shards: t.Optional[str] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Unfreezes an index. When a frozen index is unfrozen, the index goes through the
        normal recovery process and becomes writeable again.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/unfreeze-index-api.html>`_

        :param index: The name of the index to unfreeze
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Explicit operation timeout
        :param wait_for_active_shards: Sets the number of active shards to wait for before
            the operation returns.
        """
        if index in SKIP_IN_PATH:
            raise ValueError("Empty value passed for parameter 'index'")
        __path = f"/{_quote(index)}/_unfreeze"
        __query: t.Dict[str, t.Any] = {}
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if master_timeout is not None:
            __query["master_timeout"] = master_timeout
        if pretty is not None:
            __query["pretty"] = pretty
        if timeout is not None:
            __query["timeout"] = timeout
        if wait_for_active_shards is not None:
            __query["wait_for_active_shards"] = wait_for_active_shards
        __headers = {"accept": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def update_aliases(
        self,
        *,
        actions: t.Optional[
            t.Union[t.List[t.Mapping[str, t.Any]], t.Tuple[t.Mapping[str, t.Any], ...]]
        ] = None,
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
        Updates index aliases.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/indices-aliases.html>`_

        :param actions:
        :param master_timeout: Specify timeout for connection to master
        :param timeout: Request timeout
        """
        __path = "/_aliases"
        __body: t.Dict[str, t.Any] = {}
        __query: t.Dict[str, t.Any] = {}
        if actions is not None:
            __body["actions"] = actions
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
        __headers = {"accept": "application/json", "content-type": "application/json"}
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

    @_rewrite_parameters(
        body_fields=True,
    )
    def validate_query(
        self,
        *,
        index: t.Optional[t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]] = None,
        all_shards: t.Optional[bool] = None,
        allow_no_indices: t.Optional[bool] = None,
        analyze_wildcard: t.Optional[bool] = None,
        analyzer: t.Optional[str] = None,
        default_operator: t.Optional[t.Union["t.Literal['and', 'or']", str]] = None,
        df: t.Optional[str] = None,
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
        explain: t.Optional[bool] = None,
        filter_path: t.Optional[
            t.Union[str, t.Union[t.List[str], t.Tuple[str, ...]]]
        ] = None,
        human: t.Optional[bool] = None,
        ignore_unavailable: t.Optional[bool] = None,
        lenient: t.Optional[bool] = None,
        pretty: t.Optional[bool] = None,
        q: t.Optional[str] = None,
        query: t.Optional[t.Mapping[str, t.Any]] = None,
        rewrite: t.Optional[bool] = None,
    ) -> ObjectApiResponse[t.Any]:
        """
        Allows a user to validate a potentially expensive query without executing it.

        `<https://www.elastic.co/guide/en/elasticsearch/reference/8.9/search-validate.html>`_

        :param index: A comma-separated list of index names to restrict the operation;
            use `_all` or empty string to perform the operation on all indices
        :param all_shards: Execute validation on all shards instead of one random shard
            per index
        :param allow_no_indices: Whether to ignore if a wildcard indices expression resolves
            into no concrete indices. (This includes `_all` string or when no indices
            have been specified)
        :param analyze_wildcard: Specify whether wildcard and prefix queries should be
            analyzed (default: false)
        :param analyzer: The analyzer to use for the query string
        :param default_operator: The default operator for query string query (AND or
            OR)
        :param df: The field to use as default where no field prefix is given in the
            query string
        :param expand_wildcards: Whether to expand wildcard expression to concrete indices
            that are open, closed or both.
        :param explain: Return detailed information about the error
        :param ignore_unavailable: Whether specified concrete indices should be ignored
            when unavailable (missing or closed)
        :param lenient: Specify whether format-based query failures (such as providing
            text to a numeric field) should be ignored
        :param q: Query in the Lucene query string syntax
        :param query:
        :param rewrite: Provide a more detailed explanation showing the actual Lucene
            query that will be executed.
        """
        if index not in SKIP_IN_PATH:
            __path = f"/{_quote(index)}/_validate/query"
        else:
            __path = "/_validate/query"
        __query: t.Dict[str, t.Any] = {}
        __body: t.Dict[str, t.Any] = {}
        if all_shards is not None:
            __query["all_shards"] = all_shards
        if allow_no_indices is not None:
            __query["allow_no_indices"] = allow_no_indices
        if analyze_wildcard is not None:
            __query["analyze_wildcard"] = analyze_wildcard
        if analyzer is not None:
            __query["analyzer"] = analyzer
        if default_operator is not None:
            __query["default_operator"] = default_operator
        if df is not None:
            __query["df"] = df
        if error_trace is not None:
            __query["error_trace"] = error_trace
        if expand_wildcards is not None:
            __query["expand_wildcards"] = expand_wildcards
        if explain is not None:
            __query["explain"] = explain
        if filter_path is not None:
            __query["filter_path"] = filter_path
        if human is not None:
            __query["human"] = human
        if ignore_unavailable is not None:
            __query["ignore_unavailable"] = ignore_unavailable
        if lenient is not None:
            __query["lenient"] = lenient
        if pretty is not None:
            __query["pretty"] = pretty
        if q is not None:
            __query["q"] = q
        if query is not None:
            __body["query"] = query
        if rewrite is not None:
            __query["rewrite"] = rewrite
        if not __body:
            __body = None  # type: ignore[assignment]
        __headers = {"accept": "application/json"}
        if __body is not None:
            __headers["content-type"] = "application/json"
        return self.perform_request(  # type: ignore[return-value]
            "POST", __path, params=__query, headers=__headers, body=__body
        )

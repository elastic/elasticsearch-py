---
navigation_title: "Elasticsearch Python Client"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/release-notes.html
---

# Elasticsearch Python Client release notes [elasticsearch-python-client-release-notes]

Review the changes, fixes, and more in each version of Elasticsearch Python Client.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [elasticsearch-python-client-next-release-notes]

% ### Features and enhancements [elasticsearch-python-client-next-features-enhancements]
% *

% ### Fixes [elasticsearch-python-client-next-fixes]
## 9.3.0 (2026-02-03)

Enhancements

* Add `pack_dense_vector` helper function to pack dense vectors for efficient uploading ([#3219](https://github.com/elastic/elasticsearch-py/pull/3219))
* Updates to ES|QL functions for 9.3 and Serverless ([#3266](https://github.com/elastic/elasticsearch-py/pull/3266))

API

* Added `cat.circuit_breaker` API
* Added `esql.get_view`, `esql.put_view` and `esql.delete_view` APIs
* Added `indices.get_sample_configuration`, `indices.put_sample_configuration`, `indices.delete_sample_configuration`, `indices.get_all_sample_configuration` APIs
* Added `inference.put_groq`, `inference.put_openshift_ai`, `inference.put_nvidia` APIs
* Added `transform.get_node_stats` API
* Added `requests_per_second` argument to `delete_by_query_rethrottle`, `reindex_rethrottle` and `update_by_query_rethrottle` APIs
* Added `allow_closed`, `allow_no_indices`, `expand_wildcards`, `ignore_throttled` and `ignore_available` arguments to `cat.segments` API
* Added `downsampling_method` argument to `indices.put_alias` API
* Added `chunking_settings` argument to `inference.put_watsonxai` API
* Added `return_documents` and `top_n` arguments to `inference.rerank` API
* Added `id` argument to `ml.stop_trained_model_deployment` API
* Added `close_job` argument to `ml.stop_data_frame_analytics` API
* Added `project_routing` argument to `project.tags` API
* Added `certificate_identity` to `security.create_cross_cluster_api_key` and `security.update_cross_cluster_api_key` APIs
* Removed `chunking_settings` argument from `inference.put_anthropic`, `inference.put_contextualai`, `inference.put_deepseek` APIs

DSL

* Added `NumpyDenseVector` field, with support for dense vectors based on numpy arrays ([#3218](https://github.com/elastic/elasticsearch-py/pull/3218))
* Added `ExponentialHistogram` field
* Added `time_series_metric` argument to `Histogram` field
* Added `slices` argument to `UpdateByQueryResponse` type

## 9.2.1 (2025-12-23)

Enhancements

* Instrument ping with OTel ([#3160](https://github.com/elastic/elasticsearch-py/pull/3160))
* Make positional arguments in DSL generated classes explicit  ([#3233](https://github.com/elastic/elasticsearch-py/pull/3233))
* Add warnings for private APIs ([#3212](https://github.com/elastic/elasticsearch-py/pull/3212))

Bug fixes

* ES|QL query builder: fix missing assignment ([#3151](https://github.com/elastic/elasticsearch-py/pull/3151))
* Use relative imports to fix `elasticsearch9` package imports ([#3232](https://github.com/elastic/elasticsearch-py/pull/3232))

API

* Added `transform.get_node_stats` API
* Added `requests_per_second` argument to `delete_by_query_rethrottle`, `reindex_rethrottle` and `update_by_query_rethrottle` APIs
* Added `allow_closed`, `allow_no_indices`, `expand_wildcards`, `ignore_throttled` and `ignore_available` arguments to `cat.segments` API
* Added `chunking_settings` argument to `inference.put_watsonxai` API
* Added `id` argument to `ml.stop_trained_model_deployment` API
* Removed `chunking_settings` argument from `inference.put_anthropic`, `inference.put_contextualai`, `inference.put_deepseek` APIs

DSL

* Removed `on_disk_score` argument from `DenseVectorIndexOptions` type


## 9.2.0 (2025-10-28)

### Enhancements

* Support Trio when using the [HTTPX](https://www.python-httpx.org/) async client ([#3089](https://github.com/elastic/elasticsearch-py/pull/3089))
* Pydantic integration for the DSL module ([#3086](https://github.com/elastic/elasticsearch-py/pull/3086))
* Add `flush_after_seconds` option to `streaming_bulk()` ([#3064](https://github.com/elastic/elasticsearch-py/pull/3064))
* Add `TS`, `FUSE` and `INLINE STATS` commands to the ES|QL query builder ([#3096](https://github.com/elastic/elasticsearch-py/pull/3096))

### Bug Fixes

* DSL: support passing inner documents as `AttrDict` instances ([#3080](https://github.com/elastic/elasticsearch-py/pull/3080))
* DSL: add some recently added field classes as top-level exports for the package ([#3078](https://github.com/elastic/elasticsearch-py/pull/3078))

### API

- Add `source_exclude_vectors` to Field Caps, Scroll and Search APIs
- Add `require_data_stream` to Index API
- Add `settings_filter` to Cluster Get Component Template API
- Add `cause` to Cluster Put Component Template API
- Add `master_timeout` to Cluster State API
- Add `ccs_minimize_roundtrips` to EQL Search API
- Add `keep_alive` and `keep_on_completion` to ES|QL Async Query API
- Add `format` to ES|QL Async Query Get API
- Add ES|QL Get Query and List Queries APIs
- Add Indices Delete Data Stream Options API
- Add Indices Get Data Stream Mappings and Put Data Stream Mappings APIs
- Add Indices Get Data Stream Options and Put Data Stream Options APIS
- Add Indices Get Data Stream Settings and Put Data Stream Settings APIs
- Add `allow_no_indices`, `expand_wildcards` and `ignore_available` to Indices Recovery API
- Add Indices Remove Block API
- Add `input_type` to Inference API
- Add `timeout` to all Inference Put APIs
- Add Inference Put Custom API
- Add Inference Put DeepSeek API
- Add `task_settings` to Put HuggingFace API
- Add `streams` namespace with `streams.logs_disable`, `streams.logs_enable`, `streams.status` APIs
- Add `inference.contextualai` API
- Add `security.get_stats` API
- Add `bytes` and `time` parameters to various APIs in the `cat` namespace.
- Add `include_execution_metadata` parameter to `esql.async_query` and `esql.query` APIs
- Add `index_template` parameter to `indices.simulate_index_template` API
- Add `input_type` parameter to `inference.text_embedding` API
- Add `field_access_pattern` parameter to `ingest.put_pipeline` API
- Add `refresh` to Security Grant API Key API
- Add `wait_for_completion` to the Snapshot Delete API
- Add `state` to Snapshot Get API
- Add `refresh` to Synonyms Put Synonym, Put Synonym Rule and Delete Synonym Rule APIs
- Remove unsupported `size` parameter from `reindex` API
- Remove deprecated `if_primary_term`, `if_seq_no` and `op_type` from Create API
- Remove deprecated `master_timeout` from Ingest Get Ip Location Database API
- Remove deprecated `application`, `priviledge` and `username` from the Security Get User API
- Rename `type_query_string` to `type` in License Post Start Trial API

#### Serverless-specific

- Add `project` namespace with `project.tags` API
- Add `project_routing` parameter to `count`, `field_caps`, `msearch`, `msearch_template`, `open_point_in_time`, `search`, `search_mvt`, `search_template`, `async_search.submit`, `cat.count`, `eql.search`, `indices.resolve_index`, `sql.query` APIs

### DSL

- New `CartesianBounds`, `CartesianCentroid`, `ChangePoint` aggregations
- Add `p_value` parameter to `SignificantTerms` aggregation
- Add `fields` parameter to `SemanticText` field
- Add `visit_percentage` parameter to `Knn` query
- Add `on_disk_rescore` field to `DenseVectorIndexOptions` type
- Add `sparse_vector` field to `SemanticTextIndexOptions` type
- Add `index_options` to SparseVector type
- Add `separator_group` and `separators` to ChunkingSettings type
- Add SparseVectorIndexOptions type
- Add key to FiltersBucket type

### Other

* Add 3.14 to CI builds ([#3103](https://github.com/elastic/elasticsearch-py/pull/3103))
* Drop Python 3.9 support ([#3114](https://github.com/elastic/elasticsearch-py/pull/3114))

## 9.1.2 (2025-10-28)

### Enhancements

* Add `flush_after_seconds` option to `streaming_bulk()` ([#3064](https://github.com/elastic/elasticsearch-py/pull/3064))

### Bug Fixes

* DSL: support passing inner documents as `AttrDict` instances ([#3080](https://github.com/elastic/elasticsearch-py/pull/3080))
* DSL: add some recently added field classes as top-level exports for the package ([#3078](https://github.com/elastic/elasticsearch-py/pull/3078))

### API

- Add `streams` namespace with `streams.logs_disable`, `streams.logs_enable`, `streams.status` APIs
- Add `bytes` and `time` parameters to various APIs in the `cat` namespace.
- Add `index_template` parameter to `indices.simulate_index_template` API
- Add `input_type` parameter to `inference.text_embedding` API

### DSL

- New `CartesianBounds`, `CartesianCentroid`, `ChangePoint` aggregations
- Add `p_value` parameter to `SignificantTerms` aggregation
- Add `index_options` and `fields` parameters to `SemanticText` field
- Add `visit_percentage` parameter to `Knn` query
- Add `on_disk_rescore` field to `DenseVectorIndexOptions` type

### Other

* Add 3.14 to CI builds ([#3103](https://github.com/elastic/elasticsearch-py/pull/3103))

## 9.1.1 (2025-09-11)

### Enhancements

* ES|QL query builder integration with the DSL module ([#3058](https://github.com/elastic/elasticsearch-py/pull/3058))
* ES|QL query builder robustness fixes ([#3017](https://github.com/elastic/elasticsearch-py/pull/3017))
* Fix ES|QL `multi_match()` signature ([#3052](https://github.com/elastic/elasticsearch-py/pull/3052))

### API

* Add support for ES|QL query builder objects to ES|QL Query and Async Query APIs
* Add Transform Set Upgrade Mode API
* Fix type of `fields` parameter of Term Vectors API to array of strings
* Fix type of `params` parameter of SQL Query API to array

### DSL

* Preserve the `skip_empty` setting in `to_dict()` recursive serializations ([#3041](https://github.com/elastic/elasticsearch-py/pull/3041))
* Add `separator_group` and `separators` attributes to `ChunkingSettings` type
* Add `primary` attribute to `ShardFailure` type
* Fix type of `key` attribute of `ArrayPercentilesItem` to float


## 9.1.0 (2025-07-30)

### Enhancements

* ES|QL query builder (technical preview) ([#2997](https://github.com/elastic/elasticsearch-py/pull/2997))
* Update OpenTelemetry conventions ([#2999](https://github.com/elastic/elasticsearch-py/pull/2999))
* Add option to disable accurate reporting of file and line location in warnings (Fixes #3003) ([#3006](https://github.com/elastic/elasticsearch-py/pull/3006))

### APIs

* Remove `if_primary_term`, `if_seq_no` and `op_type` from Create API
* Remove `master_timeout` from Ingest Get Ip Location Database API
* Remove `application`, `priviledge` and `username` from the Security Get User API
* Rename `type_query_string` to `type` in License Post Start Trial API
* Add `require_data_stream` to Index API
* Add `settings_filter` to Cluster Get Component Template API
* Add `cause` to Cluster Put Component Template API
* Add `master_timeout` to Cluster State API
* Add `ccs_minimize_roundtrips` to EQL Search API
* Add `keep_alive` and `keep_on_completion` to ES|QL Async Query API
* Add `format` to ES|QL Async Query Get API
* Add ES|QL Get Query and List Queries APIs
* Add Indices Delete Data Stream Options API
* Add Indices Get Data Stream Options and Put Data Stream Options APIS
* Add Indices Get Data Stream Settings and Put Data Stream Settings APIs
* Add `allow_no_indices`, `expand_wildcards` and `ignore_available` to Indices Recovery API
* Add Indices Remove Block API
* Add Amazon Sagemaker to Inference API
* Add `input_type` to Inference API
* Add `timeout` to all Inference Put APIs
* Add Inference Put Custom API
* Add Inference Put DeepSeek API
* Add `task_settings` to Put HuggingFace API
* Add `refresh` to Security Grant API Key API
* Add `wait_for_completion` to the Snapshot Delete API
* Add `state` to Snapshot Get API
* Add `refresh` to Synonyms Put Synonym, Put Synonym Rule and Delete Synonym Rule APIs

### DSL

* Handle lists in `copy_to` option in DSL field declarations correctly (Fixes #2992) ([#2993](https://github.com/elastic/elasticsearch-py/pull/2993))
* Add `index_options` to SparseVector type
* Add SparseVectorIndexOptions type
* Add `key` to FiltersBucket type

Other changes

* Drop support for Python 3.8 ([#3001](https://github.com/elastic/elasticsearch-py/pull/3001))


## 9.0.4 (2025-09-11)

### Enhancements

* ES|QL query builder integration with the DSL module ([#3058](https://github.com/elastic/elasticsearch-py/pull/3058))
* ES|QL query builder robustness fixes ([#3017](https://github.com/elastic/elasticsearch-py/pull/3017))
* Fix ES|QL `multi_match()` signature ([#3052](https://github.com/elastic/elasticsearch-py/pull/3052))

### API

* Add support for ES|QL query builder objects to ES|QL Query and Async Query APIs
* Add Transform Set Upgrade Mode API
* Fix type of `fields` parameter of Term Vectors API to array of strings
* Fix type of `params` parameter of SQL Query API to array

### DSL

* Preserve the `skip_empty` setting in `to_dict()` recursive serializations ([#3041](https://github.com/elastic/elasticsearch-py/pull/3041))
* Add `primary` attribute to `ShardFailure` type
* Fix type of `key` attribute of `ArrayPercentilesItem` to float

## 9.0.3 (2025-07-30)

### Enhancements

* ES|QL query builder (technical preview) ([#2997](https://github.com/elastic/elasticsearch-py/pull/2997))
* Add option to disable accurate reporting of file and line location in warnings (Fixes #3003) ([#3006](https://github.com/elastic/elasticsearch-py/pull/3006))

### APIs

* Remove `if_primary_term`, `if_seq_no` and `op_type` from Create API
* Remove `stored_fields` from Get Source API
* Remove `master_timeout` from Ingest Get Ip Location Database API
* Remove `application`, `priviledge` and `username` from the Security Get User API
* Rename `type_query_string` to `type` in License Post Start Trial API
* Add `require_data_stream` to Index API
* Add `settings_filter` to Cluster Get Component Template API
* Add `cause` to Cluster Put Component Template API
* Add `ccs_minimize_roundtrips` to EQL Search API
* Add `keep_alive` and `keep_on_completion` to ES|QL Async Query API
* Add `format` to ES|QL Async Query Get API
* Add `allow_no_indices`, `expand_wildcards` and `ignore_available` to Indices Recovery API
* Add `timeout` to all Inference Put APIs
* Add `refresh` to Security Get User Profile API
* Add `wait_for_completion` to the Snapshot Delete API

### DSL

* Handle lists in `copy_to` field option correctly (Fixes #2992) ([#2993](https://github.com/elastic/elasticsearch-py/pull/2993))
* Add `key` to FiltersBucket type


## 9.0.2 (2025-06-05) [elasticsearch-python-client-902-release-notes]

### DSL

* Add `rescore_vector` to `DenseVectorIndexOptions`


## 9.0.1 (2025-04-28) [elasticsearch-python-client-901-release-notes]

### Features and enhancements [elasticsearch-python-client-901-features-enhancements]

* Surface caused_by in ApiError ([#2932](https://github.com/elastic/elasticsearch-py/pull/2932))
* Clarify Elasticsearch 9.x compatibility ([#2928](https://github.com/elastic/elasticsearch-py/pull/2928))
* Reorganize Sphinx docs to only include reference pages ([#2776](https://github.com/elastic/elasticsearch-py/pull/2776))


## 9.0.0 (2025-04-15) [elasticsearch-python-client-900-release-notes]

:::{tip}
Upgrade to Elasticsearch 9 before using elasticsearch-py 9.0.0 or later. Using elasticsearch-py 9.0.0 on an Elasticsearch 8 server will fail.
Since language clients are forward-compatible, you should first upgrade Elasticsearch, then the Elasticsearch client. See the [compatibility documentation](/reference/index.md#_compatibility) for more details.
:::

### Breaking changes

* Remove deprecated `Elasticsearch()` options ([#2840](https://github.com/elastic/elasticsearch-py/pull/2840))
* Remove deprecated `url_prefix` and `use_ssl` options ([#2797](https://github.com/elastic/elasticsearch-py/pull/2797))

See the [breaking changes page](breaking-changes.md) for more details.

### Enhancements

* Merge [`elasticsearch-dsl-py`](https://github.com/elastic/elasticsearch-dsl-py/) _ package ([#2736](https://github.com/elastic/elasticsearch-py/pull/2736))
* Add Python DSL documentation ([#2761](https://github.com/elastic/elasticsearch-py/pull/2761))
* Autogenerate DSL field classes from schema ([#2780](https://github.com/elastic/elasticsearch-py/pull/2780))
* Improve DSL documentation examples with class-based queries and type hints ([#2857](https://github.com/elastic/elasticsearch-py/pull/2857))
* Document the use of `param()` in Python DSL methods ([#2861](https://github.com/elastic/elasticsearch-py/pull/2861))
* Migrate documentation from AsciiDoc to Markdown format ([#2806](https://github.com/elastic/elasticsearch-py/pull/2806))
* Document use of sub-clients ([#2798](https://github.com/elastic/elasticsearch-py/pull/2798))
* Document how to make API calls ([#2843](https://github.com/elastic/elasticsearch-py/pull/2843))
* Fix `simulate` sub-client documentation ([#2749](https://github.com/elastic/elasticsearch-py/pull/2749))

### APIs

* Remove deprecated `/_knn_search` API
* Remove Unfreeze an index API
* Remove `min_compatible_shard_node` from Search and Async Search Submit APIs
* Remove local parameter from cat alias, Alias exists, and Get alias APIs
* Remove `verbose` from Index segments API
* Remove `include_model_definition` from Get trained model configuration info API
* Remove `wait_for_active_shards` from experimental Get field usage stats API
* Support soft-deletes in connectors:
  * Add `hard` to Delete connector API
  * Add `include_deleted` to Get and List Connector APIs
* Add `master_timeout` to Migrate to data tiers routing APIs
* Add `master_timeout` to the Alias exists and Get alias APIs.
* Add `expand_wildcards` to Create snapshot API
* Rename incorrect `access_token` to `token` in Logout of OpenID Connect API
* Add inference APIs: Alibaba Cloud AI Search, Amazon Bedrock, Anthropic, Azure AI Studio, Azure OpenAI, Cohere, Elastic Inference Service (EIS), Elasticsearch, ELSER, Google AI Studio, Google Vertex AI, Hugging Face, Jina AI, Mistral, OpenAI, and Voyage AI
* Add Elastic Inference Service (EIS) chat completion API
* Add Reindex legacy backing indices APIs
* Add Create an index from a source index API
* Add `include_source_on_error` to Create, Index, Update and Bulk APIs
* Add Stop async ES|QL query API
* Add `timeout` to Resolve Cluster API
* Add `adaptive_allocations` body field to Start and Update a trained model deployment API
* Rename `index_template_subtitutions` to `index_template_substitutions` in Simulate data ingestion API
* Add `if_primary_term`, `if_seq_no`, `op_type`, `require_alias` and `require_data_stream` to Create API
* Add `max_concurrent_shard_requests` to Open point in time API
* Add `local` and `flat_settings` to Check index templates API
* Add `reopen` to Update index settings API
* Add `resource` to Reload search analyzer API
* Add `lazy` to Roll over to a new index API
* Add `cause` and `create` to Simulate index template APIs
* Add inference APIs: Alibaba Cloud AI Search, Amazon Bedrock, Anthropic, Azure AI Studio, Azure OpenAI, Cohere, Elasticsearch, ELSER, Google AI Studio, Google Vertex AI, Hugging Face, Jina AI, Mistral, OpenAI, and Voyage AI

### DSL
 * Add `ignore_malformed`, `script`,  `on_script_error` and `time_series_dimension` to Boolean field
 * Add `index` to GeoShape field
 * Add `search_inference_id` to SemanticText field

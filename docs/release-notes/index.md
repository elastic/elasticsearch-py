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
## 9.0.4 (2025-09-11)

* ES|QL query builder integration with the DSL module ([#3058](https://github.com/elastic/elasticsearch-py/pull/3058))
* ES|QL query builder robustness fixes ([#3017](https://github.com/elastic/elasticsearch-py/pull/3017))
* Fix ES|QL `multi_match()` signature ([#3052](https://github.com/elastic/elasticsearch-py/pull/3052))

API
* Add support for ES|QL query builder objects to ES|QL Query and Async Query APIs
* Add Transform Set Upgrade Mode API
* Fix type of `fields` parameter of Term Vectors API to array of strings
* Fix type of `params` parameter of SQL Query API to array

DSL
* Preserve the `skip_empty` setting in `to_dict()` recursive serializations ([#3041](https://github.com/elastic/elasticsearch-py/pull/3041))
* Add `primary` attribute to `ShardFailure` type
* Fix type of `key` attribute of `ArrayPercentilesItem` to float
                  

## 9.0.3 (2025-07-30)

Enhancements

* ES|QL query builder (technical preview) ([#2997](https://github.com/elastic/elasticsearch-py/pull/2997))
* Add option to disable accurate reporting of file and line location in warnings (Fixes #3003) ([#3006](https://github.com/elastic/elasticsearch-py/pull/3006))

APIs

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

DSL

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

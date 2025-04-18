---
navigation_title: "Elasticsearch Python Client"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/release-notes.html
---

# Elasticsearch Python Client release notes [elasticsearch-python-client-release-notes]

Review the changes, fixes, and more in each version of Elasticsearch Python Client.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.

% ## version.next [felasticsearch-python-client-next-release-notes]

% ### Features and enhancements [elasticsearch-python-client-next-features-enhancements]
% *

% ### Fixes [elasticsearch-python-client-next-fixes]

## 9.0.0 (2025-04-15) [elasticsearch-python-client-900-release-notes]

:::{tip}
Upgrade to Elasticsearch 9 before using elasticsearch-py 9.0.0 or later. Using elasticsearch-py 9.0.0 on an Elasticsearch 8 server will fail.
Since language clients are forward-compatible, you should first upgrade Elasticsearch, then the Elasticsearch client. See the [compatibility documentation](https://www.elastic.co/docs/reference/elasticsearch/clients/python#_compatibility) for more details.
:::

### Breaking changes

* Remove deprecated `Elasticsearch()` options ([#2840](https://github.com/elastic/elasticsearch-py/pull/2840))
* Remove deprecated `url_prefix` and `use_ssl` options ([#2797](https://github.com/elastic/elasticsearch-py/pull/2797))

See the breaking changes page for more details.

### Enhancements

* Merge `Elasticsearch-DSL <https://github.com/elastic/elasticsearch-dsl-py/>`_ package ([#2736](https://github.com/elastic/elasticsearch-py/pull/2736))
* Add Python DSL documentation ([#2761](https://github.com/elastic/elasticsearch-py/pull/2761))
* Autogenerate DSL field classes from schema ([#2780](https://github.com/elastic/elasticsearch-py/pull/2780))
* Improve DSL documentation examples with class-based queries and type hints ([#2857](https://github.com/elastic/elasticsearch-py/pull/2857))
* Document the use of `param()` in Python DSL methods ([#2861](https://github.com/elastic/elasticsearch-py/pull/2861))
* Migrate documentation from AsciiDoc to Markdown format ([#2806](https://github.com/elastic/elasticsearch-py/pull/2806))
* Document use of sub-clients ([#2798](https://github.com/elastic/elasticsearch-py/pull/2798))
* Document how to making API calls ([#2843](https://github.com/elastic/elasticsearch-py/pull/2843))
* Fix `simulate` sub-client documentation ([#2749](https://github.com/elastic/elasticsearch-py/pull/2749))

### APIs

* Remove deprecated `/_knn_search` API
* Remove Unfreeze an index API
* Remove min_compatible_shard_node from Search and Async Search Submit APIs
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
* Add inference APIs: Alibaba Cloud AI Search, Amazon Bedrock, Anthropic, Azure AI Studio,Azure OpenAI, Cohere, Elastic Inference Service (EIS), Elasticsearch, ELSER, Google AIStudio, Google Vertex AI, Hugging Face, Jina AI, Mistral, OpenAI, and Voyage AI
* Add Elastic Inference Service (EIS) chat completion API
* Add Reindex legacy backing indices APIs
* Add Create an index from a source index API
* Add `include_source_on_error` to Create, Index, Update and Bulk APIs
* Add Stop async ES|QL query API
* Add `timeout` to Resolve Cluster API
* Add `adaptive_allocations` body field to Start and Update a trained model deployment API
* Rename `index_template_subtitutions` to `index_template_substitutions` in Simulate dataingestion API* Add `if_primary_term`, `if_seq_no`, `op_type`, `require_alias` and `require_data_stream` to Create API
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

### Features and enhancements [elasticsearch-python-client-900-features-enhancements]

### Fixes [elasticsearch-python-client-900-fixes]

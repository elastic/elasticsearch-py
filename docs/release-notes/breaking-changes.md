---
navigation_title: "Breaking changes"
---

# Elasticsearch Python Client breaking changes [elasticsearch-python-client-breaking-changes]
Breaking changes can impact your Elastic applications, potentially disrupting normal operations. Before you upgrade, carefully review the Elasticsearch Python Client breaking changes and take the necessary steps to mitigate any issues. To learn how to upgrade, check [Upgrade](docs-content://deploy-manage/upgrade.md).

% ## Next version [elasticsearch-python-client-nextversion-breaking-changes]

% ::::{dropdown} Title of breaking change 
% Description of the breaking change.
% For more information, check [PR #](PR link).
% **Impact**<br> Impact of the breaking change.
% **Action**<br> Steps for mitigating deprecation impact.
% ::::

## 9.2.0 [elasticsearch-python-client-920-breaking-changes]

::::{dropdown} DSL module is incompatible with Elasticsearch 9.0
Due to a change in [how Elasticsearch 9.2 returns vectors](https://www.elastic.co/search-labs/blog/elasticsearch-exclude-vectors-from-source), the DSL module in the Elasticsearch Python client 9.2.0 includes the `exclude_vectors` option in all search requests executed from a `Document` or `AsyncDocument` class. Because the `exclude_vectors` option does not exist in Elasticsearch 9.0, document queries issued with 9.2.0 or newer versions of the Elasticsearch Python client require a 9.1.0 or newer Elasticsearch server.
::::

## 9.0.0 [elasticsearch-python-client-900-breaking-changes]

::::{dropdown} Remove deprecated Elasticsearch() options
The `timeout`, `randomize_hosts`, `host_info_callback`, `sniffer_timeout`, `sniff_on_connection_fail` and `maxsize` parameters were deprecated in elasticsearch-py 8.0 and are now removed from `Elasticsearch.__init__()`.
For more information, check [PR #2840](https://github.com/elastic/elasticsearch-py/pull/2840).

**Impact**<br> These parameters were removed in favor of more descriptive versions. Using any of these parameters will prevent instantiating the Elasticsearch client.

**Action**<br> These parameters can be replaced as follows:
 * `timeout` is now `request_timeout`
 * `randomize_hosts` is now `randomize_nodes_in_pool`
 * `host_info_callback` is now `sniffed_node_callback`
 * `sniffer_timeout` is now `min_delay_between_sniffing`
 * `sniff_on_connection_fail` is now `sniff_on_node_failure`
 * `maxsize` is now `connections_per_node`
::::

::::{dropdown} Remove deprecated url_prefix and use_ssl host keys
When instantiating a new client, `hosts` can be specified as a dictionary. The `url_prefix` and `use_ssl` keys are no longer allowed.
For more information, check [PR #2797](https://github.com/elastic/elasticsearch-py/pull/2797).

**Impact**<br>
Using any of these parameters will prevent instantiating the Elasticsearch client.

**Action**<br>
The parameters can be replaced as follows:
 * `use_ssl` isn't needed, as a scheme is required since elasticsearch-py 8.0 (`http` or `https`)
 * `url_prefix` should be replaced with `path_prefix`, which is more descriptive. This functionality allows you to deploy Elasticsearch under a specific path, such as `http://host:port/path/to/elasticsearch`, instead of the default root path (`http://host:port/`)
::::

::::{dropdown} Remove APIs
Elasticsearch 9 removed the kNN search and Unfreeze index APIs.

**Action**<br>
 * The kNN search API has been replaced by the `knn` option in the search API since Elasticsearch 8.4.
 * The Unfreeze index API was deprecated in Elasticsearch 7.14 and has been removed in Elasticsearch 9.
 ::::

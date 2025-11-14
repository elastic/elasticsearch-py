---
navigation_title: "Python"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
applies_to:
  stack: ga
  serverless: ga
---

# {{es}} Python client [overview]

This documentation covers the [official Python client for {{es}}](https://github.com/elastic/elasticsearch-py). The goal of the Python client is to provide common ground for all {{es}}-related code in Python. The client is designed to be unopinionated and extendable. 

API reference documentation is provided on [Read the Docs](https://elasticsearch-py.readthedocs.io).

The following example shows a simple Python client use case:

```python
>>> from datetime import datetime
>>> from elasticsearch import Elasticsearch

# Connect to 'http://localhost:9200'
>>> client = Elasticsearch("http://localhost:9200")

# Datetimes will be serialized:
>>> client.index(index="my-index-000001", id=42, document={"any": "data", "timestamp": datetime.now()})
{'_id': '42', '_index': 'my-index-000001', '_type': 'test-type', '_version': 1, 'ok': True}

# ...but not deserialized
>>> client.get(index="my-index-000001", id=42)['_source']
{'any': 'data', 'timestamp': '2013-05-12T19:45:31.804229'}
```

## Features [_features]

The client's features include:

* Translating basic Python data types to and from JSON
* Configurable automatic discovery of cluster nodes
* Persistent connections
* Load balancing (with pluggable selection strategy) across all available nodes
* Node timeouts on transient errors
* Thread safety
* Pluggable architecture

The client also provides a convenient set of [helpers](client-helpers.md) for tasks like bulk indexing and reindexing.

::::{tip}
To get started, try this walkthrough: [Ingest data with Python](docs-content://manage-data/ingest/ingesting-data-from-applications/ingest-data-with-python-on-elasticsearch-service.md)
::::

### {{es}} Python DSL [_elasticsearch_python_dsl]

The [Python DSL module](../reference/elasticsearch-dsl.md) offers a convenient and idiomatic way to write and manipulate queries. 

## Version compatibility [_compatibility]

Language clients are **forward compatible**: each client version works with equivalent and later minor versions of the **same or next major** version of {{es}}. For full compatibility, the client and {{es}} minor versions should match.

| Client version | {{es}} `8.x` | {{es}} `9.x` | {{es}} `10.x` |
|----------------|---------------------------------|---------------------------------|----------------------------------|
| 9.x client | &#10060; Not compatible with {{es}} 8.x | &#9989; Compatible with {{es}} 9.x | &#9989; Compatible with {{es}} 10.x |
| 8.x client | &#9989; Compatible with {{es}} 8.x | &#9989; Compatible with {{es}} 9.x | &#10060; Not compatible with {{es}} 10.x |

Compatibility does not imply feature parity. New {{es}} features are supported only in equivalent client versions. For example, an 8.12 client fully supports {{es}} 8.12 features and works with 8.13 without breaking, but it does not support new {{es}} 8.13 features. An 8.13 client fully supports {{es}} 8.13 features.

{{es}} language clients are also **backward compatible** across minor versions, with default distributions and without guarantees.

## Upgrade to a new major version

:::{important}
To upgrade to a new major version, first [upgrade {{es}}](docs-content://deploy-manage/upgrade.md), then upgrade the Python client.
:::

As of version 8.0, {{es}} offers a [REST API compatibility mode](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) for smoother upgrades. In compatibility mode, you can upgrade your {{es}} cluster to the next major version while continuing to use your existing client during the transition.

### How compatibility mode works

In the Python client, compatibility mode is **always enabled**. You don't need to configure it manually or set an environment variable. The client automatically sends compatibility headers with API requests so that it can communicate with the next major version of {{es}}.

In compatibility mode, your Python client applications can continue running during an upgrade without restart or redeployment. For example, during a rolling upgrade of your {{es}} cluster from 8.x to 9.x, your 8.x Python client continues working throughout the process without any changes or intervention.

**What to expect in compatibility mode:**

If you're using the Python client in compatibility mode to work with the next major version of {{es}}:

* API calls affected by [breaking changes](../release-notes/breaking-changes.md) might fail or behave differently. 
* API calls unaffected by breaking changes continue to work as expected.
* New features from the next major version of {{es}} are not available until you upgrade the client itself.

Although compatibility mode allows your Python client to keep working without intervention, you should upgrade the client when feasible. Even if you don't need the newest {{es}} features, upgrading the client ensures you receive the latest bug fixes and improvements.

:::{tip}
To support working with multiple client versions, the Python client is also released under the package names `elasticsearch8` and `elasticsearch9` (to prevent name collisions).
:::

For guidance on upgrading your {{es}} deployment, refer to the [{{es}} upgrade documentation](docs-content://deploy-manage/upgrade.md) and [upgrade paths](docs-content://deploy-manage/upgrade.md#upgrade-paths).
---
navigation_title: "Python"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
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

### Elasticsearch Python DSL [_elasticsearch_python_dsl]

The [Python DSL module](../reference/elasticsearch-dsl.md) offers a convenient and idiomatic way to write and manipulate queries. 

## {{es}} version compatibility [_compatibility]

Language clients are **forward compatible**: each client version works with equivalent and later minor versions of the **same or next major** version of {{es}}. For full compatibility, the client and {{es}} minor versions should match.

| Client version | {{es}} `8.x` | {{es}} `9.x` | {{es}} `10.x` |
|----------------|---------------------------------|---------------------------------|----------------------------------|
| 9.x client| &#10060; Not compatible with {{es}} 8.x | &#9989; Compatible with {{es}} 9.x | &#9989; Compatible with {{es}} 10.x |
| 8.x client | &#9989; Compatible with {{es}} 8.x | &#9989; Compatible with {{es}} 9.x | &#10060; Not compatible with {{es}} 10.x |

Compatibility does not imply feature parity. New {{es}} features are supported only in equivalent client versions. For example, an 8.12 client fully supports {{es}} 8.12 features and works with 8.13 without breaking, but it does not support new {{es}} 8.13 features. An 8.13 client fully supports {{es}} 8.13 features.

{{es}} language clients are also **backward compatible** across minor versions &mdash; with default distributions and without guarantees. 

### Major version upgrades

:::{important}
To upgrade to a new major version, first [upgrade {{es}}](docs-content://deploy-manage/upgrade.md), then upgrade the Python client.
:::

As of version 8.0, {{es}} offers a compatibility mode for smoother upgrades. In compatibility mode, you can upgrade your {{es}} cluster to the next major version while continuing to use your existing client during the transition. 

For example, if you're upgrading {{es}} 8.x to {{es}} 9.x, you can continue to use the 8.x Python {{es}} client during and after the server upgrade, with the exception of [breaking changes](../release-notes/breaking-changes.md).

To enable compatibility mode, set the environment variable `ELASTIC_CLIENT_APIVERSIONING` to `true`. For more details, refer to [{{es}} API compatibility](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md).

:::{tip}
To support working with multiple client versions, the Python client is also released under the package names `elasticsearch8` and `elasticsearch9` (to prevent name collisions).
:::
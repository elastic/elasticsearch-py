---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
---

# Python [overview]

This documentation covers the [official Python client for {{es}](https://github.com/elastic/elasticsearch-py/tree/main/elasticsearch/dsl)}. The goal of the Python client is to provide common ground for all {{es}}-related code in Python. The client is designed to be unopinionated and extendable. 

API reference documentation is provided on [Read the Docs](https://elasticsearch-py.readthedocs.io).


## Example use [_example_use]

Here's a simple Python client use case:

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
For details on ingesting data into Elastic Cloud with Python, refer to [Ingest data with Python](docs-content://manage-data/ingest/ingesting-data-from-applications/ingest-data-with-python-on-elasticsearch-service.md).
::::

### Elasticsearch Python DSL [_elasticsearch_python_dsl]

The [Python DSL module](../reference/elasticsearch-dsl.md) offers a convenient and idiomatic way to write and manipulate queries. 


## Compatibility [_compatibility]

Language clients are _forward compatible:_ each client version works with equivalent and later minor versions of {{es}} without breaking. 

Compatibility does not imply full feature parity. New {{es}} features are supported only in equivalent client versions. For example, an 8.12 client fully supports {{es}} 8.12 features and works with 8.13 without breaking; however, it does not support new {{es}} 8.13 features. An 8.13 client fully supports {{es}} 8.13 features.

| Elasticsearch version | elasticsearch-py branch |
| --- | --- |
| main | main |
| 9.x | 9.x |
| 9.x | 8.x |
| 8.x | 8.x |

{{es}} language clients are also _backward compatible_ across minor versions &mdash; with default distributions and without guarantees. 

### Major version upgrades

:::{important}
To upgrade to a new major version, first upgrade {{es}}, then upgrade the Python client.
:::

As of version 8.0, {{es}} offers a compatibility mode for smoother upgrades. In compatibility mode, you can upgrade your {{es}} cluster to the next major version while continuing to use your existing client during the transition.

For example, if you're upgrading {{es}} 8.x to {{es}} 9.x, you can continue to use the 8.x Python {{es}} client during the server migration, with the except of client [breaking changes](../release-notes/breaking-changes.md).

For details, refer to [REST API compatibility workflow](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md#_rest_api_compatibility_workflow).

:::{tip}
To support working with multiple client versions, the Python client is also released under the package names `elasticsearch8` and `elasticsearch9` (to prevent name collisions).
:::

## Additional resources
- [Upgrade your deployment or cluster](docs-content://deploy-manage/upgrade.md)
- [Python client GitHub repo](https://github.com/elastic/elasticsearch-py)
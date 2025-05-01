---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
---

# Python [overview]

This is the official Python client for {{es}}. Its goal is to provide common ground for all {{es}}-related code in Python. For this reason, the client is designed to be unopinionated and extendable. API reference documentation for this client is available on [Read the Docs](https://elasticsearch-py.readthedocs.io).


## Example use [_example_use]

Simple use-case:

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

::::{tip}
For an elaborate example of how to ingest data into Elastic Cloud, refer to [this page](docs-content://manage-data/ingest/ingesting-data-from-applications/ingest-data-with-python-on-elasticsearch-service.md).
::::


## Features [_features]

The client’s features include:

* Translating basic Python data types to and from JSON
* Configurable automatic discovery of cluster nodes
* Persistent connections
* Load balancing (with pluggable selection strategy) across all available nodes
* Node timeouts on transient errors
* Thread safety
* Pluggable architecture

The client also contains a convenient set of [helpers](https://elasticsearch-py.readthedocs.org/en/master/helpers.md) for some of the more engaging tasks like bulk indexing and reindexing.


## Elasticsearch Python DSL [_elasticsearch_python_dsl]

For a higher level access with more limited scope, have a look at the DSL module, which provides a more convenient and idiomatic way to write and manipulate queries.


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

:::{tip}
To upgrade to a new major version, first upgrade {{es}}, then upgrade the Python {{es}} client.
:::

If you need to work with multiple client versions, note that older versions are also released as `elasticsearch7` and `elasticsearch8`.

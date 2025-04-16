---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
---

# Python [overview]

This is the official low-level Python client for {{es}}. Its goal is to provide common ground for all {{es}}-related code in Python. For this reason, the client is designed to be unopinionated and extendable. An API reference is available on [Read the Docs](https://elasticsearch-py.readthedocs.io).


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

Language clients are forward compatible; meaning that the clients support communicating with greater or equal minor versions of {{es}} without breaking. It does not mean that the clients automatically support new features of newer {{es}} versions; it is only possible after a release of a new client version. For example, a 8.12 client version won’t automatically support the new features of the 8.13 version of {{es}}, the 8.13 client version is required for that. {{es}} language clients are only backwards compatible with default distributions and without guarantees made.

| Elasticsearch version | elasticsearch-py branch | Supported |
| --- | --- | --- |
| main | main |  |
| 9.x | 9.x | 9.x |
| 8.x | 8.x | 8.x |
| 7.x | 7.x | 7.17 |

If you have a need to have multiple versions installed at the same time older versions are also released as `elasticsearch7` and `elasticsearch8`.

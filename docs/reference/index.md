---
navigation_title: "Python"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/overview.html
---

# {{es}} Python client [overview]

This documentation covers the [official Python client for {{es}}](https://github.com/elastic/elasticsearch-py). The Python client provides a comprehensive foundation for working with {{es}} in Python. The client is designed to be unopinionated and extensible. 

## Example [_example]

Here's an example of basic Python client usage:

::::{tab-set}

:::{tab-item} Standard Python
```python
import os
from elasticsearch import Elasticsearch

def main():
    client = Elasticsearch(
        hosts=[os.getenv("ELASTICSEARCH_URL")],
        api_key=os.getenv("ELASTIC_API_KEY"),
    )

    resp = client.search(
        index="my-index-000001",
        from_=40,
        size=20,
        query={
            "term": {
                "user.id": "kimchy"
            }
        },
    )
    print(resp)
```
:::

:::{tab-item} Async Python
```python
import os
from elasticsearch import AsyncElasticsearch

async def main():
    client = AsyncElasticsearch(
        hosts=[os.getenv("ELASTICSEARCH_URL")],
        api_key=os.getenv("ELASTIC_API_KEY"),
    )

    resp = await client.search(
        index="my-index-000001",
        from_=40,
        size=20,
        query={
            "term": {
                "user.id": "kimchy"
            }
        },
    )
    print(resp)
```
:::

::::

## Overview [_overview]

The {{es}} Python client package consists of several modules: the core client, a set of bulk helper functions, an ES|QL query builder, and a DSL module.

### The core client

This module, also known as the low-level client, enables sending requests to {{es}} servers. The client provides access to the entire surface of the {{es}} API.

* [](getting-started.md)
* [Walkthrough: Ingest data with Python](docs-content://manage-data/ingest/ingesting-data-from-applications/ingest-data-with-python-on-elasticsearch-service.md)
* [Reference documentation](https://elasticsearch-py.readthedocs.io/en/stable/es_api.html)

#### Features [_features]

The core client's features include:

* Translating basic Python data types to and from JSON
* Configurable automatic discovery of cluster nodes
* Persistent connections
* Load balancing (with pluggable selection strategy) across all available nodes
* Node timeouts on transient errors
* Thread safety
* Pluggable architecture

### Bulk helpers

The bulk helpers simplify ingesting large amounts of data, by providing a high-level interface based on Python iterables.

* [](client-helpers.md#bulk-helpers)
* [Reference documentation](https://elasticsearch-py.readthedocs.io/en/stable/api_helpers.html)

### ES|QL query builder

The ES|QL query builder offers an idiomatic interface for constructing ES|QL queries using Python expressions.

* [](esql-query-builder.md)
* [Reference documentation](https://elasticsearch-py.readthedocs.io/en/stable/esql.html)

### DSL module

The DSL module can be thought of as a high-level client for {{es}}. It allows applications to manipulate documents and queries using Python classes and objects, instead of primitive types such as dictionaries and lists.

* [](elasticsearch-dsl.md)
* [Reference documentation](https://elasticsearch-py.readthedocs.io/en/stable/dsl.html)

## Compatibility [_compatibility]

| Client version | {{es}} `8.x` | {{es}} `9.x` | {{es}} `10.x` |
|----------------|---------------------------------|---------------------------------|----------------------------------|
| 9.x client | &#10060; Not compatible with {{es}} 8.x | &#9989; Compatible with {{es}} 9.x | &#9989; Compatible with {{es}} 10.x |
| 8.x client | &#9989; Compatible with {{es}} 8.x | &#9989; Compatible with {{es}} 9.x | &#10060; Not compatible with {{es}} 10.x |

Compatibility does not imply feature parity. New {{es}} features are supported only in equivalent client versions. For example, an 8.12 client fully supports {{es}} 8.12 features and works with 8.13 without breaking, but it does not support new {{es}} 8.13 features. An 8.13 client fully supports {{es}} 8.13 features.

{{es}} language clients are also **backward compatible** across minor versions, with default distributions and without guarantees. 

### Major version upgrades

:::{important}
To upgrade to a new major version, first [upgrade {{es}}](docs-content://deploy-manage/upgrade.md), then upgrade the Python client.
:::

As of version 8.0, {{es}} offers a [compatibility mode](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) for smoother upgrades. In compatibility mode, you can upgrade your {{es}} cluster to the next major version while continuing to use your existing client during the transition. 

For example, if you're upgrading {{es}} from 8.x to 9.x, you can continue to use the 8.x Python client during and after the {{es}} server upgrade, with the exception of [breaking changes](../release-notes/breaking-changes.md).

In the Python client, compatibility mode is always enabled. 

:::{tip}
To support working with multiple client versions, the Python client is also released under the package names `elasticsearch8` and `elasticsearch9` (to prevent name collisions).
:::

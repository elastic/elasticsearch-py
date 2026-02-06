---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/elasticsearch-dsl.html
---

# Elasticsearch Python DSL [elasticsearch-dsl]

Elasticsearch DSL is a module of the official Python client that aims to help with writing and running queries against Elasticsearch in a more convenient and idiomatic way. It stays close to the Elasticsearch JSON DSL, mirroring its terminology and structure. It exposes the whole range of the DSL from Python either directly using defined classes or a queryset-like expressions. Here is an example:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
from elasticsearch.dsl import Search
from elasticsearch.dsl.query import Match, Term

s = Search(index="my-index") \
    .query(Match("title", "python")) \
    .filter(Term("category", "search")) \
    .exclude(Match("description", "beta"))
for hit in s:
    print(hit.title)
```
:::

:::{tab-item} Async Python
:sync: async
```python
from elasticsearch.dsl import AsyncSearch
from elasticsearch.dsl.query import Match, Term

async def run_query():
    s = AsyncSearch(index="my-index") \
        .query(Match("title", "python")) \
        .filter(Term("category", "search")) \
        .exclude(Match("description", "beta"))
    async for hit in s:
        print(hit.title)
```
:::

::::

It also provides an optional wrapper for working with documents as Python objects: defining mappings, retrieving and saving documents, wrapping the document data in user-defined classes.

To use the other Elasticsearch APIs (eg. cluster health) just use the regular client.






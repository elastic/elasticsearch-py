---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/client-helpers.html
---

# Client helpers [client-helpers]

You can find here a collection of simple helper functions that abstract some specifics of the raw API.


## Bulk helpers [bulk-helpers]

There are several helpers for the bulk API since its requirement for specific formatting and other considerations can make it cumbersome if used directly.

All bulk helpers accept an instance of `Elasticsearch` class and an iterable `action` (any iterable, can also be a generator, which is ideal in most cases since it allows you to index large datasets without the need of loading them into memory). For asynchronous Python, use the bulk helpers with the `async_` prefix and pass an `AsyncElasticsearch` instance as first argument.

The items in the iterable `action` should be the documents we wish to index in several formats. The most common one is the same as returned by `search()`, for example:

```yaml
{
  '_index': 'index-name',
  '_id': 42,
  '_routing': 5,
  'pipeline': 'my-ingest-pipeline',
  '_source': {
    "title": "Hello World!",
    "body": "..."
  }
}
```

Alternatively, if `_source` is not present, it pops all metadata fields from the doc and use the rest as the document data:

```yaml
{
  "_id": 42,
  "_routing": 5,
  "title": "Hello World!",
  "body": "..."
}
```

The `bulk()` api accepts `index`, `create`, `delete`, and `update` actions. Use the `_op_type` field to specify an action (`_op_type` defaults to `index`):

```yaml
{
  '_op_type': 'delete',
  '_index': 'index-name',
  '_id': 42,
}
{
  '_op_type': 'update',
  '_index': 'index-name',
  '_id': 42,
  'doc': {'question': 'The life, universe and everything.'}
}
```


## Scan [scan]

Simple abstraction on top of the `scroll()` API - a simple iterator that yields all hits as returned by underlining scroll requests.

By default scan does not return results in any pre-determined order. To have a standard order in the returned documents (either by score or explicit sort definition) when scrolling, use `preserve_order=True`. This may be an expensive operation and will negate the performance benefits of using `scan`.

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```py
scan(es,
    query={"query": {"match": {"title": "python"}}},
    index="orders-*"
)
```
:::

:::{tab-item} Async Python
:sync: async
```py
await scan(es,
    query={"query": {"match": {"title": "python"}}},
    index="orders-*"
)
```
:::

::::

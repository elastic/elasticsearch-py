---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/async.html
---

# Using with asyncio [async]

The `elasticsearch` package supports async/await with [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://docs.aiohttp.org). You can either install `aiohttp` directly or use the `[async]` extra:

```bash
$ python -m pip install elasticsearch aiohttp

# - OR -

$ python -m pip install elasticsearch[async]
```


## Getting Started with Async [_getting_started_with_async]

After installation all async API endpoints are available via `~elasticsearch.AsyncElasticsearch` and are used in the same way as other APIs, with an extra `await`:

```python
import asyncio
from elasticsearch import AsyncElasticsearch

client = AsyncElasticsearch()

async def main():
    resp = await client.search(
        index="documents",
        body={"query": {"match_all": {}}},
        size=20,
    )
    print(resp)

asyncio.run(main())
```

All APIs that are available under the sync client are also available under the async client.

[Reference documentation](https://elasticsearch-py.readthedocs.io/en/latest/async.html#api-reference)


## ASGI Applications and Elastic APM [_asgi_applications_and_elastic_apm]

[ASGI](https://asgi.readthedocs.io) (Asynchronous Server Gateway Interface) is a way to serve Python web applications making use of async I/O to achieve better performance. Some examples of ASGI frameworks include FastAPI, Django 3.0+, and Starlette. If you’re using one of these frameworks along with Elasticsearch then you should be using `~elasticsearch.AsyncElasticsearch` to avoid blocking the event loop with synchronous network calls for optimal performance.

[Elastic APM](apm-agent-python://reference/index.md) also supports tracing of async Elasticsearch queries like synchronous queries. For an example on how to configure `AsyncElasticsearch` with a popular ASGI framework [FastAPI](https://fastapi.tiangolo.com/) and APM tracing there is a [pre-built example](https://github.com/elastic/elasticsearch-py/tree/master/examples/fastapi-apm) in the `examples/fastapi-apm` directory.

See also the [Using OpenTelemetry](/reference/opentelemetry.md) page.

## Trio support

If you prefer using Trio instead of asyncio to take advantage of its better structured concurrency support, you can use the HTTPX async node which supports Trio out of the box.

```python
import trio
from elasticsearch import AsyncElasticsearch

client = AsyncElasticsearch(
    "https://...",
    api_key="...",
    node_class="httpxasync")

async def main():
    resp = await client.info()
    print(resp.body)

trio.run(main)
```

The one limitation of Trio support is that it does not currently support node sniffing, which was not implemented with structured concurrency in mind.

## Frequently Asked Questions [_frequently_asked_questions]


### ValueError when initializing `AsyncElasticsearch`? [_valueerror_when_initializing_asyncelasticsearch]

If when trying to use `AsyncElasticsearch` you receive `ValueError: You must have 'aiohttp' installed to use AiohttpHttpNode` you should ensure that you have `aiohttp` installed in your environment (check with `$ python -m pip freeze | grep aiohttp`). Otherwise, async support won’t be available.


### What about the `elasticsearch-async` package? [_what_about_the_elasticsearch_async_package]

Previously asyncio was supported separately with the [elasticsearch-async](https://github.com/elastic/elasticsearch-py-async) package. The `elasticsearch-async` package has been deprecated in favor of `AsyncElasticsearch` provided by the `elasticsearch` package in v7.8 and onwards.


### Receiving *Unclosed client session / connector* warning? [_receiving_unclosed_client_session_connector_warning]

This warning is created by `aiohttp` when an open HTTP connection is garbage collected. You’ll typically run into this when closing your application. To resolve the issue ensure that `~elasticsearch.AsyncElasticsearch.close` is called before the `~elasticsearch.AsyncElasticsearch` instance is garbage collected.

For example if using FastAPI that might look like this:

```python
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch

ELASTICSEARCH_URL = os.environ["ELASTICSEARCH_URL"]
client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = AsyncElasticsearch(ELASTICSEARCH_URL)
    yield
    await client.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def main():
    return await client.info()
```

You can run this example by saving it to `main.py` and executing `ELASTICSEARCH_URL=http://localhost:9200 uvicorn main:app`.


## Async Helpers [_async_helpers]

Async variants of all helpers are available in `elasticsearch.helpers` and are all prefixed with `async_*`. You’ll notice that these APIs are identical to the ones in the sync [*Client helpers*](/reference/client-helpers.md) documentation.

All async helpers that accept an iterator or generator also accept async iterators and async generators.

[Reference documentation](https://elasticsearch-py.readthedocs.io/en/latest/async.html#api-reference)


Using Asyncio with Elasticsearch
================================

 .. py:module:: elasticsearch

Starting in ``elasticsearch-py`` v7.8.0 for Python 3.6+ the ``elasticsearch`` package supports async/await with
`Asyncio <https://docs.python.org/3/library/asyncio.html>`_. Install the package with the ``async``
extra to install the `aiohttp <https://docs.aiohttp.org>`_ HTTP client and other dependencies
required for async support:

 .. code-block:: bash

    $ python -m pip install elasticsearch[async]>=7.8.0

The same version specifiers for following the Elastic Stack apply to
the ``async`` extra:

 .. code-block:: bash

    # Elasticsearch 7.x
    $ python -m pip install elasticsearch[async]>=7,<8

 .. note::
    Async functionality is a new feature of this library in v7.8.0 so
    `please open an issue <https://github.com/elastic/elasticsearch-py/issues>`_
    if you find an issue or have a question about async support.

Getting Started with Async
--------------------------

After installation all async API endpoints are available via :class:`~elasticsearch.AsyncElasticsearch`
and are used in the same way as other APIs, just with an extra ``await``:

 .. code-block:: python

    import asyncio
    from elasticsearch import AsyncElasticsearch

    es = AsyncElasticsearch()

    async def main():
        resp = await es.search(
            index="documents",
            body={"query": {"match_all": {}}}
            size=20,
        )
        print(resp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

All APIs that are available under the sync client are also available under the async client.

Async Helpers
-------------

Async variants of all helpers are available in ``elasticsearch.helpers``
and are all prefixed with ``async_*``. You'll notice that these APIs
are identical to the ones in the sync :ref:`helpers` documentation.

All async helpers that accept an iterator or generator also accept async iterators
and async generators.

 .. py:module:: elasticsearch.helpers

Bulk and Streaming Bulk
~~~~~~~~~~~~~~~~~~~~~~~

 .. autofunction:: async_bulk

 .. code-block:: python

    import asyncio
    from elasticsearch import AsyncElasticsearch
    from elasticsearch.helpers import async_bulk

    es = AsyncElasticsearch()

    async def gendata():
        mywords = ['foo', 'bar', 'baz']
        for word in mywords:
            yield {
                "_index": "mywords",
                "doc": {"word": word},
            }

    async def main():
        await async_bulk(es, gendata())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

 .. autofunction:: async_streaming_bulk

 .. code-block:: python

    import asyncio
    from elasticsearch import AsyncElasticsearch
    from elasticsearch.helpers import async_bulk

    es = AsyncElasticsearch()

    async def gendata():
        mywords = ['foo', 'bar', 'baz']
        for word in mywords:
            yield {
                "_index": "mywords",
                "doc": {"word": word},
            }

    async def main():
        async for ok, result in async_streaming_bulk(es, gendata()):
            action, result = result.popitem()
            if not ok:
                print("failed to %s document %s" % ())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Scan
~~~~

 .. autofunction:: async_scan

 .. code-block:: python

    import asyncio
    from elasticsearch import AsyncElasticsearch
    from elasticsearch.helpers import async_scan

    es = AsyncElasticsearch()

    async def main():
        async for doc in async_scan(
            client=es,
            query={"query": {"match": {"title": "python"}}},
            index="orders-*"
        ):
            print(doc)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Reindex
~~~~~~~

 .. autofunction:: async_reindex


Frequently Asked Questions
--------------------------

NameError / ImportError when importing ``AsyncElasticsearch``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If when trying to use ``AsyncElasticsearch`` and you're receiving a ``NameError`` or ``ImportError``
you should ensure that you're installing via the ``elasticsearch[async]`` extra given above.
The ``AsyncElasticsearch`` name won't be available unless ``aiohttp`` and other async dependencies
are installed and you're using Python 3.6 or later.

What about the ``elasticsearch-async`` package?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Previously asyncio was supported separately via the `elasticsearch-async <https://github.com/elastic/elasticsearch-py-async>`_ package.
elasticsearch-async has been deprecated in favor of ``elasticsearch`` async support.
For Elasticsearch 7.x and later you must install
``elasticsearch[async]`` and use ``elasticsearch.AsyncElasticsearch()``.

Receiving 'Unclosed client session / connector' warning?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This warning is created by ``aiohttp`` when an open HTTP connection is
garbage collected. You'll typically run into this when closing your application.
To resolve the issue ensure that :meth:`~elasticsearch.AsyncElasticsearch.close`
is called before the :py:class:`~elasticsearch.AsyncElasticsearch` instance is garbage collected.

For example if using FastAPI that might look like this:

 .. code-block:: python

    from fastapi import FastAPI
    from elasticsearch import AsyncElasticsearch

    app = FastAPI()
    es = AsyncElasticsearch()

    # This gets called once the app is shutting down.
    @app.on_event("shutdown")
    async def app_shutdown():
        await es.close()


API Reference
-------------

 .. py:module:: elasticsearch

The API of :class:`~elasticsearch.AsyncElasticsearch` is nearly identical
to the API of :class:`~elasticsearch.Elasticsearch` with the exception that
every API call like :py:func:`~elasticsearch.AsyncElasticsearch.search` is
an ``async`` function and requires an ``await`` to properly return the response
body.

AsyncElasticsearch
~~~~~~~~~~~~~~~~~~

 .. note::

    To reference Elasticsearch APIs that are namespaced like ``.indices.create()``
    refer to the sync API reference. These APIs are identical between sync and async.

 .. autoclass:: AsyncElasticsearch
   :members:

AsyncTransport
~~~~~~~~~~~~~~

 .. autoclass:: AsyncTransport
   :members:

AIOHttpConnection
~~~~~~~~~~~~~~~~~

 .. autoclass:: AIOHttpConnection
   :members:

.. _helpers:

Helpers
=======

Collection of simple helper functions that abstract some specifics of the raw API.


Bulk helpers
------------

There are several helpers for the ``bulk`` API since its requirement for
specific formatting and other considerations can make it cumbersome if used directly.

All bulk helpers accept an instance of ``Elasticsearch`` class and an iterable
``actions`` (any iterable, can also be a generator, which is ideal in most
cases since it will allow you to index large datasets without the need of
loading them into memory).

The items in the ``action`` iterable should be the documents we wish to index
in several formats. The most common one is the same  as returned by
:meth:`~elasticsearch.Elasticsearch.search`, for example:

.. code:: python

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

Alternatively, if `_source` is not present, it will pop all metadata fields
from the doc and use the rest as the document data:

.. code:: python

    {
        "_id": 42,
        "_routing": 5,
        "title": "Hello World!",
        "body": "..."
    }

The :meth:`~elasticsearch.Elasticsearch.bulk` api accepts ``index``, ``create``,
``delete``, and ``update`` actions. Use the ``_op_type`` field to specify an
action (``_op_type`` defaults to ``index``):

.. code:: python

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


Example:
~~~~~~~~

Lets say we have an iterable of data. Lets say a list of words called ``mywords``
and we want to index those words into individual documents where the structure of the
document is like ``{"word": "<myword>"}``.

.. code:: python

    def gendata():
        mywords = ['foo', 'bar', 'baz']
        for word in mywords:
            yield {
                "_index": "mywords",
                "word": word,
            }

    bulk(es, gendata())


For a more complete and complex example please take a look at
https://github.com/elastic/elasticsearch-py/blob/main/examples/bulk-ingest

The :meth:`~elasticsearch.Elasticsearch.parallel_bulk` api is a wrapper around the :meth:`~elasticsearch.Elasticsearch.bulk` api to provide threading. :meth:`~elasticsearch.Elasticsearch.parallel_bulk` returns a generator which must be consumed to produce results.

To see the results use:

.. code:: python

    for success, info in parallel_bulk(...):
    if not success:
        print('A document failed:', info)
        
If you don't care about the results, you can use deque from collections:

.. code:: python

    from collections import deque
    deque(parallel_bulk(...), maxlen=0)

.. note::

    When reading raw json strings from a file, you can also pass them in
    directly (without decoding to dicts first). In that case, however, you lose
    the ability to specify anything (index, op_type and even id) on a per-record
    basis, all documents will just be sent to elasticsearch to be indexed
    as-is.


.. py:module:: elasticsearch.helpers

.. autofunction:: streaming_bulk

.. autofunction:: parallel_bulk

.. autofunction:: bulk


Scan
----

.. autofunction:: scan


Reindex
-------

.. autofunction:: reindex

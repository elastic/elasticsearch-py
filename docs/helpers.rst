.. _helpers:

Helpers
=======

Collection of simple helper functions that abstract some specifics or the raw
API.


Bulk helpers
------------

There are several helpers for the ``bulk`` API since it's requirement for
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
        '_type': 'document',
        '_id': 42,
        '_parent': 5,
        '_ttl': '1d',
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
        "_parent": 5,
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
        '_type': 'document',
        '_id': 42,
    }
    {
        '_op_type': 'update',
        '_index': 'index-name',
        '_type': 'document',
        '_id': 42,
        'doc': {'question': 'The life, universe and everything.'}
    }


.. note::

    When reading raw json strings from a file, you can also pass them in
    directly (without decoding to dicts first). In that case, however, you lose
    the ability to specify anything (index, type, even id) on a per-record
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

Python Elasticsearch Client
===========================

.. image:: https://img.shields.io/pypi/v/elasticsearch
   :target: https://pypi.org/project/elasticsearch

.. image:: https://pepy.tech/badge/elasticsearch
   :target: https://pepy.tech/project/elasticsearch?versions=*

.. image:: https://clients-ci.elastic.co/job/elastic+elasticsearch-py+master/badge/icon
   :target: https://clients-ci.elastic.co/job/elastic+elasticsearch-py+master

.. image:: https://readthedocs.org/projects/elasticsearch-py/badge/?version=latest&style=flat
   :target: https://elasticsearch-py.readthedocs.io

Official low-level client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.

Installation
------------

Install the ``elasticsearch`` package with `pip
<https://pypi.org/project/elasticsearch>`_::

    $ python -m pip install elasticsearch

If your application uses async/await in Python you can install with
the ``async`` extra::

    $ python -m pip install elasticsearch[async]

Read more about `how to use asyncio with this project <https://elasticsearch-py.readthedocs.io/en/master/async.html>`_.


Compatibility
-------------

The library is compatible with all Elasticsearch versions since ``0.90.x`` but you
**have to use a matching major version**:

For **Elasticsearch 7.0** and later, use the major version 7 (``7.x.y``) of the
library.

For **Elasticsearch 6.0** and later, use the major version 6 (``6.x.y``) of the
library.

For **Elasticsearch 5.0** and later, use the major version 5 (``5.x.y``) of the
library.

For **Elasticsearch 2.0** and later, use the major version 2 (``2.x.y``) of the
library, and so on.

The recommended way to set your requirements in your `setup.py` or
`requirements.txt` is::

    # Elasticsearch 7.x
    elasticsearch>=7.0.0,<8.0.0

    # Elasticsearch 6.x
    elasticsearch>=6.0.0,<7.0.0

    # Elasticsearch 5.x
    elasticsearch>=5.0.0,<6.0.0

    # Elasticsearch 2.x
    elasticsearch>=2.0.0,<3.0.0

If you have a need to have multiple versions installed at the same time older
versions are also released as ``elasticsearch2`` and ``elasticsearch5``.


Example use
-----------

.. code-block:: python

    >>> from datetime import datetime
    >>> from elasticsearch import Elasticsearch

    # by default we connect to localhost:9200
    >>> es = Elasticsearch()

    # create an index in elasticsearch, ignore status code 400 (index already exists)
    >>> es.indices.create(index='my-index', ignore=400)
    {'acknowledged': True, 'shards_acknowledged': True, 'index': 'my-index'}

    # datetimes will be serialized
    >>> es.index(index="my-index", id=42, body={"any": "data", "timestamp": datetime.now()})
    {'_index': 'my-index',
     '_type': '_doc',
     '_id': '42',
     '_version': 1,
     'result': 'created',
     '_shards': {'total': 2, 'successful': 1, 'failed': 0},
     '_seq_no': 0,
     '_primary_term': 1}

    # but not deserialized
    >>> es.get(index="my-index", id=42)['_source']
    {'any': 'data', 'timestamp': '2019-05-17T17:28:10.329598'}

Elastic Cloud (and SSL) use-case:

.. code-block:: python

    >>> from elasticsearch import Elasticsearch
    >>> es = Elasticsearch(cloud_id="<some_long_cloud_id>", http_auth=('elastic','yourpassword'))
    >>> es.info()

Using SSL Context with a self-signed cert use-case:

.. code-block:: python

    >>> from elasticsearch import Elasticsearch
    >>> from ssl import create_default_context

    >>> context = create_default_context(cafile="path/to/cafile.pem")
    >>> es = Elasticsearch("https://elasticsearch.url:port", ssl_context=context, http_auth=('elastic','yourpassword'))
    >>> es.info()


Features
--------

The client's features include:

* translating basic Python data types to and from json (datetimes are not
  decoded for performance reasons)
* configurable automatic discovery of cluster nodes
* persistent connections
* load balancing (with pluggable selection strategy) across all available nodes
* failed connection penalization (time based - failed connections won't be
  retried until a timeout is reached)
* support for ssl and http authentication
* thread safety
* pluggable architecture


Elasticsearch-DSL
-----------------

For a more high level client library with more limited scope, have a look at
`elasticsearch-dsl`_ - a more pythonic library sitting on top of
``elasticsearch-py``.

`elasticsearch-dsl`_ provides a more convenient and idiomatic way to write and manipulate
`queries`_ by mirroring the terminology and structure of Elasticsearch JSON DSL
while exposing the whole range of the DSL from Python
either directly using defined classes or a queryset-like expressions.

It also provides an optional `persistence layer`_ for working with documents as
Python objects in an ORM-like fashion: defining mappings, retrieving and saving
documents, wrapping the document data in user-defined classes.

.. _elasticsearch-dsl: https://elasticsearch-dsl.readthedocs.io/
.. _queries: https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
.. _persistence layer: https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#doctype


License
-------

Copyright 2021 Elasticsearch B.V. Licensed under the Apache License, Version 2.0.

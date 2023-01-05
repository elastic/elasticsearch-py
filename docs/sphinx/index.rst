Python Elasticsearch Client
===========================

Official low-level client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.


Installation
------------

Install the ``elasticsearch`` package with `pip
<https://pypi.org/project/elasticsearch>`_:

.. code-block:: console

    $ python -m pip install elasticsearch

If your application uses async/await in Python you can install with
the ``async`` extra:

.. code-block:: console

    $ python -m pip install elasticsearch[async]

Read more about `how to use asyncio with this project <async.html>`_.


Compatibility
-------------

Language clients are forward compatible; meaning that clients support communicating
with greater or equal minor versions of Elasticsearch. Elasticsearch language clients
are only backwards compatible with default distributions and without guarantees made.

If you have a need to have multiple versions installed at the same time older
versions are also released as ``elasticsearch2``, ``elasticsearch5`` and ``elasticsearch6``.


Example Usage
-------------

.. code-block:: python

    from datetime import datetime
    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }
    resp = es.index(index="test-index", id=1, document=doc)
    print(resp['result'])

    resp = es.get(index="test-index", id=1)
    print(resp['_source'])

    es.indices.refresh(index="test-index")

    resp = es.search(index="test-index", query={"match_all": {}})
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


Features
--------

This client was designed as very thin wrapper around Elasticsearch's REST API to
allow for maximum flexibility. This means that there are no opinions in this
client; it also means that some of the APIs are a little cumbersome to use from
Python. We have created some :ref:`helpers` to help with this issue as well as
a more high level library (`elasticsearch-dsl`_) on top of this one to provide
a more convenient way of working with Elasticsearch.



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


Contents
--------

.. toctree::
   :maxdepth: 3

   api
   exceptions
   async
   helpers
   Release Notes <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/release-notes.html>

License
-------

Copyright 2023 Elasticsearch B.V. Licensed under the Apache License, Version 2.0.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

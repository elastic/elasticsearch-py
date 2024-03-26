Python Elasticsearch Client
===========================

Official low-level client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.

`Download the latest version of Elasticsearch <https://www.elastic.co/downloads/elasticsearch>`_
or
`sign-up <https://cloud.elastic.co/registration?elektra=en-ess-sign-up-page>`_
for a free trial of Elastic Cloud.


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

Language clients are forward compatible; meaning that the clients support
communicating with greater or equal minor versions of Elasticsearch without
breaking. It does not mean that the clients automatically support new features
of newer Elasticsearch versions; it is only possible after a release of a new
client version. For example, a 8.12 client version won't automatically support
the new features of the 8.13 version of Elasticsearch, the 8.13 client version
is required for that. Elasticsearch language clients are only backwards
compatible with default distributions and without guarantees made.

+-----------------------+-------------------------+-----------+
| Elasticsearch version | elasticsearch-py branch | Supported |
+=======================+=========================+===========+
| main                  | main                    |           |
+-----------------------+-------------------------+-----------+
| 8.x                   | 8.x                     | 8.x       |
+-----------------------+-------------------------+-----------+
| 7.x                   | 7.x                     | 7.17      |
+-----------------------+-------------------------+-----------+

If you need multiple versions installed at the same time, versions are
also released, such as ``elasticsearch7`` and ``elasticsearch8``.


Example Usage
-------------

.. code-block:: python

    from datetime import datetime
    from elasticsearch import Elasticsearch

    client = Elasticsearch("http://localhost:9200/", api_key="YOUR_API_KEY")

    doc = {
        "author": "kimchy",
        "text": "Elasticsearch: cool. bonsai cool.",
        "timestamp": datetime.now(),
    }
    resp = client.index(index="test-index", id=1, document=doc)
    print(resp["result"])

    resp = client.get(index="test-index", id=1)
    print(resp["_source"])

    client.indices.refresh(index="test-index")

    resp = client.search(index="test-index", query={"match_all": {}})
    print("Got {} hits:".format(resp["hits"]["total"]["value"]))
    for hit in resp["hits"]["hits"]:
        print("{timestamp} {author} {text}".format(**hit["_source"]))

See more examples in the :ref:`quickstart` page.



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

   quickstart
   interactive
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

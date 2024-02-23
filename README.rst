.. raw:: html

   <img align="right" width="auto" height="auto" src="https://www.elastic.co/static-res/images/elastic-logo-200.png">

Elasticsearch Python Client
===========================

.. image:: https://img.shields.io/pypi/v/elasticsearch
   :target: https://pypi.org/project/elasticsearch

.. image:: https://img.shields.io/conda/vn/conda-forge/elasticsearch?color=blue
   :target: https://anaconda.org/conda-forge/elasticsearch

.. image:: https://static.pepy.tech/badge/elasticsearch
   :target: https://pepy.tech/project/elasticsearch?versions=*

.. image:: https://clients-ci.elastic.co/job/elastic+elasticsearch-py+main/badge/icon
   :target: https://clients-ci.elastic.co/job/elastic+elasticsearch-py+main

.. image:: https://readthedocs.org/projects/elasticsearch-py/badge/?version=latest&style=flat
   :target: https://elasticsearch-py.readthedocs.io

*The official Python client for Elasticsearch.*


Features
--------

* Translating basic Python data types to and from JSON
* Configurable automatic discovery of cluster nodes
* Persistent connections
* Load balancing (with pluggable selection strategy) across available nodes
* Failed connection penalization (time based - failed connections won't be
  retried until a timeout is reached)
* Support for TLS and HTTP authentication
* Thread safety across requests
* Pluggable architecture
* Helper functions for idiomatically using APIs together


Installation
------------

`Download the latest version of Elasticsearch <https://www.elastic.co/downloads/elasticsearch>`_
or
`sign-up <https://cloud.elastic.co/registration?elektra=en-ess-sign-up-page>`_
for a free trial of Elastic Cloud.

Refer to the `Installation section <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_installation>`_ 
of the getting started documentation.


Connecting
----------

Refer to the `Connecting section <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_connecting>`_ 
of the getting started documentation.


Usage
-----

* `Creating an index <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_creating_an_index>`_ 
* `Indexing a document <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_indexing_documents>`_
* `Getting documents <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_getting_documents>`_
* `Searching documents <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_searching_documents>`_
* `Updating documents <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_updating_documents>`_ 
* `Deleting documents <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_deleting_documents>`_
* `Deleting an index <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_deleting_an_index>`_


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

If you have a need to have multiple versions installed at the same time older
versions are also released as ``elasticsearch7`` and ``elasticsearch8``.


Documentation
-------------

Documentation for the client is `available on elastic.co`_ and `Read the Docs`_.

.. _available on elastic.co: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
.. _Read the Docs: https://elasticsearch-py.readthedocs.io


License
-------

Copyright 2023 Elasticsearch B.V. Licensed under the Apache License, Version 2.0.

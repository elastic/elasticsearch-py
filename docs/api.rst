.. _api:

API Documentation
=================

All the API calls map the raw REST api as closely as possible, including the
distinction between required and optional arguments to the calls. This means
that the code makes distinction between positional and keyword arguments; we,
however, recommend that people **use keyword arguments for all calls for
consistency and safety**.

An API call is considered successful (and will return a response) if
elasticsearch returns a 2XX response. Otherwise an instance of
:class:`~elasticsearch.TransportError` (or a more specific subclass) will be
raised. You can see other exception and error states in :ref:`exceptions`. If
you do not wish an exception to be raised you can always pass in an ``ignore``
parameter with either a single status code that should be ignored or a list of
them::

    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    # ignore 400 cause by IndexAlreadyExistsException when creating an index
    es.indices.create(index='test-index', ignore=400)

    # ignore 404 and 400
    es.indices.delete(index='test-index', ignore=[400, 404])

.. note::
   
    for compatibility with the Python ecosystem we use ``from_`` instead of
    ``from`` and ``doc_type`` instead of ``type`` as parameter names.

.. py:module:: elasticsearch

Elasticsearch
-------------

.. autoclass:: Elasticsearch
   :members:

.. py:module:: elasticsearch.client

Indices
-------

.. autoclass:: IndicesClient
   :members:

Cluster
-------

.. autoclass:: ClusterClient
   :members:

Nodes
-----

.. autoclass:: NodesClient
   :members:

Cat
---

.. autoclass:: CatClient
   :members:

Snapshot
---

.. autoclass:: SnapshotClient
   :members:


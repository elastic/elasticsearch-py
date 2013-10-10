.. _api:

API Documentation
=================

.. note::

    All the API calls map the raw REST api as closely as possible, including
    the distinction between required and optional arguments to the calls. This
    means that the code makes distinction between positional and keyword arguments;
    we, however, recommend that people use keyword arguments for all calls for
    consistency and safety.

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


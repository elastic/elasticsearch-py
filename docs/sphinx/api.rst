.. _api:

Elasticsearch API Reference
===========================

All the API calls map the raw REST API as closely as possible, including the
distinction between required and optional arguments to the calls. Keyword
arguments are required for all 

.. note::

   Some API parameters in Elasticsearch are reserved keywords in Python.
   For example the ``from`` query parameter for pagination would be
   aliased as ``from_``.


Elasticsearch
-------------

.. py:module:: elasticsearch

.. autoclass:: Elasticsearch
   :members:

.. py:module:: elasticsearch.client

Async Search
------------

.. autoclass:: AsyncSearchClient
   :members:

Autoscaling
-----------

.. autoclass:: AutoscalingClient
   :members:

Cat
---

.. autoclass:: CatClient
   :members:

Cross-Cluster Replication (CCR)
-------------------------------

.. autoclass:: CcrClient
   :members:

Cluster
-------

.. autoclass:: ClusterClient
   :members:

Dangling Indices
----------------

.. autoclass:: DanglingIndicesClient
   :members:

Enrich Policies
---------------

.. autoclass:: EnrichClient
   :members:

Event Query Language (EQL)
--------------------------

.. autoclass:: EqlClient
   :members:

Snapshottable Features
----------------------

.. autoclass:: FeaturesClient
   :members:

Fleet
-----

.. autoclass:: FleetClient
   :members:

Graph Explore
-------------

.. autoclass:: GraphClient
   :members:

Index Lifecycle Management (ILM)
--------------------------------

.. autoclass:: IlmClient
   :members:

Indices
-------

.. autoclass:: IndicesClient
   :members:

Ingest Pipelines
----------------

.. autoclass:: IngestClient
   :members:

License
-------

.. autoclass:: LicenseClient
   :members:

Logstash
--------

.. autoclass:: LogstashClient
   :members:

Migration
---------

.. autoclass:: MigrationClient
   :members:

Machine Learning (ML)
---------------------

.. autoclass:: MlClient
   :members:

Monitoring
----------

.. autoclass:: MonitoringClient
   :members:

Nodes
-----

.. autoclass:: NodesClient
   :members:

Rollup Indices
--------------

.. autoclass:: RollupClient
   :members:

Searchable Snapshots
--------------------

.. autoclass:: SearchableSnapshotsClient
   :members:

Security
--------

.. autoclass:: SecurityClient
   :members:

Shutdown
--------

.. autoclass:: ShutdownClient
   :members:

Snapshot Lifecycle Management (SLM)
-----------------------------------

.. autoclass:: SlmClient
   :members:

Snapshots
---------

.. autoclass:: SnapshotClient
   :members:

SQL
---

.. autoclass:: SqlClient
   :members:

TLS/SSL
-------

.. autoclass:: SslClient
   :members:

Tasks
-----

.. autoclass:: TasksClient
   :members:

Text Structure
--------------

.. autoclass:: TextStructureClient
   :members:

Transforms
----------

.. autoclass:: TransformClient
   :members:

Watcher
-------

.. autoclass:: WatcherClient
   :members:

X-Pack
------

.. autoclass:: XPackClient
   :members:

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


Contents
--------

.. toctree::
   :maxdepth: 3

   rest-apis/elasticsearch 
   rest-apis/autoscaling
   rest-apis/cat
   rest-apis/ccr
   rest-apis/cluster
   rest-apis/dangling-indices
   rest-apis/enrich-policies
   rest-apis/eql
   rest-apis/fleet
   rest-apis/snapshottable-features 




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

Query rules
-----------

.. autoclass:: QueryRulesetClient
   :members:

Rollup Indices
--------------

.. autoclass:: RollupClient
   :members:

Search Applications
-------------------

.. autoclass:: SearchApplicationClient
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

Synonyms
--------

.. autoclass:: SynonymsClient
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

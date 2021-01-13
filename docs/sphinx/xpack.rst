.. _xpack:

X-Pack APIs
===========

X-Pack is an Elastic Stack extension that bundles security, alerting, monitoring,
reporting, and graph capabilities into one easy-to-install package.
While the X-Pack components are designed to work together seamlessly, you can
easily enable or disable the features you want to use.

.. py:module:: elasticsearch.client


X-Pack Info
-----------

`X-Pack Info API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/info-api.html>`_
provides general info about the installed X-Pack.

.. autoclass:: XPackClient
   :members:

Autoscaling
-----------

`Autoscaling API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/autoscaling-apis.html>`_
is used to perform autoscaling operations.

.. autoclass:: AutoscalingClient
   :members:

Cross-Cluster Replication
-------------------------

`Cross-Cluster Replication APIs <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/ccr-apis.html>`_
are used to perform cross-cluster replication operations.

.. autoclass:: CcrClient
   :members:

Enrich
------

`Enrich APIs <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/enrich-apis.html>`_
can be used to add data from your existing indices to incoming documents during ingest.

.. autoclass:: EnrichClient
   :members:

EQL
---

`EQL APIs <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/eql.html>`_
accept EQL to query event-based time series data, such as logs, metrics, and traces.

.. autoclass:: EqlClient
   :members:

Graph Explore
-------------

`Graph Explore API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/graph-explore-api.html>`_
enables you to extract and summarize information about the documents and terms in your Elasticsearch index.

.. autoclass:: GraphClient
   :members:

Index Lifecycle Management (ILM)
--------------------------------

`Index Lifecycle Management APIs <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/index-lifecycle-management-api.html>`_
used to set up policies to automatically manage the index lifecycle.

.. autoclass:: IlmClient
   :members:

Licensing
---------

`License APIs <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/licensing-apis.html>`_
can be used to manage your licences.

.. autoclass:: LicenseClient
   :members:

Machine Learning
----------------

`Machine Learning APIs <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/ml-apis.html>`_
can be useful for discovering new patterns about your data. For a more detailed explanation
about X-Pack's machine learning please refer to the official documentation.

.. autoclass:: MlClient
   :members:

Migration
---------

`Migration API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/migration-api.html>`_
helps simplify upgrading X-Pack indices from one version to another.

.. autoclass:: MigrationClient
   :members:

Monitoring
----------

`Monitoring API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/es-monitoring.html>`_
used to collect data from the Elasticsearch nodes, Logstash nodes, Kibana instances, and Beats in your cluster.

.. autoclass:: MonitoringClient
   :members:

Rollup
------

`Rollup API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/rollup-apis.html>`_
enables searching through rolled-up data using the standard query DSL.

.. autoclass:: RollupClient
   :members:

Searchable Snapshots
--------------------

`Searchable Snapshots API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/searchable-snapshots-apis.html>`_
used to perform searchable snapshots operations.

.. autoclass:: SearchableSnapshotsClient
   :members:

Security
--------

`Security API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/security-api.html>`_
can be used to help secure your Elasticsearch cluster. Integrating with LDAP and Active Directory.

.. autoclass:: SecurityClient
   :members:

Snapshot Lifecycle Management (SLM)
-----------------------------------

`Snapshot Lifecycle Management API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/snapshot-lifecycle-management-api.html>`_
can be used to set up policies to automatically take snapshots and control how long they are retained.

.. autoclass:: SlmClient
   :members:

SQL
---

The `SQL REST API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/sql-rest.html>`_
accepts SQL in a JSON document, executes it, and returns the results.

.. autoclass:: SqlClient
   :members:

SSL Certificate
---------------

`SSL Certificate API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/security-api-ssl.html>`_
enables you to retrieve information about the X.509 certificates that are used
to encrypt communications in your Elasticsearch cluster.

.. autoclass:: SslClient
   :members:

Text Structure
--------------

`Text Structure API <https://www.elastic.co/guide/en/elasticsearch/reference/master/ml-find-file-structure.html>`_
finds the structure of a text file. The text file must contain data that is
suitable to be ingested into Elasticsearch.

.. autoclass:: TextStructureClient
   :members:

Transform
---------

`Transform API <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/transform-apis.html>`_
manages transformation operations from grabbing data from source indices, transforms it, and
saves it to a destination index.

.. autoclass:: TransformClient
   :members:

Watcher
-------

`Watcher APIs <https://www.elastic.co/guide/en/elasticsearch/reference/7.x/watcher-api.html>`_
can be used to notify you when certain pre-defined thresholds have happened.

.. autoclass:: WatcherClient
   :members:

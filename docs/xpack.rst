.. _xpack:

X-Pack APIs
===========

X-Pack is an Elastic Stack extension that bundles security, alerting, monitoring,
reporting, and graph capabilities into one easy-to-install package.
While the X-Pack components are designed to work together seamlessly, you can
easily enable or disable the features you want to use.


Info
----

`X-Pack info <https://www.elastic.co/guide/en/elasticsearch/reference/current/info-api.html>`_
provides general info about the installed X-Pack.

.. py:module:: elasticsearch.client.xpack

.. autoclass:: XPackClient
   :members:


Graph Explore APIs
------------------

`Graph Explore API <https://www.elastic.co/guide/en/elasticsearch/reference/current/graph-explore-api.html>`_
enables you to extract and summarize information about the documents and terms in your Elasticsearch index.

.. py:module:: elasticsearch.client.xpack.graph


.. autoclass:: GraphClient
   :members:


Licensing APIs
--------------

`Licensing API <https://www.elastic.co/guide/en/elasticsearch/reference/current/licensing-apis.html>`_
can be used to manage your licences.


.. py:module:: elasticsearch.client.xpack.license


.. autoclass:: LicenseClient
   :members:

Machine Learning APIs
---------------------

`Machine Learning <https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-apis.html>`_
can be useful for discovering new patterns about your data. For a more detailed explanation
about X-Pack's machine learning please refer to the official documentation.


.. py:module:: elasticsearch.client.xpack.ml


.. autoclass:: MlClient
   :members:

Security APIs
-------------

`Security API <https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api.html>`_
can be used to help secure your Elasticsearch cluster. Integrating with LDAP and Active Directory.

.. py:module:: elasticsearch.client.xpack.security


.. autoclass:: SecurityClient
   :members:

Watcher APIs
-------------

`Watcher API <https://www.elastic.co/guide/en/elasticsearch/reference/current/watcher-api.html>`_
can be used to notify you when certain pre-defined thresholds have happened.

.. py:module:: elasticsearch.client.xpack.watcher

.. autoclass:: WatcherClient
   :members:


Migration APIs
---------------

`Migration API <https://www.elastic.co/guide/en/elasticsearch/reference/current/migration-api.html>`_
helps simplify upgrading X-Pack indices from one version to another.

.. py:module:: elasticsearch.client.xpack.migration

.. autoclass:: MigrationClient
   :members:


Monitoring APIs
----------------

`Monitoring API <https://www.elastic.co/guide/en/elasticsearch/reference/master/es-monitoring.html>`_
used to collect data from the Elasticsearch nodes, Logstash nodes, Kibana instances, and Beats in your cluster.

.. py:module:: elasticsearch.client.xpack.monitoring

.. autoclass:: MonitoringClient
   :members:


Deprecation APIs
-----------------

`Deprecation API <https://www.elastic.co/guide/en/elasticsearch/reference/master/migration-api-deprecation.html>`_
used to retrieve information about different cluster, node, and index level settings that use deprecated features
that will be removed or changed in the next major version.

.. py:module:: elasticsearch.client.xpack.deprecation

.. autoclass:: DeprecationClient
   :members:

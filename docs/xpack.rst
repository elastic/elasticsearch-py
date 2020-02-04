.. _xpack:

X-Pack APIs
===========

X-Pack is an Elastic Stack extension that bundles security, alerting, monitoring,
reporting, and graph capabilities into one easy-to-install package.
While the X-Pack components are designed to work together seamlessly, you can
easily enable or disable the features you want to use.



Info
----

`X-Pack info <https://www.elastic.co/guide/en/elasticsearch/reference/6.2/info-api.html>`_
provides general info about the installed X-Pack.

.. py:module:: elasticsearch.client.xpack

.. autoclass:: XPackClient
   :members:


Graph Explore
-------------
`X-Pack Graph Explore <https://www.elastic.co/guide/en/elasticsearch/reference/6.2/graph-explore-api.html>`_
enables you to extract and summarize information about the documents and terms in your Elasticsearch index.

.. py:module:: elasticsearch.client.graph


.. autoclass:: GraphClient
   :members:

Licensing API
-------------

`Licensing API <https://www.elastic.co/guide/en/elasticsearch/reference/6.2/licensing-apis.html>`_
can be used to manage your licences.


.. py:module:: elasticsearch.client.license


.. autoclass:: LicenseClient
   :members:

Machine Learning APIs
---------------------

`Machine Learning <https://www.elastic.co/guide/en/elasticsearch/reference/6.2/ml-apis.html>`_
can be useful for discovering new patterns about your data. For a more detailed explanation
about X-Pack's machine learning please refer to the official documentation.


.. py:module:: elasticsearch.client.ml


.. autoclass:: MlClient
   :members:

Security APIs
-------------

`Security API <https://www.elastic.co/guide/en/elasticsearch/reference/6.2/security-api.html>`_
can be used to help secure your Elasticsearch cluster. Integrating with LDAP and Active Directory.

.. py:module:: elasticsearch.client.security


.. autoclass:: SecurityClient
   :members:

Watcher APIs
-------------

`Watcher API <https://www.elastic.co/guide/en/elasticsearch/reference/6.2/watcher-api.html>`_
can be used to notify you when certain pre-defined thresholds have happened.

.. py:module:: elasticsearch.client.watcher

.. autoclass:: WatcherClient
   :members:


Migration APIs
---------------

`Migration API <https://www.elastic.co/guide/en/elasticsearch/reference/6.2/migration-api.html>`_
helps simplify upgrading X-Pack indices from one version to another.

.. py:module:: elasticsearch.client.migration

.. autoclass:: MigrationClient
   :members:


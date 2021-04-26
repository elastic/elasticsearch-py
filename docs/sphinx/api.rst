.. _api:

API Documentation
=================

All the API calls map the raw REST api as closely as possible, including the
distinction between required and optional arguments to the calls. This means
that the code makes distinction between positional and keyword arguments; we,
however, recommend that people **use keyword arguments for all calls for
consistency and safety**.

.. note::

    for compatibility with the Python ecosystem we use ``from_`` instead of
    ``from`` and ``doc_type`` instead of ``type`` as parameter names.


Global Options
--------------

Some parameters are added by the client itself and can be used in all API
calls.

Ignore
~~~~~~

An API call is considered successful (and will return a response) if
elasticsearch returns a 2XX response. Otherwise an instance of
:class:`~elasticsearch.TransportError` (or a more specific subclass) will be
raised. You can see other exception and error states in :ref:`exceptions`. If
you do not wish an exception to be raised you can always pass in an ``ignore``
parameter with either a single status code that should be ignored or a list of
them:

.. code-block:: python

    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    # ignore 400 cause by IndexAlreadyExistsException when creating an index
    es.indices.create(index='test-index', ignore=400)

    # ignore 404 and 400
    es.indices.delete(index='test-index', ignore=[400, 404])


Timeout
~~~~~~~

Global timeout can be set when constructing the client (see
:class:`~elasticsearch.Connection`'s ``timeout`` parameter) or on a per-request
basis using ``request_timeout`` (float value in seconds) as part of any API
call, this value will get passed to the ``perform_request`` method of the
connection class:

.. code-block:: python

    # only wait for 1 second, regardless of the client's default
    es.cluster.health(wait_for_status='yellow', request_timeout=1)

.. note::

    Some API calls also accept a ``timeout`` parameter that is passed to
    Elasticsearch server. This timeout is internal and doesn't guarantee that the
    request will end in the specified time.

Tracking Requests with Opaque ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can enrich your requests against Elasticsearch with an identifier string, that allows you to discover this identifier
in `deprecation logs <https://www.elastic.co/guide/en/elasticsearch/reference/7.4/logging.html#deprecation-logging>`_, to support you with
`identifying search slow log origin <https://www.elastic.co/guide/en/elasticsearch/reference/7.4/index-modules-slowlog.html#_identifying_search_slow_log_origin>`_
or to help with `identifying running tasks <https://www.elastic.co/guide/en/elasticsearch/reference/current/tasks.html#_identifying_running_tasks>`_.

 .. code-block:: python

    from elasticsearch import Elasticsearch

    client = Elasticsearch()

    # You can apply X-Opaque-Id in any API request via 'opaque_id':
    resp = client.get(index="test", id="1", opaque_id="request-1")


.. py:module:: elasticsearch

Response Filtering
~~~~~~~~~~~~~~~~~~

The ``filter_path`` parameter is used to reduce the response returned by
elasticsearch.  For example, to only return ``_id`` and ``_type``, do:

.. code-block:: python

    es.search(index='test-index', filter_path=['hits.hits._id', 'hits.hits._type'])

It also supports the ``*`` wildcard character to match any field or part of a
field's name:

.. code-block:: python

    es.search(index='test-index', filter_path=['hits.hits._*'])

Elasticsearch
-------------

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

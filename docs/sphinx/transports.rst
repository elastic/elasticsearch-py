.. _transports:

Transport classes
=================

List of transport classes that can be used, simply import your choice and pass
it to the constructor of :class:`~elasticsearch.Elasticsearch` as
`connection_class`. Note that the
:class:`~elasticsearch.connection.RequestsHttpConnection` requires ``requests``
to be installed.

For example to use the ``requests``-based connection just import it and use it:

.. code-block:: python

    from elasticsearch import Elasticsearch, RequestsHttpConnection
    es = Elasticsearch(connection_class=RequestsHttpConnection)

The default connection class is based on ``urllib3`` which is more performant
and lightweight than the optional ``requests``-based class. Only use
``RequestsHttpConnection`` if you have need of any of ``requests`` advanced
features like custom auth plugins etc.

Product check on first request
------------------------------

Starting in v7.14.0 the client performs a required product check before
the first API call is executed. This product check allows the client to
establish that it's communicating with a valid Elasticsearch cluster.

The product check requires a single HTTP request to the ``info`` API. In
most cases this request will succeed quickly and then no further product
check HTTP requests will be sent.

The product check will verify that the ``X-Elastic-Product: Elasticsearch``
HTTP header is being sent or if the ``info`` API response has proper values
of ``tagline`` and ``version.build_flavor``.

If the client detects that it's not connected to Elasticsearch the
``NotElasticsearchError`` exception will be raised. In previous versions
of Elasticsearch the ``info`` API required additional permissions so
if an authentication or authorization error is raised during the
product check then an ``ElasticsearchWarning`` is raised and the client
proceeds normally.

.. py:module:: elasticsearch.connection

Connection
----------

.. autoclass:: Connection

Urllib3HttpConnection
---------------------

.. autoclass:: Urllib3HttpConnection


RequestsHttpConnection
----------------------

.. autoclass:: RequestsHttpConnection


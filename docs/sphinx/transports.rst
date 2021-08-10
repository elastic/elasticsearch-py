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


Product check and unsupported distributions
-------------------------------------------

Starting in v7.14.0 the client performs a required product check before
the first API call is executed. This product check allows the client to
establish that it's communicating with a supported Elasticsearch cluster.

For 8.x clients the product check will verify that the ``X-Elastic-Product: Elasticsearch``
HTTP header is being sent with every response. If the client detects that it's not connected
to a supported distribution of Elasticsearch the ``UnsupportedProductError`` exception
will be raised.

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


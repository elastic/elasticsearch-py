.. _transports:

Transport classes
=================

List of transport classes that can be used, simply import your choice and pass
it to the constructor of :class:`~elasticsearch.Elasticsearch` as
`connection_class`. Note that the
:class:`~elasticsearch.connection.RequestsHttpConnection` requires ``requests``
to be installed.

For example to use the ``requests``-based connection just import it and use it::

    from elasticsearch import Elasticsearch, RequestsHttpConnection
    es = Elasticsearch(connection_class=RequestsHttpConnection)


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


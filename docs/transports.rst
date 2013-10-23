.. _transports:

Transport classes
=================

List of transport classes that can be used, simply import your choice and pass
it to the constructor of :class:`~elasticsearch.Elasticsearch` as
`connection_class`. Note that Thrift and Memcached protocols are experimental
and require a plugin to be installed in your cluster as well as additional
dependencies (`thrift==0.9` and `pylibmc==1.2`).

For example to use the thrift connection just import it and use it. The
connection classes are aware of their respective default ports (9500 for
thrift) so there is no need to specify them unless modified::

    from elasticsearch import Elasticsearch, ThriftConnection
    es = Elasticsearch(connection_class=ThriftConnection)


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


ThriftConnection
----------------

.. autoclass:: ThriftConnection


MemcachedConnection
-------------------

.. autoclass:: MemcachedConnection


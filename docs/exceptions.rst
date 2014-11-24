.. _exceptions:

Exceptions
==========

.. py:module:: elasticsearch

.. autoclass:: ImproperlyConfigured

.. autoclass:: ElasticsearchException

.. autoclass:: SerializationError(ElasticsearchException)

.. autoclass:: TransportError(ElasticsearchException)
   :members:

.. autoclass:: ConnectionError(TransportError)
.. autoclass:: ConnectionTimeout(ConnectionError)
.. autoclass:: SSLError(ConnectionError)

.. autoclass:: NotFoundError(TransportError)
.. autoclass:: ConflictError(TransportError)
.. autoclass:: RequestError(TransportError)
.. autoclass:: ConnectionError(TransportError)

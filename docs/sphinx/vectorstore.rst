.. _vectorstore:

Vector store
============

.. py:module:: elasticsearch.helpers.vectorstore

The vector store helpers wrap an Elasticsearch index that is used for vector
search. :class:`VectorStore` owns the index and the documents, a retrieval
strategy decides how the index is mapped and how a query is turned into an
Elasticsearch query, and an embedding service turns text into vectors.

Async variants of all of these classes are available and are prefixed with
``Async*``. Refer to :ref:`async_vectorstore`.

Vector stores
-------------

.. autoclass:: VectorStore
   :members:

Retrieval strategies
--------------------

.. autoclass:: RetrievalStrategy
   :members:

.. autoclass:: DenseVectorStrategy
   :members:

.. autoclass:: DenseVectorScriptScoreStrategy
   :members:

.. autoclass:: SparseVectorStrategy
   :members:

.. autoclass:: BM25Strategy
   :members:

.. autoclass:: DistanceMetric
   :members:

Embedding services
------------------

.. autoclass:: EmbeddingService
   :members:

.. autoclass:: ElasticsearchEmbeddings
   :members:

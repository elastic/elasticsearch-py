.. _async_vectorstore:

Async Vector store
==================

Async variants of all vector store helpers are available in
``elasticsearch.helpers.vectorstore`` and are all prefixed with ``Async*``.
These APIs are identical to the ones in the sync :ref:`vectorstore`
documentation, except that their methods have to be awaited.

.. py:module:: elasticsearch.helpers.vectorstore
   :no-index:

Vector stores
-------------

.. autoclass:: AsyncVectorStore
   :members:

Retrieval strategies
--------------------

.. autoclass:: AsyncRetrievalStrategy
   :members:

.. autoclass:: AsyncDenseVectorStrategy
   :members:

.. autoclass:: AsyncDenseVectorScriptScoreStrategy
   :members:

.. autoclass:: AsyncSparseVectorStrategy
   :members:

.. autoclass:: AsyncBM25Strategy
   :members:

Embedding services
------------------

.. autoclass:: AsyncEmbeddingService
   :members:

.. autoclass:: AsyncElasticsearchEmbeddings
   :members:

Quickstart 
==========

This guide shows you how to install the Elasticsearch Python client and perform basic
operations like indexing or searching documents.

Requirements
------------

- `Python <https://www.python.org/>`_ 3.6 or newer
- `pip <https://pip.pypa.io/en/stable/>`_


Installation
------------

To install the client, run the following command:

.. code-block:: console

    $ python -m pip install elasticsearch


Connecting
----------

You can connect to Elastic Cloud using an API key and the Cloud ID.

.. code-block:: python

    from elasticsearch import Elasticsearch

    client = Elasticsearch(cloud_id="YOUR_CLOUD_ID", api_key="YOUR_API_KEY")

Your Cloud ID can be found on the **My deployment** page of your deployment 
under **Cloud ID**.

You can generate an API key on the **Management** page under Security.

.. image:: ../guide/images/create-api-key.png


Using the client
----------------

Time to use Elasticsearch! This section walks you through the most important 
operations of Elasticsearch. The following examples assume that the Python 
client was instantiated as above.


Creating an index
^^^^^^^^^^^^^^^^^

This is how you create the `my_index` index:

.. code-block:: python

    client.indices.create(index="my_index")


Indexing documents
^^^^^^^^^^^^^^^^^^

This indexes a document with the index API:

.. code-block:: python

    client.index(
        index="my_index",
        id="my_document_id",
        document={
            "foo": "foo",
            "bar": "bar",
        },
    )


Getting documents
^^^^^^^^^^^^^^^^^

You can get documents by using the following code:

.. code-block:: python
    
    client.get(index="my_index", id="my_document_id")


Searching documents
^^^^^^^^^^^^^^^^^^^

This is how you can create a single match query with the Python client: 


.. code-block:: python

    client.search(index="my_index", query={"match": {"foo": {"query": "foo"}}})


Updating documents
^^^^^^^^^^^^^^^^^^

This is how you can update a document, for example to add a new field:

.. code-block:: python

    client.update(
        index="my_index",
        id="my_document_id",
        doc={
            "foo": "bar",
            "new_field": "new value",
        },
    )


Deleting documents
^^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    client.delete(index="my_index", id="my_document_id")


Deleting an index
^^^^^^^^^^^^^^^^^

.. code-block:: python
    
    client.indices.delete(index="my_index")

.. _connection_api:

Connection Layer API
====================

All of the classes responsible for handling the connection to the Elasticsearch
cluster. The default subclasses used can be overridden by passing parameters to the
:class:`~elasticsearch.Elasticsearch` class. All of the arguments to the client
will be passed on to :class:`~elasticsearch.Transport`,
:class:`~elasticsearch.ConnectionPool` and :class:`~elasticsearch.Connection`.

For example if you wanted to use your own implementation of the
:class:`~elasticsearch.ConnectionSelector` class you can just pass in the
``selector_class`` parameter.

.. note::

  :class:`~elasticsearch.ConnectionPool` and related options (like
  ``selector_class``) will only be used if more than one connection is defined.
  Either directly or via the :ref:`sniffing` mechanism.

.. py:module:: elasticsearch

Transport
---------

.. autoclass:: Transport(hosts, connection_class=Urllib3HttpConnection, connection_pool_class=ConnectionPool, host_info_callback=construct_hosts_list, sniff_on_start=False, sniffer_timeout=None, sniff_on_connection_fail=False, serializer=JSONSerializer(), max_retries=3, ** kwargs)
   :members:


Connection Pool
---------------

.. autoclass:: ConnectionPool(connections, dead_timeout=60, selector_class=RoundRobinSelector, randomize_hosts=True, ** kwargs)
   :members:


Connection Selector
-------------------

.. autoclass:: ConnectionSelector(opts)
   :members:


Urllib3HttpConnection (default connection_class)
------------------------------------------------

If you have complex SSL logic for connecting to Elasticsearch using an `SSLContext` object
might be more helpful. You can create one natively using the python SSL library with the
`create_default_context` (https://docs.python.org/3/library/ssl.html#ssl.create_default_context) method.

To create an `SSLContext` object you only need to use one of cafile, capath or cadata:

.. code-block:: python

    >>> from ssl import create_default_context
    >>> context = create_default_context(cafile=None, capath=None, cadata=None)

* `cafile` is the path to your CA File
* `capath` is the directory of a collection of CA's
* `cadata` is either an ASCII string of one or more PEM-encoded certificates or a bytes-like object of DER-encoded certificates.

Please note that the use of SSLContext is only available for urllib3.

.. autoclass:: Urllib3HttpConnection
   :members:


API Compatibility HTTP Header
-----------------------------

The Python client can be configured to emit an HTTP header
``Accept: application/vnd.elasticsearch+json; compatible-with=7``
which signals to Elasticsearch that the client is requesting
``7.x`` version of request and response bodies. This allows for
upgrading from 7.x to 8.x version of Elasticsearch without upgrading
everything at once. Elasticsearch should be upgraded first after
the compatibility header is configured and clients should be upgraded
second.

 .. code-block:: python

    from elasticsearch import Elasticsearch

    client = Elasticsearch("http://...", headers={"accept": "application/vnd.elasticsearch+json; compatible-with=7"})

If you'd like to have the client emit the header without configuring ``headers`` you
can use the environment variable ``ELASTIC_CLIENT_APIVERSIONING=1``.

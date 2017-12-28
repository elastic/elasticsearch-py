.. _connection_api:

Connection Layer API
====================

All of the classes responsible for handling the connection to the Elasticsearch
cluster. The default subclasses used can be overriden by passing parameters to the
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

.. autoclass:: Transport(hosts, connection_class=Urllib3HttpConnection, connection_pool_class=ConnectionPool, nodes_to_host_callback=construct_hosts_list, sniff_on_start=False, sniffer_timeout=None, sniff_on_connection_fail=False, serializer=JSONSerializer(), max_retries=3, ** kwargs)
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

Deprecation Notice: `use_ssl`, `verify_certs`, `ca_certs` and `ssl_version` are being
deprecated in favor of using a `SSLContext` (https://docs.python.org/3/library/ssl.html#ssl.SSLContext) object.

You can continue to use the deprecated parameters and an `SSLContext` will be created for you.

If you want to create your own `SSLContext` object you can create one natively using the
python SSL library with the `create_default_context` (https://docs.python.org/3/library/ssl.html#ssl.create_default_context) method
or you can use the wrapper function :function:`~elasticsearch.connection.http_urllib3.create_ssl_context`.

To create an `SSLContext` object you only need to use one of cafile, capath or cadata::

    >>> from elasticsearch.connection import create_ssl_context
    >>> context = create_ssl_context(cafile=None, capath=None, cadata=None)

* `cafile` is the path to your CA File
* `capath` is the directory of a collection of CA's
* `cadata` is either an ASCII string of one or more PEM-encoded certificates or a bytes-like object of DER-encoded certificates.

.. autoclass:: Urllib3HttpConnection
   :members:

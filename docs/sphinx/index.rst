Python Elasticsearch Client
===========================

Official low-level client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.


Installation
------------

Install the ``elasticsearch`` package with `pip
<https://pypi.org/project/elasticsearch>`_:

.. code-block:: console

    $ python -m pip install elasticsearch

If your application uses async/await in Python you can install with
the ``async`` extra:

.. code-block:: console

    $ python -m pip install elasticsearch[async]

Read more about `how to use asyncio with this project <async.html>`_.


Compatibility
-------------

The library is compatible with all Elasticsearch versions since ``0.90.x`` but you
**have to use a matching major version**:

For **Elasticsearch 7.0** and later, use the major version 7 (``7.x.y``) of the
library.

For **Elasticsearch 6.0** and later, use the major version 6 (``6.x.y``) of the
library.

For **Elasticsearch 5.0** and later, use the major version 5 (``5.x.y``) of the
library.

For **Elasticsearch 2.0** and later, use the major version 2 (``2.x.y``) of the
library, and so on.

The recommended way to set your requirements in your `setup.py` or
`requirements.txt` is:

.. code-block:: python

    # Elasticsearch 7.x
    elasticsearch>=7.0.0,<8.0.0

    # Elasticsearch 6.x
    elasticsearch>=6.0.0,<7.0.0

    # Elasticsearch 5.x
    elasticsearch>=5.0.0,<6.0.0

    # Elasticsearch 2.x
    elasticsearch>=2.0.0,<3.0.0

If you have a need to have multiple versions installed at the same time older
versions are also released as ``elasticsearch2``, ``elasticsearch5`` and ``elasticsearch6``.


Example Usage
-------------

.. code-block:: python

    from datetime import datetime
    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    doc = {
        'author': 'kimchy',
        'text': 'Elasticsearch: cool. bonsai cool.',
        'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", id=1, body=doc)
    print(res['result'])

    res = es.get(index="test-index", id=1)
    print(res['_source'])

    es.indices.refresh(index="test-index")

    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


Features
--------

This client was designed as very thin wrapper around Elasticsearch's REST API to
allow for maximum flexibility. This means that there are no opinions in this
client; it also means that some of the APIs are a little cumbersome to use from
Python. We have created some :ref:`helpers` to help with this issue as well as
a more high level library (`elasticsearch-dsl`_) on top of this one to provide
a more convenient way of working with Elasticsearch.

.. _elasticsearch-dsl: https://elasticsearch-dsl.readthedocs.io/

Persistent Connections
~~~~~~~~~~~~~~~~~~~~~~

``elasticsearch-py`` uses persistent connections inside of individual connection
pools (one per each configured or sniffed node). Out of the box you can choose
between two ``http`` protocol implementations. See :ref:`transports` for more
information.

The transport layer will create an instance of the selected connection class
per node and keep track of the health of individual nodes - if a node becomes
unresponsive (throwing exceptions while connecting to it) it's put on a timeout
by the :class:`~elasticsearch.ConnectionPool` class and only returned to the
circulation after the timeout is over (or when no live nodes are left). By
default nodes are randomized before being passed into the pool and round-robin
strategy is used for load balancing.

You can customize this behavior by passing parameters to the
:ref:`connection_api` (all keyword arguments to the
:class:`~elasticsearch.Elasticsearch` class will be passed through). If what
you want to accomplish is not supported you should be able to create a subclass
of the relevant component and pass it in as a parameter to be used instead of
the default implementation.


Automatic Retries
~~~~~~~~~~~~~~~~~

If a connection to a node fails due to connection issues (raises
:class:`~elasticsearch.ConnectionError`) it is considered in faulty state. It
will be placed on hold for ``dead_timeout`` seconds and the request will be
retried on another node. If a connection fails multiple times in a row the
timeout will get progressively larger to avoid hitting a node that's, by all
indication, down. If no live connection is available, the connection that has
the smallest timeout will be used.

By default retries are not triggered by a timeout
(:class:`~elasticsearch.ConnectionTimeout`), set ``retry_on_timeout`` to
``True`` to also retry on timeouts.

.. _sniffing:

Sniffing
~~~~~~~~

The client can be configured to inspect the cluster state to get a list of
nodes upon startup, periodically and/or on failure. See
:class:`~elasticsearch.Transport` parameters for details.

Some example configurations:

 .. code-block:: python

    from elasticsearch import Elasticsearch

    # by default we don't sniff, ever
    es = Elasticsearch()

    # you can specify to sniff on startup to inspect the cluster and load
    # balance across all nodes
    es = Elasticsearch(["seed1", "seed2"], sniff_on_start=True)

    # you can also sniff periodically and/or after failure:
    es = Elasticsearch(["seed1", "seed2"],
              sniff_on_start=True,
              sniff_on_connection_fail=True,
              sniffer_timeout=60)

Thread safety
~~~~~~~~~~~~~

The client is thread safe and can be used in a multi threaded environment. Best
practice is to create a single global instance of the client and use it
throughout your application. If your application is long-running consider
turning on :ref:`sniffing` to make sure the client is up to date on the cluster
location.

By default we allow ``urllib3`` to open up to 10 connections to each node, if
your application calls for more parallelism, use the ``maxsize`` parameter to
raise the limit:

.. code-block:: python

    # allow up to 25 connections to each node
    es = Elasticsearch(["host1", "host2"], maxsize=25)

.. note::

    Since we use persistent connections throughout the client it means that the
    client doesn't tolerate ``fork`` very well. If your application calls for
    multiple processes make sure you create a fresh client after call to
    ``fork``. Note that Python's ``multiprocessing`` module uses ``fork`` to
    create new processes on POSIX systems.

TLS/SSL and Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can configure the client to use ``SSL`` for connecting to your
elasticsearch cluster, including certificate verification and HTTP auth:

.. code-block:: python

    from elasticsearch import Elasticsearch

    # you can use RFC-1738 to specify the url
    es = Elasticsearch(['https://user:secret@localhost:443'])

    # ... or specify common parameters as kwargs

    es = Elasticsearch(
        ['localhost', 'otherhost'],
        http_auth=('user', 'secret'),
        scheme="https",
        port=443,
    )

    # SSL client authentication using client_cert and client_key

    from ssl import create_default_context

    context = create_default_context(cafile="path/to/cert.pem")
    es = Elasticsearch(
        ['localhost', 'otherhost'],
        http_auth=('user', 'secret'),
        scheme="https",
        port=443,
        ssl_context=context,
    )

..  warning::

    ``elasticsearch-py`` doesn't ship with default set of root certificates. To
    have working SSL certificate validation you need to either specify your own
    as ``cafile`` or ``capath`` or ``cadata``  or install `certifi`_ which will
    be picked up automatically.


See class :class:`~elasticsearch.Urllib3HttpConnection` for detailed
description of the options.

.. _certifi: http://certifiio.readthedocs.io/en/latest/

Connecting via Cloud ID
~~~~~~~~~~~~~~~~~~~~~~~

Cloud ID is an easy way to configure your client to work
with your Elastic Cloud deployment. Combine the ``cloud_id``
with either ``http_auth`` or ``api_key`` to authenticate
with your Elastic Cloud deployment.

Using ``cloud_id`` enables TLS verification and HTTP compression by default
and sets the port to ``443`` unless otherwise overwritten via the ``port`` parameter
or the port value encoded within ``cloud_id``.  Using Cloud ID also disables sniffing.

.. code-block:: python

    from elasticsearch import Elasticsearch

    es = Elasticsearch(
        cloud_id="cluster-1:dXMa5Fx...",
        http_auth=("elastic", "<password>"),
    )

API Key Authentication
~~~~~~~~~~~~~~~~~~~~~~

You can configure the client to use Elasticsearch's `API Key`_ for connecting to your cluster.
Please note this authentication method has been introduced with release of Elasticsearch ``6.7.0``.

    from elasticsearch import Elasticsearch

    # you can use the api key tuple
    es = Elasticsearch(
        ['node-1', 'node-2', 'node-3'],
        api_key=('id', 'api_key'),
    )

    # or you pass the base 64 encoded token
    es = Elasticsearch(
        ['node-1', 'node-2', 'node-3'],
        api_key='base64encoded tuple',
    )

.. _API Key: https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html

Logging
~~~~~~~

``elasticsearch-py`` uses the standard `logging library`_ from python to define
two loggers: ``elasticsearch`` and ``elasticsearch.trace``. ``elasticsearch``
is used by the client to log standard activity, depending on the log level.
``elasticsearch.trace`` can be used to log requests to the server in the form
of ``curl`` commands using pretty-printed json that can then be executed from
command line. Because it is designed to be shared (for example to demonstrate
an issue) it also just uses ``localhost:9200`` as the address instead of the
actual address of the host. If the trace logger has not been configured
already it is set to `propagate=False` so it needs to be activated separately.

.. _logging library: http://docs.python.org/3/library/logging.html

Type Hints
~~~~~~~~~~

Starting in ``elasticsearch-py`` v7.10.0 the library now ships with `type hints`_
and supports basic static type analysis with tools like `Mypy`_ and `Pyright`_.

If we write a script that has a type error like using ``request_timeout`` with
a ``str`` argument instead of ``float`` and then run Mypy on the script:

.. code-block:: python

    # script.py
    from elasticsearch import Elasticsearch

    es = Elasticsearch(...)
    es.search(
        index="test-index",
        request_timeout="5"  # type error!
    )

    # $ mypy script.py
    # script.py:5: error: Argument "request_timeout" to "search" of "Elasticsearch" has 
    #                     incompatible type "str"; expected "Union[int, float, None]"
    # Found 1 error in 1 file (checked 1 source file)

For now many parameter types for API methods aren't specific to
a type (ie they are of type ``typing.Any``) but in the future
they will be tightened for even better static type checking.

Type hints also allow tools like your IDE to check types and provide better
auto-complete functionality.

.. warning::

    The type hints for API methods like ``search`` don't match the function signature
    that can be found in the source code. Type hints represent optimal usage of the
    API methods. Using keyword arguments is highly recommended so all optional parameters
    and ``body`` are keyword-only in type hints.

    JetBrains PyCharm will use the warning ``Unexpected argument`` to denote that the
    parameter may be keyword-only.

.. _type hints: https://www.python.org/dev/peps/pep-0484
.. _mypy: http://mypy-lang.org
.. _pyright: https://github.com/microsoft/pyright


Environment considerations
--------------------------

When using the client there are several limitations of your environment that
could come into play.

When using an HTTP load balancer you cannot use the :ref:`sniffing`
functionality - the cluster would supply the client with IP addresses to
directly connect to the cluster, circumventing the load balancer. Depending on
your configuration this might be something you don't want or break completely.

Compression
~~~~~~~~~~~

When using capacity-constrained networks (low throughput), it may be handy to enable
compression. This is especially useful when doing bulk loads or inserting large
documents. This will configure compression.

.. code-block:: python

   from elasticsearch import Elasticsearch
   es = Elasticsearch(hosts, http_compress=True)

Compression is enabled by default when connecting to Elastic Cloud via ``cloud_id``.

Customization
-------------

Custom serializers
~~~~~~~~~~~~~~~~~~

By default, `JSONSerializer`_ is used to encode all outgoing requests.
However, you can implement your own custom serializer

.. code-block:: python

   from elasticsearch.serializer import JSONSerializer

   class SetEncoder(JSONSerializer):
       def default(self, obj):
           if isinstance(obj, set):
               return list(obj)
           if isinstance(obj, Something):
               return 'CustomSomethingRepresentation'
           return JSONSerializer.default(self, obj)

   es = Elasticsearch(serializer=SetEncoder())

.. _JSONSerializer: https://github.com/elastic/elasticsearch-py/blob/master/elasticsearch/serializer.py#L24


Elasticsearch-DSL
-----------------

For a more high level client library with more limited scope, have a look at
`elasticsearch-dsl`_ - a more pythonic library sitting on top of
``elasticsearch-py``.

`elasticsearch-dsl`_ provides a more convenient and idiomatic way to write and manipulate
`queries`_ by mirroring the terminology and structure of Elasticsearch JSON DSL
while exposing the whole range of the DSL from Python
either directly using defined classes or a queryset-like expressions.

It also provides an optional `persistence layer`_ for working with documents as
Python objects in an ORM-like fashion: defining mappings, retrieving and saving
documents, wrapping the document data in user-defined classes.

.. _elasticsearch-dsl: https://elasticsearch-dsl.readthedocs.io/
.. _queries: https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
.. _persistence layer: https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#doctype


Contents
--------

.. toctree::
   :maxdepth: 2

   api
   exceptions
   async
   connection
   transports
   helpers
   Release Notes <https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/release-notes.html>

License
-------

Copyright 2021 Elasticsearch B.V. Licensed under the Apache License, Version 2.0.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

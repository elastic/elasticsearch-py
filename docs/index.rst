Python Elasticsearch Client
===========================

Official low-level client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.

For a more high level client library with more limited scope, have a look at
`elasticsearch-dsl`_ - it is a more pythonic library sitting on top of
``elasticsearch-py``.

.. _elasticsearch-dsl: https://elasticsearch-dsl.readthedocs.io/

Compatibility
-------------

The library is compatible with all Elasticsearch versions since ``0.90.x`` but you
**have to use a matching major version**:

For **Elasticsearch 2.0** and later, use the major version 2 (``2.x.y``) of the
library.

For **Elasticsearch 1.0** and later, use the major version 1 (``1.x.y``) of the
library.

For **Elasticsearch 0.90.x**, use a version from ``0.4.x`` releases of the
library.

The recommended way to set your requirements in your `setup.py` or
`requirements.txt` is::

    # Elasticsearch 2.x
    elasticsearch>=2.0.0,<3.0.0

    # Elasticsearch 1.x
    elasticsearch>=1.0.0,<2.0.0

    # Elasticsearch 0.90.x
    elasticsearch<1.0.0

The development is happening on ``master`` and ``1.x`` branches, respectively.

Example Usage
-------------

::

    from datetime import datetime
    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    doc = {
        'author': 'kimchy', 
        'text': 'Elasticsearch: cool. bonsai cool.', 
        'timestamp': datetime.now(),
    }
    res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    print(res['created'])

    res = es.get(index="test-index", doc_type='tweet', id=1)
    print(res['_source'])

    es.indices.refresh(index="test-index")

    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


Features
--------

This client was designed as very thin wrapper around Elasticseach's REST API to
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

Some example configurations::

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
your application calls for more paralelism, use the ``maxsize`` parameter to
raise the limit::

    # allow up to 25 connections to each node
    es = Elasticsearch(["host1", "host2"], maxsize=25)

.. note::

    Since we use persistent connections throughout the client it means that the
    client doesn't tolerate ``fork`` very well. If your application calls for
    multiple processes make sure you create a fresh client after call to
    ``fork``. Note that Python's ``multiprocessing`` module uses ``fork`` to
    create new processes on POSIX systems.

SSL and Authentication
~~~~~~~~~~~~~~~~~~~~~~

You can configure the client to use ``SSL`` for connecting to your
elasticsearch cluster, including certificate verification and http auth::

    from elasticsearch import Elasticsearch

    # you can use RFC-1738 to specify the url
    es = Elasticsearch(['https://user:secret@localhost:443'])

    # ... or specify common parameters as kwargs

    # use certifi for CA certificates
    import certifi

    es = Elasticsearch(
        ['localhost', 'otherhost'],
        http_auth=('user', 'secret'),
        port=443,
        use_ssl=True,
        verify_certs=True,
        ca_certs=certifi.where(),
    )

    # SSL client authentication using client_cert and client_key

    es = Elasticsearch(
        ['localhost', 'otherhost'],
        http_auth=('user', 'secret'),
        port=443,
        use_ssl=True,
        verify_certs=True,
        ca_certs='/path/to/cacert.pem',
        client_cert='/path/to/client_cert.pem',
        client_key='/path/to/client_key.pem',
    )

..  warning::

    By default SSL certificates won't be verified, pass in
    ``verify_certs=True`` to make sure your certificates will get verified. The
    client doesn't ship with any CA certificates; easiest way to obtain the
    common set is by using the `certifi`_ package (as shown above).

See class :class:`~elasticsearch.Urllib3HttpConnection` for detailed
description of the options.

.. _certifi: http://certifi.io/

Logging
~~~~~~~

``elasticsearch-py`` uses the standard `logging library`_ from python to define
two loggers: ``elasticsearch`` and ``elasticsearch.trace``. ``elasticsearch``
is used by the client to log standard activity, depending on the log level.
``elasticsearch.trace`` can be used to log requests to the server in the form
of ``curl`` commands using pretty-printed json that can then be executed from
command line. If the trace logger has not been configured already it is set to
`propagate=False` so it needs to be activated separately.

.. _logging library: http://docs.python.org/3.3/library/logging.html

Environment considerations
--------------------------

When using the client there are several limitations of your environment that
could come into play.

When using an http load balancer you cannot use the :ref:`sniffing`
functionality - the cluster would supply the client with IP addresses to
directly connect to the cluster, circumventing the load balancer. Depending on
your configuration this might be something you don't want or break completely.

In some environments (notably on Google App Engine) your http requests might be
restricted so that ``GET`` requests won't accept body. In that case use the
``send_get_body_as`` parameter of :class:`~elasticsearch.Transport` to send all
bodies via post::

    from elasticsearch import Elasticsearch
    es = Elasticsearch(send_get_body_as='POST')

Running on AWS with IAM
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to use this client with IAM based authentication on AWS you can use
the `requests-aws4auth`_ package::

    from elasticsearch import Elasticsearch, RequestsHttpConnection
    from requests_aws4auth import AWS4Auth

    host = 'YOURHOST.us-east-1.es.amazonaws.com'
    awsauth = AWS4Auth(YOUR_ACCESS_KEY, YOUR_SECRET_KEY, REGION, 'es')

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    print(es.info())

.. _requests-aws4auth: https://pypi.python.org/pypi/requests-aws4auth

Contents
--------

.. toctree::
   :maxdepth: 2

   api
   exceptions
   connection
   transports
   helpers
   Changelog

License
-------

Copyright 2013 Elasticsearch

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


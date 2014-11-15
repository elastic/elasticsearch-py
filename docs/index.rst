Python Elasticsearch Client
===========================

Official low-level client for Elasticsearch. Its goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.

Compatibility
-------------

The library is compatible with both Elasticsearch 1.x and 0.90.x but you
**have to use a matching version**.

For **Elasticsearch 1.0** and later, use the major version 1 (``1.x.y``) of the
library.

For **Elasticsearch 0.90.x**, use a version from ``0.4.x`` releases of the
library.

The recommended way to set your requirements in your `setup.py` or
`requirements.txt` is::

    # Elasticsearch 1.0
    elasticsearch>=1.0.0,<2.0.0

    # Elasticsearch 0.90
    elasticsearch<1.0.0

The development is happening on ``master`` and ``0.4`` branches, respectively.

Example Usage
-------------

::

    from datetime import datetime
    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    doc = {
        'author': 'kimchy', 
        'text': 'Elasticsearch: cool. bonsai cool.', 
        'timestamp': datetime(2010, 10, 10, 10, 10, 10)
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
Python. We have created some :ref:`helpers` to help with this issue.

Persistent Connections
~~~~~~~~~~~~~~~~~~~~~~

``elasticsearch-py`` uses persistent connections inside of individual connection
pools (one per each configured or sniffed node). Out of the box you can choose
to use ``http``, ``thrift`` or an experimental ``memcached`` protocol to
communicate with the elasticsearch nodes. See :ref:`transports` for more
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
    es = Elasticsearch(["seed1", "seed2"], sniff_on_start=True, sniff_on_connection_fail=True, sniffer_timeout=60)


Logging
~~~~~~~

``elasticsearch-py`` uses the standard `logging library`_ from python to define
two loggers: ``elasticsearch`` and ``elasticsearch.trace``. ``elasticsearch``
is used by the client to log standard activity, depending on the log level.
``elasticsearch.trace`` can be used to log requests to the server in the form
of ``curl`` commands using pretty-printed json that can then be executed from
command line. The trace logger doesn't inherit from the base one - it needs to
be activated separately.

.. _logging library: http://docs.python.org/3.3/library/logging.html

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


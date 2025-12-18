.. raw:: html

   <img align="right" width="auto" height="auto" src="https://www.elastic.co/static-res/images/elastic-logo-200.png">


Elasticsearch Python Client
===========================

*The official Python client for Elasticsearch.*


Features
--------

* Translating basic Python data types to and from JSON
* Configurable automatic discovery of cluster nodes
* Persistent connections
* Load balancing (with pluggable selection strategy) across available nodes
* Failed connection penalization (time based - failed connections won't be
  retried until a timeout is reached)
* Support for TLS and HTTP authentication
* Thread safety across requests
* Pluggable architecture
* Helper functions for idiomatically using APIs together


Installation
------------

Install the ``elasticsearch`` package with `pip
<https://pypi.org/project/elasticsearch>`_::

    $ python -m pip install elasticsearch

If your application uses async/await in Python you can install with
the ``async`` extra::

    $ python -m pip install elasticsearch[async]

Read more about `how to use asyncio with this project <https://elasticsearch-py.readthedocs.io/en/master/async.html>`_.


Compatibility
-------------

Language clients are forward compatible; meaning that clients support communicating
with greater or equal minor versions of Elasticsearch. Elasticsearch language clients
are only backwards compatible with default distributions and without guarantees made.

If you have a need to have multiple versions installed at the same time older
versions are also released as ``elasticsearch2`` and ``elasticsearch5``.


Documentation
-------------

Documentation for the client is `available on elastic.co`_ and `Read the Docs`_.

.. _available on elastic.co: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
.. _Read the Docs: https://elasticsearch-py.readthedocs.io

Quick Start
-----------

.. code-block:: python

    # Import the client from the 'elasticsearch' module
    >>> from elasticsearch import Elasticsearch
    
    # Instantiate a client instance
    >>> client = Elasticsearch("http://localhost:9200")
    
    # Call an API, in this example `info()`
    >>> resp = client.info()

    # View the result
    >>> resp
    {
      "name" : "instance-name",
      "cluster_name" : "cluster-name",
      "cluster_uuid" : "cluster-uuid",
      "version" : {
        "number" : "7.14.0",
        ...
      },
      "tagline" : "You know, for Search"
    }


You can read more about `configuring the client`_ in the documentation.

.. _configuring the client: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/connecting.html


Local Development
=================

Install ENV
-----------

After cloning the code, create a development environment:

.. code:: bash

   conda create -n es7-py python=3.10

Install Development Dependencies
--------------------------------

.. code:: bash

   pip install -r dev-requirements.txt

Run Unit Tests
--------------

Start the Elasticsearch dependency before running unit tests:

.. code:: bash

   docker run --rm \
     --name elasticsearch-7.16 \
     -p 9200:9200 \
     -e "discovery.type=single-node" \
     -e "xpack.security.enabled=false" \
     -e "ES_JAVA_OPTS=-Xms1024m -Xmx1024m" \
     docker.elastic.co/elasticsearch/elasticsearch:7.16.0

Run unit tests using pytest:

.. code:: bash

   python -m pytest

Run unit tests across multiple Python environments using nox:

.. code:: bash

   # Example: Run tests in Python 3.11 environment (supports py 3.10 ~ 3.14)
   python -m pip install 'nox[pbs]'
   nox -s test-3.11

Code Lint
=========

::

   python -m pip install 'nox[pbs]'
   nox -s format

Build and Compile
-----------------

After completing local development, use pre-compiled builds:

::

   ./.ci/make.sh assemble 7.x-SNAPSHOT

On successful compilation, you can find ``.tar.gz`` and ``.whl`` files
in ``.ci/output/``.

Once adjustments are confirmed, update the version number ``VERSION`` in
``elasticsearch/_version.py`` (requires a git commit) and run below to complete the new version package build.:

::

   ./.ci/make.sh assemble ${VERSION}




License
-------

Copyright 2021 Elasticsearch B.V. Licensed under the Apache License, Version 2.0.

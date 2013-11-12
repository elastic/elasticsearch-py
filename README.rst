Python Elasticsearch Client
===========================

Official low-level client for Elasticsearch. It's goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.

Installation
------------

Install the `elasticsearch` package with `pip
<https://pypi.python.org/pypi/elasticsearch/0.4.3>`_::

    pip install elasticsearch


Example use
-----------

Simple use-case::

    >>> from datetime import datetime
    >>> from elasticsearch import Elasticsearch

    # by default we connect to localhost:9200
    >>> es = Elasticsearch()

    # datetimes will be serialized
    >>> es.index(index="my-index", doc_type="test-type", id=42, body={"any": "data", "timestamp": datetime.now()})
    {u'_id': u'42', u'_index': u'my-index', u'_type': u'test-type', u'_version': 1, u'ok': True}

    # but not deserialized
    >>> es.get(index="my-index", doc_type="test-type", id=42)['_source']
    {u'any': u'data', u'timestamp': u'2013-05-12T19:45:31.804229'}

`Full documentation`_.

.. _Full documentation: http://elasticsearch-py.rtfd.org/


Features
--------

The client's features include:

 * translating basic Python data types to and from json (datetimes are not
   decoded for performance reasons)
 * configurable automatic discovery of cluster nodes
 * persistent connections
 * load balancing (with pluggable selection strategy) across all availible nodes
 * failed connection penalization (time based - failed connections won't be
   retried until a timeout is reached)
 * thread safety
 * pluggable architecture


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

Build status
------------

.. image:: https://secure.travis-ci.org/elasticsearch/elasticsearch-py.png
   :target: http://travis-ci.org/#!/elasticsearch/elasticsearch-py

.. image:: https://coveralls.io/repos/elasticsearch/elasticsearch-py/badge.png?branch=master
   :target: https://coveralls.io/r/elasticsearch/elasticsearch-py

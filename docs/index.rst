Python Elasticsearch Client
===========================

Official low-level client for Elasticsearch. It's goal is to provide common
ground for all Elasticsearch-related code in Python; because of this it tries
to be opinion-free and very extendable.


Example Usage
-------------


.. testsetup::

    from datetime import datetime
    from elasticsearch import Elasticsearch
    es = Elasticsearch()
    es.delete_index("test_index", ignore_missing=True)

.. testcode::

    from elasticsearch import Elasticsearch
    es = Elasticsearch()

    doc = {
        'author': 'kimchy', 
        'text': 'Elasticsearch: cool. bonsai cool.', 
        'timestamp': datetime(2010, 10, 10, 10, 10, 10)
    }
    res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    print(res['ok'])

    res = es.get(index="test-index", doc_type='tweet', id=1)
    print(res['_source'])

    es.indices.refresh(index="test-index")

    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

.. testoutput::
    :hide:

    True
    {u'text': u'Elasticsearch: cool. bonsai cool.', u'author': u'kimchy', u'timestamp': u'2010-10-10T10:10:10'}
    Got 1 Hits:
    2010-10-10T10:10:10 kimchy: Elasticsearch: cool. bonsai cool.

Features
--------

Extendability
~~~~~~~~~~~~~

Configurable connections and load balancing (see :ref:`connection_api`)::
 * persistent connections
 * configurable load balancing strategy
 * different protocols and connection classes
 * ...


Sniffing
~~~~~~~~

The client can be configured to inspect the cluster state to get a list of
nodes upon startup, periodically and/or on failure. See
:class:`~elasticsearch.Transport` parameters for details.
    
Contents
--------

.. toctree::
   :maxdepth: 2

   api
   connection
   transports
   helpers

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


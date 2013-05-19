API Documentation
=================

.. py:module:: elasticsearch

.. autoclass:: Elasticsearch
   :members:

.. autoclass:: Transport(hosts, connection_class=RequestsHttpConnection, connection_pool_class=ConnectionPool, nodes_to_host_callback=construct_hosts_list, sniff_on_start=False, sniff_after_requests=None, sniff_on_connection_fail=False, serializer=JSONSerializer(), max_retries=3, ** kwargs)
   :members:

.. autoclass:: ConnectionPool(connections, dead_timeout=60, selector_class=RoundRobinSelector, randomize_hosts=True, ** kwargs)
   :members:

.. autoclass:: Connection
   :members:


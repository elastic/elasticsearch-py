.. _api:

Elasticsearch API Reference
===========================

All the API calls map the raw REST API as closely as possible, including the
distinction between required and optional arguments to the calls. Keyword
arguments are required for all calls.

.. note::

   Some API parameters in Elasticsearch are reserved keywords in Python.
   For example the ``from`` query parameter for pagination would be
   aliased as ``from_``.

.. toctree::
   :maxdepth: 1

   rest-apis/elasticsearch
   rest-apis/autoscaling
   rest-apis/cat
   rest-apis/ccr
   rest-apis/cluster
   rest-apis/dangling-indices
   rest-apis/enrich-policies
   rest-apis/eql
   rest-apis/fleet
   rest-apis/graph-explore
   rest-apis/index-lifecycle-management
   rest-apis/indices
   rest-apis/ingest-pipelines
   rest-apis/license
   rest-apis/migration
   rest-apis/ml
   rest-apis/monitoring
   rest-apis/nodes
   rest-apis/query-rules
   rest-apis/rollup-indices
   rest-apis/search-application
   rest-apis/searchable-snapshots
   rest-apis/security
   rest-apis/shutdown
   rest-apis/snapshot-lifecycle-management
   rest-apis/snapshots
   rest-apis/snapshottable-features
   rest-apis/sql
   rest-apis/synonyms
   rest-apis/tls-ssl
   rest-apis/tasks
   rest-apis/text-structure
   rest-apis/transforms
   rest-apis/watcher
   rest-apis/x-pack

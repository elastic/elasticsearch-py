.. _changelog:

Changelog
=========

2.4.1 (2017-01-03)
------------------
 * don't warn on empty data returned from server
 * Propagate request_timeout to scroll calls

2.4.0 (2016-08-17)
------------------

 * ``ping`` now ignores all ``TransportError`` exceptions and just returns
   ``False``
 * expose ``scroll_id`` on ``ScanError``
 * increase default size for ``scan`` helper to 1000

Internal:

 * changed ``Transport.perform_request`` to just return the body, not status as well.

2.3.0 (2016-02-29)
------------------

 * added ``client_key`` argument to configure client certificates
 * debug logging now includes response body even for failed requests

2.2.0 (2016-01-05)
------------------

Due to change in json encoding the client will no longer mask issues with
encoding - if you work with non-ascii data in python 2 you must use the
``unicode`` type or have proper encoding set in your environment.

 * adding additional options for ssh - ``ssl_assert_hostname`` and
   ``ssl_assert_fingerprint`` to the default connection class
 * fix sniffing

2.1.0 (2015-10-19)
------------------

  * move multiprocessing import inside parallel bulk for Google App Engine

2.0.0 (2015-10-14)
------------------

 * Elasticsearch 2.0 compatibility release

1.8.0 (2015-10-14)
------------------

 * removed thrift and memcached connections, if you wish to continue using
   those, extract the classes and use them separately.
 * added a new, parallel version of the bulk helper using thread pools
 * In helpers, removed ``bulk_index`` as an alias for ``bulk``. Use ``bulk``
   instead.

1.7.0 (2015-09-21)
------------------

 * elasticsearch 2.0 compatibility
 * thrift now deprecated, to be removed in future version
 * make sure urllib3 always uses keep-alive

1.6.0 (2015-06-10)
------------------

 * Add ``indices.flush_synced`` API
 * ``helpers.reindex`` now supports reindexing parent/child documents

1.5.0 (2015-05-18)
------------------

 * Add support for ``query_cache`` parameter when searching
 * helpers have been made more secure by changing defaults to raise an
   exception on errors
 * removed deprecated options ``replication`` and the deprecated benchmark api.
 * Added ``AddonClient`` class to allow for extending the client from outside

1.4.0 (2015-02-11)
------------------

 * Using insecure SSL configuration (``verify_cert=False``) raises a warning
 * ``reindex`` accepts a ``query`` parameter
 * enable ``reindex`` helper to accept any kwargs for underlying ``bulk`` and
   ``scan`` calls
 * when doing an initial sniff (via ``sniff_on_start``) ignore special sniff timeout
 * option to treat ``TransportError`` as normal failure in ``bulk`` helpers
 * fixed an issue with sniffing when only a single host was passed in

1.3.0 (2014-12-31)
------------------

 * Timeout now doesn't trigger a retry by default (can be overriden by setting
   ``retry_on_timeout=True``)
 * Introduced new parameter ``retry_on_status`` (defaulting to ``(503, 504,
   )``) controls which http status code should lead to a retry.
 * Implemented url parsing according to RFC-1738
 * Added support for proper SSL certificate handling
 * Required parameters are now checked for non-empty values
 * ConnectionPool now checks if any connections were defined
 * DummyConnectionPool introduced when no load balancing is needed (only one
   connection defined)
 * Fixed a race condition in ConnectionPool

1.2.0 (2014-08-03)
------------------

Compatibility with newest (1.3) Elasticsearch APIs.

 * Filter out master-only nodes when sniffing
 * Improved docs and error messages

1.1.1 (2014-07-04)
------------------

Bugfix release fixing escaping issues with ``request_timeout``.

1.1.0 (2014-07-02)
------------------

Compatibility with newest Elasticsearch APIs.

 * Test helpers - ``ElasticsearchTestCase`` and ``get_test_client`` for use in your
   tests
 * Python 3.2 compatibility
 * Use ``simplejson`` if installed instead of stdlib json library
 * Introducing a global ``request_timeout`` parameter for per-call timeout
 * Bug fixes

1.0.0 (2014-02-11)
------------------

Elasticsearch 1.0 compatibility. See 0.4.X releases (and 0.4 branch) for code
compatible with 0.90 elasticsearch.

 * major breaking change - compatible with 1.0 elasticsearch releases only!
 * Add an option to change the timeout used for sniff requests (``sniff_timeout``).
 * empty responses from the server are now returned as empty strings instead of None
 * ``get_alias`` now has ``name`` as another optional parameter due to issue #4539
   in es repo. Note that the order of params have changed so if you are not
   using keyword arguments this is a breaking change.

0.4.4 (2013-12-23)
------------------

 * ``helpers.bulk_index`` renamed to ``helpers.bulk`` (alias put in place for
   backwards compatibility, to be removed in future versions)
 * Added ``helpers.streaming_bulk`` to consume an iterator and yield results per
   operation
 * ``helpers.bulk`` and ``helpers.streaming_bulk`` are no longer limitted to just
   index operations.
 * unicode body (for ``incices.analyze`` for example) is now handled correctly
 * changed ``perform_request`` on ``Connection`` classes to return headers as well.
   This is a backwards incompatible change for people who have developed their own
   connection class.
 * changed deserialization mechanics. Users who provided their own serializer
   that didn't extend ``JSONSerializer`` need to specify a ``mimetype`` class
   attribute.
 * minor bug fixes

0.4.3 (2013-10-22)
------------------

 * Fixes to ``helpers.bulk_index``, better error handling
 * More benevolent ``hosts`` argument parsing for ``Elasticsearch``
 * ``requests`` no longer required (nor recommended) for install

0.4.2 (2013-10-08)
------------------
 
 * ``ignore`` param acceted by all APIs
 * Fixes to ``helpers.bulk_index``

0.4.1 (2013-09-24)
------------------

Initial release.

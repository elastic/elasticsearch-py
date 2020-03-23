.. _changelog:

Changelog
=========

7.6.0 (2020-03-19)
------------------
  * Added support for ES 7.6 APIs
  * Added support for `X-Opaque-Id`_ to identify long-running tasks
  * Added support for HTTP compression to ``RequestsHttpConnection``
  * Updated default setting of ``http_compress`` when using ``cloud_id`` to ``True``
  * Updated default setting of ``sniffing`` when using ``cloud_id`` to ``False``
  * Updated default port to ``443`` if ``cloud_id`` and no other port is defined
    on the client or within ``cloud_id``
  * Updated ``GET`` HTTP requests that contain a body to ``POST`` where
    the API allows this to fix proxies rejecting these requests.
  * Fix regression of ``client.cluster.state()`` where the default ``metric``
    should be set to ``"_all"`` if an index is given (See `#1143`_)
  * Fix regression of ``client.tasks.get()`` without a ``task_id``
    having similar functionality to ``client.tasks.list()`` This will
    be removed in ``v8.0`` of ``elasticsearch-py`` (See `#1157`_)

  .. _X-Opaque-Id: https://www.elastic.co/guide/en/elasticsearch/reference/current/tasks.html#_identifying_running_tasks
  .. _#1143: https://github.com/elastic/elasticsearch-py/pull/1143
  .. _#1157: https://github.com/elastic/elasticsearch-py/pull/1157

7.5.1 (2020-01-19)
------------------
  * ``7.5.0`` tag was not released so retagging

7.5.0
-----
  * All API is now auto generated
  * deprecated the ``.xpack`` namespace
  * Update client to support ES 7.5 APIs

7.1.0 (2019-11-14)
------------------
  * Fix sniffing with ``http.publish_host``
  * Fix ``request_timeout`` for ``indices`` APIs
  * Allow access to ``x-pack`` features without ``xpack`` namespace
  * Fix mark dead

7.0.5 (2019-10-01)
------------------
  * Fix ``verify_certs=False``

7.0.4 (2019-08-22)
------------------
  * Fix wheel distribution

7.0.3 (2019-08-21)
------------------
  * remove sleep in retries
  * pass ``scroll_id`` through body in ``scroll``
  * add ``user-agent``

7.0.2 (2019-05-29)
------------------
  * Add connection parameter for Elastic Cloud cloud_id.
  * ML client uses client object for _bulk_body requests

7.0.1 (2019-05-19)
------------------
  * Use black to format the code.
  * Update the test matrix to only use current pythons and 7.x ES
  * Blocking pool must fit thread_count
  * Update client to support missing ES 7 API's and query params.

7.0.0 (2019-04-11)
------------------
  * Removed deprecated option ``update_all_types``.
  * Using insecure SSL configuration (``verify_cert=False``) raises a warning, this can
    be not showed with ``ssl_show_warn=False``
  * Add support for 7.x api's in Elasticsearch both xpack and oss flavors

6.3.0 (2018-06-20)
------------------

  * Add an exponential wait on delays
  * Fix issues with dependencies
  * Adding X-pack Docs
  * Adding forecast to x-pack ML client

6.2.0 (2018-03-20)
------------------

  * cleanup for SSL Context
  * Add X-Pack clients to -py
  * Adding Gzip support for capacity constrained networks
  * ``_routing`` in bulk action has been deprecated in ES. Introduces a breaking change
    if you use ``routing`` as a field in your documents.

6.1.1 (2018-01-05)
------------------

 * Updates to SSLContext logic to make it easier to use and have saner defaults.
 * Doc updates

6.1.0 (2018-01-05)
------------------

  * bad release

6.0.0 (2017-11-14)
------------------

 * compatibility with Elasticsearch 6.0.0

5.5.0 (2017-11-10)
------------------

 * ``streaming_bulk`` helper now supports retries with incremental backoff
 * ``scan`` helper properly checks for successful shards instead of just
   checking ``failed``
 * compatible release with elasticsearch ``5.6.4``
 * fix handling of UTF-8 surrogates

5.4.0 (2017-05-18)
------------------

 * ``bulk`` helpers now extract ``pipeline`` parameter from the action
   dictionary.

5.3.0 (2017-03-30)
------------------

Compatibility with elasticsearch 5.3

5.2.0 (2017-02-12)
------------------

The client now automatically sends ``Content-Type`` http header set to
``application/json``. If you are explicitly passing in other encoding than
``json`` you need to set the header manually.

5.1.0 (2017-01-11)
------------------

 * Fixed sniffing

5.0.1 (2016-11-02)
------------------

Fixed performance regression in ``scan`` helper

5.0.0 (2016-10-19)
------------------

Version compatible with elasticsearch 5.0

 * when using SSL certificate validation is now on by default. Install
   ``certifi`` or supply root certificate bundle.
 * ``elasticsearch.trace`` logger now also logs failed requests, signature of
   internal logging method ``log_request_fail`` has changed, all custom
   connection classes need to be updated
 * added ``headers`` arg to connections to support custom http headers
 * passing in a keyword parameter with ``None`` as value will cause that param
   to be ignored

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
 * ``helpers.bulk`` and ``helpers.streaming_bulk`` are no longer limited to just
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

 * ``ignore`` param accepted by all APIs
 * Fixes to ``helpers.bulk_index``

0.4.1 (2013-09-24)
------------------

Initial release.

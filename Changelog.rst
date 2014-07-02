.. _changelog:

Changelog
=========

1.1.0 (2014-07-02)
------------------

Compatibility with newest Elasticsearch APIs.

 * Test helpers - `ElasticsearchTestCase` and `get_test_client` for use in your
   tests
 * Python 3.2 compatibility
 * Use ``simplejson`` if installed instead of stdlib json library
 * Introducing a global `request_timeout` parameter for per-call timeout
 * Bug fixes

1.0.0 (2014-02-11)
------------------

Elasticsearch 1.0 compatibility. See 0.4.X releases (and 0.4 branch) for code
compatible with 0.90 elasticsearch.

 * major breaking change - compatible with 1.0 elasticsearch releases only!
 * Add an option to change the timeout used for sniff requests (`sniff_timeout`).
 * empty responses from the server are now returned as empty strings instead of None
 * `get_alias` now has `name` as another optional parameter due to issue #4539
   in es repo. Note that the order of params have changed so if you are not
   using keyword arguments this is a breaking change.

0.4.4 (2013-12-23)
------------------

 * `helpers.bulk_index` renamed to `helpers.bulk` (alias put in place for
   backwards compatibility, to be removed in future versions)
 * Added `helpers.streaming_bulk` to consume an iterator and yield results per
   operation
 * `helpers.bulk` and `helpers.streaming_bulk` are no longer limitted to just
   index operations.
 * unicode body (for `incices.analyze` for example) is now handled correctly
 * changed `perform_request` on `Connection` classes to return headers as well.
   This is a backwards incompatible change for people who have developed their own
   connection class.
 * changed deserialization mechanics. Users who provided their own serializer
   that didn't extend `JSONSerializer` need to specify a `mimetype` class
   attribute.
 * minor bug fixes

0.4.3 (2013-10-22)
------------------

 * Fixes to `helpers.bulk_index`, better error handling
 * More benevolent `hosts` argument parsing for `Elasticsearch`
 * `requests` no longer required (nor recommended) for install

0.4.2 (2013-10-08)
------------------
 
 * `ignore` param acceted by all APIs
 * Fixes to `helpers.bulk_index`

0.4.1 (2013-09-24)
------------------

Initial release.

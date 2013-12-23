.. _changelog:

Changelog
=========

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

from unittest import TestCase

from elasticsearch.client import _normalize_hosts

class TestNormalizeHosts(TestCase):
    def test_none_uses_defaults(self):
        self.assertEquals([{}], _normalize_hosts(None))

    def test_strings_are_used_as_hostnames(self):
        self.assertEquals([{"host": "elasticsearch.org"}], _normalize_hosts(["elasticsearch.org"]))

    def test_strings_are_parsed_for_port(self):
        self.assertEquals(
            [{"host": "elasticsearch.org", "port": 42}, {"host": "user:secret@elasticsearch.com"}],
            _normalize_hosts(["elasticsearch.org:42", u"user:secret@elasticsearch.com"])
        )

    def test_dicts_are_left_unchanged(self):
        self.assertEquals([{"host": "local", "extra": 123}], _normalize_hosts([{"host": "local", "extra": 123}]))

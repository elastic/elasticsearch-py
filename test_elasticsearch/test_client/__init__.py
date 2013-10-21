from mock import patch

from elasticsearch.client import _normalize_hosts

from ..test_cases import TestCase, ElasticsearchTestCase

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

    @patch('elasticsearch.client.logger')
    def test_schema_is_stripped_out(self, logger):
        self.assertEquals(
            [{"host": "elasticsearch.org", "port": 9200}],
            _normalize_hosts(["http://elasticsearch.org:9200/"])
        )
        # schema triggers a warning
        self.assertEquals(1, logger.warn.call_count)

    def test_single_string_is_wrapped_in_list(self):
        self.assertEquals(
            [{"host": "elasticsearch.org"}],
            _normalize_hosts("elasticsearch.org")
        )


class TestClient(ElasticsearchTestCase):
    def test_from_in_search(self):
        self.client.search(index='i', doc_type='t', from_=10)
        calls = self.assert_url_called('GET', '/i/t/_search')
        self.assertEquals([({'from': '10'}, None)], calls)

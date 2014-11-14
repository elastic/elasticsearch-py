from __future__ import unicode_literals

from elasticsearch.client import _normalize_hosts, Elasticsearch

from ..test_cases import TestCase, ElasticsearchTestCase

class TestNormalizeHosts(TestCase):
    def test_none_uses_defaults(self):
        self.assertEquals([{}], _normalize_hosts(None))

    def test_strings_are_used_as_hostnames(self):
        self.assertEquals([{"host": "elasticsearch.org"}], _normalize_hosts(["elasticsearch.org"]))

    def test_strings_are_parsed_for_port_and_user(self):
        self.assertEquals(
            [{"host": "elasticsearch.org", "port": 42}, {"host": "elasticsearch.com", "http_auth": "user:secret"}],
            _normalize_hosts(["elasticsearch.org:42", "user:secret@elasticsearch.com"])
        )

    def test_strings_are_parsed_for_scheme(self):
        self.assertEquals(
            [
                {"host": "elasticsearch.org", "port": 42, "use_ssl": True, 'scheme': 'http'},
                {"host": "elasticsearch.com", "http_auth": "user:secret", "use_ssl": True, "port": 443, 'scheme': 'http'}
            ],
            _normalize_hosts(["https://elasticsearch.org:42", "https://user:secret@elasticsearch.com"])
        )

    def test_dicts_are_left_unchanged(self):
        self.assertEquals([{"host": "local", "extra": 123}], _normalize_hosts([{"host": "local", "extra": 123}]))

    def test_single_string_is_wrapped_in_list(self):
        self.assertEquals(
            [{"host": "elasticsearch.org"}],
            _normalize_hosts("elasticsearch.org")
        )


class TestClient(ElasticsearchTestCase):
    def test_request_timeout_is_passed_through_unescaped(self):
        self.client.ping(request_timeout=.1)
        calls = self.assert_url_called('HEAD', '/')
        self.assertEquals([({'request_timeout': .1}, None)], calls)

    def test_from_in_search(self):
        self.client.search(index='i', doc_type='t', from_=10)
        calls = self.assert_url_called('GET', '/i/t/_search')
        self.assertEquals([({'from': '10'}, None)], calls)

    def test_repr_contains_hosts(self):
        self.assertEquals('<Elasticsearch([{}])>', repr(self.client))

    def test_repr_contains_hosts_passed_in(self):
        self.assertIn("es.org", repr(Elasticsearch(['es.org:123'])))

    def test_repr_truncates_host_to_10(self):
        hosts = [{"host": "es" + str(i)} for i in range(20)]
        self.assertNotIn("es5", repr(Elasticsearch(hosts)))

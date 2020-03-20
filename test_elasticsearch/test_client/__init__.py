from __future__ import unicode_literals

from elasticsearch.client import _normalize_hosts, Elasticsearch

from ..test_cases import TestCase, ElasticsearchTestCase


class TestNormalizeHosts(TestCase):
    def test_none_uses_defaults(self):
        self.assertEquals([{}], _normalize_hosts(None))

    def test_strings_are_used_as_hostnames(self):
        self.assertEquals([{"host": "elastic.co"}], _normalize_hosts(["elastic.co"]))

    def test_strings_are_parsed_for_port_and_user(self):
        self.assertEquals(
            [
                {"host": "elastic.co", "port": 42},
                {"host": "elastic.co", "http_auth": "user:secre]"},
            ],
            _normalize_hosts(["elastic.co:42", "user:secre%5D@elastic.co"]),
        )

    def test_strings_are_parsed_for_scheme(self):
        self.assertEquals(
            [
                {"host": "elastic.co", "port": 42, "use_ssl": True},
                {
                    "host": "elastic.co",
                    "http_auth": "user:secret",
                    "use_ssl": True,
                    "port": 443,
                    "url_prefix": "/prefix",
                },
            ],
            _normalize_hosts(
                ["https://elastic.co:42", "https://user:secret@elastic.co/prefix"]
            ),
        )

    def test_dicts_are_left_unchanged(self):
        self.assertEquals(
            [{"host": "local", "extra": 123}],
            _normalize_hosts([{"host": "local", "extra": 123}]),
        )

    def test_single_string_is_wrapped_in_list(self):
        self.assertEquals([{"host": "elastic.co"}], _normalize_hosts("elastic.co"))


class TestClient(ElasticsearchTestCase):
    def test_request_timeout_is_passed_through_unescaped(self):
        self.client.ping(request_timeout=0.1)
        calls = self.assert_url_called("HEAD", "/")
        self.assertEquals([({"request_timeout": 0.1}, {}, None)], calls)

    def test_params_is_copied_when(self):
        rt = object()
        params = dict(request_timeout=rt)
        self.client.ping(params=params)
        self.client.ping(params=params)
        calls = self.assert_url_called("HEAD", "/", 2)
        self.assertEquals(
            [({"request_timeout": rt}, {}, None), ({"request_timeout": rt}, {}, None)],
            calls,
        )
        self.assertFalse(calls[0][0] is calls[1][0])

    def test_headers_is_copied_when(self):
        hv = "value"
        headers = dict(Authentication=hv)
        self.client.ping(headers=headers)
        self.client.ping(headers=headers)
        calls = self.assert_url_called("HEAD", "/", 2)
        self.assertEquals(
            [({}, {"authentication": hv}, None), ({}, {"authentication": hv}, None)],
            calls,
        )
        self.assertFalse(calls[0][0] is calls[1][0])

    def test_from_in_search(self):
        self.client.search(index="i", from_=10)
        calls = self.assert_url_called("POST", "/i/_search")
        self.assertEquals([({"from": "10"}, {}, None)], calls)

    def test_repr_contains_hosts(self):
        self.assertEquals("<Elasticsearch([{}])>", repr(self.client))

    def test_repr_subclass(self):
        class OtherElasticsearch(Elasticsearch):
            pass

        self.assertEqual("<OtherElasticsearch([{}])>", repr(OtherElasticsearch()))

    def test_repr_contains_hosts_passed_in(self):
        self.assertIn("es.org", repr(Elasticsearch(["es.org:123"])))

    def test_repr_truncates_host_to_5(self):
        hosts = [{"host": "es" + str(i)} for i in range(10)]
        es = Elasticsearch(hosts)
        self.assertNotIn("es5", repr(es))
        self.assertIn("...", repr(es))

    def test_index_uses_post_if_id_is_empty(self):
        self.client.index(index="my-index", id="", body={})

        self.assert_url_called("POST", "/my-index/_doc")

    def test_index_uses_put_if_id_is_not_empty(self):
        self.client.index(index="my-index", id=0, body={})

        self.assert_url_called("PUT", "/my-index/_doc/0")

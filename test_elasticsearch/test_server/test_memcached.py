# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, MemcachedConnection, NotFoundError

from elasticsearch.transport import ADDRESS_RE

from . import ElasticTestCase

from unittest import SkipTest

class TestMemcachedConnection(ElasticTestCase):
    def setUp(self):
        super(TestMemcachedConnection, self).setUp()
        nodes = self.client.cluster.node_info()
        for node_id, node_info in nodes["nodes"].items():
            if 'memcached_address' in node_info:
                connection_info = ADDRESS_RE.search(node_info['memcached_address']).groupdict()
                self.mc_client = Elasticsearch(
                    [connection_info],
                    connection_class=MemcachedConnection
                )
                break
        else:
            raise SkipTest("No memcached plugin.")

    def test_index(self):
        self.mc_client.index("test_index", "test_type", {"answer": 42}, id=1)
        self.assertTrue(self.client.exists("test_index", doc_type="test_type", id=1))

    def test_get(self):
        self.client.index("test_index", "test_type", {"answer": 42}, id=1)
        self.assertEquals({"answer": 42}, self.mc_client.get("test_index", doc_type="test_type", id=1)["_source"])

    def test_unicode(self):
        self.mc_client.index("test_index", "test_type", {"answer": u"你好"}, id=u"你好")
        self.assertEquals({"answer": u"你好"}, self.mc_client.get("test_index", doc_type="test_type", id=u"你好")["_source"])

    def test_missing(self):
        self.assertRaises(NotFoundError, self.mc_client.get, "test_index", doc_type="test_type", id=42)

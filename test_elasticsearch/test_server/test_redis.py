# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch, RedisConnection, NotFoundError

from elasticsearch.transport import ADDRESS_RE

from . import ElasticTestCase
from ..test_cases import SkipTest

class TestRedisConnection(ElasticTestCase):
    def setUp(self):
        try:
            import redis
        except ImportError:
            raise SkipTest("No redis-py.")
        super(TestRedisConnection, self).setUp()
        nodes = self.client.nodes.info()
        for node_id, node_info in nodes["nodes"].items():
            if 'redis_address' in node_info:
                connection_info = ADDRESS_RE.search(node_info['redis_address']).groupdict()
                self.redis_client = Elasticsearch(
                    [connection_info],
                    connection_class=RedisConnection
                )
                break
        else:
            raise SkipTest("No redis plugin.")

    def test_index(self):
        self.redis_client.index("test_index", "test_type", {"answer": 42}, id=1)
        self.assertTrue(self.client.exists("test_index", doc_type="test_type", id=1))

    def test_get(self):
        self.client.index("test_index", "test_type", {"answer": 42}, id=1)
        self.assertEquals({"answer": 42}, self.redis_client.get("test_index", doc_type="test_type", id=1)["_source"])

    def test_unicode(self):
        self.redis_client.index("test_index", "test_type", {"answer_str": u"你好"}, id=u"你好")
        self.assertEquals({"answer_str": u"你好"}, self.redis_client.get("test_index", doc_type="test_type", id=u"你好")["_source"])

    def test_missing(self):
        self.assertEquals(False, self.redis_client.exists("test_index", doc_type="test_type", id=42))



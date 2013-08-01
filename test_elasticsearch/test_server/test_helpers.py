from elasticsearch import helpers

from . import ElasticTestCase

class TestBulkIndex(ElasticTestCase):
    def test_all_documents_get_inserted(self):
        docs = [{"answer": x} for x in range(100)]
        success, failed = helpers.bulk_index(self.client, docs, index='test-index', doc_type='answers', refresh=True)

        self.assertEquals(100, len(success))
        self.assertFalse(failed)
        self.assertEquals(100, self.client.count(index='test-index', doc_type='answers')['count'])

class TestScan(ElasticTestCase):
    def test_all_documents_are_read(self):
        bulk = []
        for x in range(100):
            bulk.append({"index": {"_index": "test_index", "_type": "answers", "_id": x}})
            bulk.append({"answer": x, "correct": x == 42})
        self.client.bulk(bulk, refresh=True)

        docs = list(helpers.scan(self.client, index="test_index", doc_type="answers", size=2))

        self.assertEquals(100, len(docs))
        self.assertEquals(set(map(str, range(100))), set(d['_id'] for d in docs))
        self.assertEquals(set(range(100)), set(d['_source']['answer'] for d in docs))

class TestReindex(ElasticTestCase):
    def test_all_documents_get_moved(self):
        bulk = []
        for x in range(100):
            bulk.append({"index": {"_index": "test_index", "_type": "answers" if x % 2 == 0 else "questions", "_id": x}})
            bulk.append({"answer": x, "correct": x == 42})
        self.client.bulk(bulk, refresh=True)

        helpers.reindex(self.client, "test_index", "prod_index")
        self.client.indices.refresh()

        self.assertTrue(self.client.indices.exists("prod_index"))
        self.assertTrue(self.client.indices.exists_type("prod_index", "answers"))
        self.assertTrue(self.client.indices.exists_type("prod_index", "questions"))
        self.assertEquals(100, self.client.count(index='prod_index')['count'])


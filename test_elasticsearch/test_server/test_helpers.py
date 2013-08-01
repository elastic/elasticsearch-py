from elasticsearch import helpers

from . import ElasticTestCase

class TestBulkIndex(ElasticTestCase):
    def test_all_documents_get_inserted(self):
        docs = [{"answer": x} for x in range(100)]
        success, failed = helpers.bulk_index(self.client, docs, index='test-index', doc_type='answers', refresh=True)

        self.assertEquals(len(success), len(docs))
        self.assertFalse(failed)
        self.assertEquals(len(docs), self.client.count(index='test-index', doc_type='answers')['count'])


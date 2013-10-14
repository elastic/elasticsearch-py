from elasticsearch import helpers

from . import ElasticTestCase

class TestBulkIndex(ElasticTestCase):
    def test_all_documents_get_inserted(self):
        docs = [{"answer": x, '_id': x} for x in range(100)]
        success, failed = helpers.bulk_index(self.client, docs, index='test-index', doc_type='answers', refresh=True)

        self.assertEquals(100, success)
        self.assertFalse(failed)
        self.assertEquals(100, self.client.count(index='test-index', doc_type='answers')['count'])
        self.assertEquals({"answer": 42}, self.client.get(index='test-index', doc_type='answers', id=42)['_source'])

    def test_stats_only_reports_numbers(self):
        docs = [{"answer": x} for x in range(100)]
        success, failed = helpers.bulk_index(self.client, docs, index='test-index', doc_type='answers', refresh=True, stats_only=True)

        self.assertEquals(100, success)
        self.assertEquals(0, failed)
        self.assertEquals(100, self.client.count(index='test-index', doc_type='answers')['count'])

    def test_errors_are_reported_correctly(self):
        self.client.indices.create("i",
            {
                "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0}
            })
        self.client.cluster.health(wait_for_status="yellow")

        success, failed = helpers.bulk_index(
            self.client,
            [{"a": 42}, {"a": "c", '_id': 42}],
            index="i",
            doc_type="t"
        )
        self.assertEquals(1, success)
        self.assertEquals(1, len(failed))
        error = failed[0]
        self.assertEquals('42', error['index']['_id'])
        self.assertEquals('t', error['index']['_type'])
        self.assertEquals('i', error['index']['_index'])
        self.assertIn('MapperParsingException', error['index']['error'])

    def test_error_is_raised_if_requested(self):
        self.client.indices.create("i",
            {
                "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0}
            })
        self.client.cluster.health(wait_for_status="yellow")

        self.assertRaises(helpers.BulkIndexError, helpers.bulk_index,
            self.client,
            [{"a": 42}, {"a": "c"}],
            index="i",
            doc_type="t",
            raise_on_error=True
        )

    def test_errors_are_collected_properly(self):
        self.client.indices.create("i",
            {
                "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0}
            })
        self.client.cluster.health(wait_for_status="yellow")

        success, failed = helpers.bulk_index(
            self.client,
            [{"a": 42}, {"a": "c"}],
            index="i",
            doc_type="t",
            stats_only=True
        )
        self.assertEquals(1, success)
        self.assertEquals(1, failed)


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

        self.assertEquals({"answer": 42, "correct": True}, self.client.get(index="prod_index", doc_type="answers", id=42)['_source'])

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


class TestStreamingBulkIndex(ElasticTestCase):
    def test_all_documents_get_inserted(self):
        commands = [
            [
                {"index": {"_id": x}},
                {'answer': x}
            ]
            for x in range(101)
        ]
        for x, (ok, cmd, result) in enumerate(helpers.streaming_bulk_index(
            self.client, commands,
            chunk_size=10,
            index='test-index', doc_type='answers', refresh=True,
        )):
            self.assertTrue(ok)
            self.assertEquals(cmd, [{"index": {"_id": x}}, {'answer': x}])
            self.assertEquals(result, {
                "index": {"_index": "test-index",
                          "_type": "answers",
                          "_id": str(x),
                          "_version": 1,
                          "ok": True, }})
        self.assertEquals(x, 100)

    def test_responses_are_reported_correctly(self):
        self.client.indices.create("i", {
            "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
            "settings": {"number_of_shards": 1, "number_of_replicas": 0}
        })
        self.client.cluster.health(wait_for_status="yellow")

        commands = [
            [{"index": {}}, {'a': 42}],
            [{"index": {'_id': 42}}, {"a": "c"}],
        ]
        results = tuple(helpers.streaming_bulk_index(
            self.client, commands, index="i", doc_type="t"
        ))
        self.assertEqual(len(results), 2)
        autoid = results[0][2].values()[0].get('_id')
        self.assertEqual(results[0], (
            True,
            commands[0],
            {u'create': {u'_id': autoid,
                         u'_index': u'i',
                         u'_type': u't',
                         u'_version': 1,
                         u'ok': True}}
        ))

        autoerrmsg = results[1][2].values()[0].get('error')
        self.assertTrue('MapperParsingException' in autoerrmsg)
        self.assertEqual(results[1], (
            False,
            commands[1],
            {u'index': {u'_id': u'42',
                        u'_index': u'i',
                        u'_type': u't',
                        u'error': autoerrmsg}}
        ))

    def test_update_using_command_object(self):
        self.client.indices.create("i", {
            "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
            "settings": {"number_of_shards": 1, "number_of_replicas": 0}
        })
        self.client.cluster.health(wait_for_status="yellow")

        commands = [
            helpers.BulkCommand({"index": {}}, {'a': 42}, ext="hi"),
            helpers.BulkCommand({"index": {'_id': 42}}, {"a": "c"}, ext="ho"),
            helpers.BulkCommand({"delete": {'_id': 42}}, ext="hum"),
        ]
        results = tuple(helpers.streaming_bulk_index(
            self.client, commands, index="i", doc_type="t"
        ))
        self.assertEqual(len(results), 3)
        autoid = results[0][2].values()[0].get('_id')
        self.assertEqual(results[0], (
            True,
            commands[0],
            {u'create': {u'_id': autoid,
                         u'_index': u'i',
                         u'_type': u't',
                         u'_version': 1,
                         u'ok': True}}
        ))
        self.assertEqual(results[0][1].ext, 'hi')

        autoerrmsg = results[1][2].values()[0].get('error')
        self.assertTrue('MapperParsingException' in autoerrmsg)
        self.assertEqual(results[1], (
            False,
            commands[1],
            {u'index': {u'_id': u'42',
                        u'_index': u'i',
                        u'_type': u't',
                        u'error': autoerrmsg}}
        ))
        self.assertEqual(results[1][1].ext, 'ho')

        self.assertEqual(results[2], (
            True,
            commands[2],
            {u'delete': {u'_id': u'42',
                         u'_index': u'i',
                         u'_type': u't',
                         u'_version': 1,
                         u'found': False,
                         u'ok': True}}
        ))
        self.assertEqual(results[2][1].ext, 'hum')


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
        self.assertEquals(50, self.client.count(index='prod_index', doc_type='questions')['count'])
        self.assertEquals(50, self.client.count(index='prod_index', doc_type='answers')['count'])

        self.assertEquals({"answer": 42, "correct": True}, self.client.get(index="prod_index", doc_type="answers", id=42)['_source'])

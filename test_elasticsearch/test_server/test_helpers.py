from elasticsearch import helpers, TransportError

from . import ElasticsearchTestCase
from ..test_cases import SkipTest


class FailingBulkClient(object):
    def __init__(self, client, fail_at=(2, ), fail_with=TransportError(599, "Error!", {})):
        self.client = client
        self._called = 0
        self._fail_at = fail_at
        self.transport = client.transport
        self._fail_with = fail_with

    def bulk(self, *args, **kwargs):
        self._called += 1
        if self._called in self._fail_at:
            raise self._fail_with
        return  self.client.bulk(*args, **kwargs)

class TestStreamingBulk(ElasticsearchTestCase):
    def test_actions_remain_unchanged(self):
        actions = [{'_id': 1}, {'_id': 2}]
        for ok, item in helpers.streaming_bulk(self.client, actions, index='test-index', doc_type='answers'):
            self.assertTrue(ok)
        self.assertEquals([{'_id': 1}, {'_id': 2}], actions)

    def test_all_documents_get_inserted(self):
        docs = [{"answer": x, '_id': x} for x in range(100)]
        for ok, item in helpers.streaming_bulk(self.client, docs, index='test-index', doc_type='answers', refresh=True):
            self.assertTrue(ok)

        self.assertEquals(100, self.client.count(index='test-index', doc_type='answers')['count'])
        self.assertEquals({"answer": 42}, self.client.get(index='test-index', doc_type='answers', id=42)['_source'])

    def test_all_errors_from_chunk_are_raised_on_failure(self):
        self.client.indices.create("i",
            {
                "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0}
            })
        self.client.cluster.health(wait_for_status="yellow")

        try:
            for ok, item in helpers.streaming_bulk(self.client, [{"a": "b"},
                {"a": "c"}], index="i", doc_type="t", raise_on_error=True):
                self.assertTrue(ok)
        except helpers.BulkIndexError as e:
            self.assertEquals(2, len(e.errors))
        else:
            assert False, "exception should have been raised"

    def test_different_op_types(self):
        if self.es_version < (0, 90, 1):
            raise SkipTest('update supported since 0.90.1')
        self.client.index(index='i', doc_type='t', id=45, body={})
        self.client.index(index='i', doc_type='t', id=42, body={})
        docs = [
            {'_index': 'i', '_type': 't', '_id': 47, 'f': 'v'},
            {'_op_type': 'delete', '_index': 'i', '_type': 't', '_id': 45},
            {'_op_type': 'update', '_index': 'i', '_type': 't', '_id': 42, 'doc': {'answer': 42}}
        ]
        for ok, item in helpers.streaming_bulk(self.client, docs):
            self.assertTrue(ok)

        self.assertFalse(self.client.exists(index='i', doc_type='t', id=45))
        self.assertEquals({'answer': 42}, self.client.get(index='i', doc_type='t', id=42)['_source'])
        self.assertEquals({'f': 'v'}, self.client.get(index='i', doc_type='t', id=47)['_source'])

    def test_transport_error_can_becaught(self):
        failing_client = FailingBulkClient(self.client)
        docs = [
            {'_index': 'i', '_type': 't', '_id': 47, 'f': 'v'},
            {'_index': 'i', '_type': 't', '_id': 45, 'f': 'v'},
            {'_index': 'i', '_type': 't', '_id': 42, 'f': 'v'},
        ]

        results = list(helpers.streaming_bulk(failing_client, docs, raise_on_exception=False, raise_on_error=False, chunk_size=1))
        self.assertEquals(3, len(results))
        self.assertEquals([True, False, True], [r[0] for r in results])

        exc = results[1][1]['index'].pop('exception')
        self.assertIsInstance(exc, TransportError)
        self.assertEquals(599, exc.status_code)
        self.assertEquals(
            {
                'index': {
                    '_index': 'i',
                    '_type': 't',
                    '_id': 45,
                    'data': {'f': 'v'},
                    'error': "TransportError(599, 'Error!')",
                    'status': 599
                }
            },
            results[1][1]
        )

    def test_rejected_documents_are_retried(self):
        failing_client = FailingBulkClient(self.client, fail_with=TransportError(429, 'Rejected!', {}))
        docs = [
            {'_index': 'i', '_type': 't', '_id': 47, 'f': 'v'},
            {'_index': 'i', '_type': 't', '_id': 45, 'f': 'v'},
            {'_index': 'i', '_type': 't', '_id': 42, 'f': 'v'},
        ]
        results = list(helpers.streaming_bulk(failing_client, docs,
                                              raise_on_exception=False,
                                              raise_on_error=False,
                                              chunk_size=1, max_retries=1,
                                              initial_backoff=0))
        self.assertEquals(3, len(results))
        self.assertEquals([True, True, True], [r[0] for r in results])
        self.client.indices.refresh(index='i')
        res = self.client.search(index='i')
        self.assertEquals(3, res['hits']['total'])
        self.assertEquals(4, failing_client._called)

    def test_rejected_documents_are_retried_at_most_max_retries_times(self):
        failing_client = FailingBulkClient(self.client, fail_at=(1, 2, ),
                                           fail_with=TransportError(429, 'Rejected!', {}))

        docs = [
            {'_index': 'i', '_type': 't', '_id': 47, 'f': 'v'},
            {'_index': 'i', '_type': 't', '_id': 45, 'f': 'v'},
            {'_index': 'i', '_type': 't', '_id': 42, 'f': 'v'},
        ]
        results = list(helpers.streaming_bulk(failing_client, docs,
                                              raise_on_exception=False,
                                              raise_on_error=False,
                                              chunk_size=1, max_retries=1,
                                              initial_backoff=0))
        self.assertEquals(3, len(results))
        self.assertEquals([False, True, True], [r[0] for r in results])
        self.client.indices.refresh(index='i')
        res = self.client.search(index='i')
        self.assertEquals(2, res['hits']['total'])
        self.assertEquals(4, failing_client._called)

    def test_transport_error_is_raised_with_max_retries(self):
        failing_client = FailingBulkClient(self.client, fail_at=(1, 2, 3, 4, ),
                                           fail_with=TransportError(429, 'Rejected!', {}))

        def streaming_bulk():
            results = list(helpers.streaming_bulk(
                failing_client,
                [{"a": 42}, {"a": 39}],
                raise_on_exception=True,
                max_retries=3,
                initial_backoff=0
            ))
            return results

        self.assertRaises(TransportError, streaming_bulk)
        self.assertEquals(4, failing_client._called)


class TestBulk(ElasticsearchTestCase):
    def test_bulk_works_with_single_item(self):
        docs = [{"answer": 42, '_id': 1}]
        success, failed = helpers.bulk(self.client, docs, index='test-index', doc_type='answers', refresh=True)

        self.assertEquals(1, success)
        self.assertFalse(failed)
        self.assertEquals(1, self.client.count(index='test-index', doc_type='answers')['count'])
        self.assertEquals({"answer": 42}, self.client.get(index='test-index', doc_type='answers', id=1)['_source'])

    def test_all_documents_get_inserted(self):
        docs = [{"answer": x, '_id': x} for x in range(100)]
        success, failed = helpers.bulk(self.client, docs, index='test-index', doc_type='answers', refresh=True)

        self.assertEquals(100, success)
        self.assertFalse(failed)
        self.assertEquals(100, self.client.count(index='test-index', doc_type='answers')['count'])
        self.assertEquals({"answer": 42}, self.client.get(index='test-index', doc_type='answers', id=42)['_source'])

    def test_stats_only_reports_numbers(self):
        docs = [{"answer": x} for x in range(100)]
        success, failed = helpers.bulk(self.client, docs, index='test-index', doc_type='answers', refresh=True, stats_only=True)

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

        success, failed = helpers.bulk(
            self.client,
            [{"a": 42}, {"a": "c", '_id': 42}],
            index="i",
            doc_type="t",
            raise_on_error=False
        )
        self.assertEquals(1, success)
        self.assertEquals(1, len(failed))
        error = failed[0]
        self.assertEquals('42', error['index']['_id'])
        self.assertEquals('t', error['index']['_type'])
        self.assertEquals('i', error['index']['_index'])
        print(error['index']['error'])
        self.assertTrue('MapperParsingException' in repr(error['index']['error']) or 'mapper_parsing_exception' in repr(error['index']['error']))

    def test_error_is_raised(self):
        self.client.indices.create("i",
            {
                "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0}
            })
        self.client.cluster.health(wait_for_status="yellow")

        self.assertRaises(helpers.BulkIndexError, helpers.bulk,
            self.client,
            [{"a": 42}, {"a": "c"}],
            index="i",
            doc_type="t"
        )

    def test_errors_are_collected_properly(self):
        self.client.indices.create("i",
            {
                "mappings": {"t": {"properties": {"a": {"type": "integer"}}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0}
            })
        self.client.cluster.health(wait_for_status="yellow")

        success, failed = helpers.bulk(
            self.client,
            [{"a": 42}, {"a": "c"}],
            index="i",
            doc_type="t",
            stats_only=True,
            raise_on_error=False
        )
        self.assertEquals(1, success)
        self.assertEquals(1, failed)


class TestScan(ElasticsearchTestCase):
    def test_order_can_be_preserved(self):
        bulk = []
        for x in range(100):
            bulk.append({"index": {"_index": "test_index", "_type": "answers", "_id": x}})
            bulk.append({"answer": x, "correct": x == 42})
        self.client.bulk(bulk, refresh=True)

        docs = list(helpers.scan(self.client, index="test_index", doc_type="answers", query={"sort": "answer"}, preserve_order=True))

        self.assertEquals(100, len(docs))
        self.assertEquals(list(map(str, range(100))), list(d['_id'] for d in docs))
        self.assertEquals(list(range(100)), list(d['_source']['answer'] for d in docs))

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

class TestReindex(ElasticsearchTestCase):
    def setUp(self):
        super(TestReindex, self).setUp()
        bulk = []
        for x in range(100):
            bulk.append({"index": {"_index": "test_index", "_type": "post", "_id": x}})
            bulk.append({"answer": x, "correct": x == 42, "type": "answers" if x % 2 == 0 else "questions"})
        self.client.bulk(bulk, refresh=True)

    def test_reindex_passes_kwargs_to_scan_and_bulk(self):
        helpers.reindex(self.client, "test_index", "prod_index", scan_kwargs={'q': 'type:answers'}, bulk_kwargs={'refresh': True})

        self.assertTrue(self.client.indices.exists("prod_index"))
        self.assertEquals(50, self.client.count(index='prod_index', q='type:answers')['count'])

        self.assertEquals({"answer": 42, "correct": True, "type": "answers"}, self.client.get(index="prod_index", doc_type="post", id=42)['_source'])

    def test_reindex_accepts_a_query(self):
        helpers.reindex(self.client, "test_index", "prod_index", query={"query": {"bool": {"filter": {"term": {"type": "answers"}}}}})
        self.client.indices.refresh()

        self.assertTrue(self.client.indices.exists("prod_index"))
        self.assertEquals(50, self.client.count(index='prod_index', q='type:answers')['count'])

        self.assertEquals({"answer": 42, "correct": True, "type": "answers"}, self.client.get(index="prod_index", doc_type="post", id=42)['_source'])

    def test_all_documents_get_moved(self):
        helpers.reindex(self.client, "test_index", "prod_index")
        self.client.indices.refresh()

        self.assertTrue(self.client.indices.exists("prod_index"))
        self.assertEquals(50, self.client.count(index='prod_index', q='type:questions')['count'])
        self.assertEquals(50, self.client.count(index='prod_index', q='type:answers')['count'])

        self.assertEquals({"answer": 42, "correct": True, "type": "answers"}, self.client.get(index="prod_index", doc_type="post", id=42)['_source'])

class TestParentChildReindex(ElasticsearchTestCase):
    def setUp(self):
        super(TestParentChildReindex, self).setUp()
        body={
            'settings': {"number_of_shards": 1, "number_of_replicas": 0},
            'mappings': {
                'post': {
                    'properties': {
                        'question_answer': {
                            'type': 'join',
                            'relations': {'question': 'answer'}
                        }
                    }
                }
            }
        }
        self.client.indices.create(index='test-index', body=body)
        self.client.indices.create(index='real-index', body=body)

        self.client.index(
            index='test-index',
            doc_type='post',
            id=42,
            body={'question_answer': 'question'},
        )
        self.client.index(
            index='test-index',
            doc_type='post',
            id=47,
            routing=42,
            body={'some': 'data', 'question_answer': {'name': 'answer', 'parent': 42}},
        )
        self.client.indices.refresh(index='test-index')

    def test_children_are_reindexed_correctly(self):
        helpers.reindex(self.client, 'test-index', 'real-index')

        q = self.client.get(
            index='real-index',
            doc_type='post',
            id=42
        )
        self.assertEquals(
            {
                '_id': '42',
                '_index': 'real-index',
                '_source': {'question_answer': 'question'},
                '_type': 'post',
                '_version': 1,
                'found': True
            }, q
        )
        q = self.client.get(
            index='test-index',
            doc_type='post',
            id=47,
            routing=42
        )
        self.assertEquals(
            {
                '_routing': '42',
                '_id': '47',
                '_index': 'test-index',
                '_source': {'some': 'data', 'question_answer': {'name': 'answer', 'parent': 42}},
                '_type': 'post',
                '_version': 1,
                'found': True
            }, q
        )

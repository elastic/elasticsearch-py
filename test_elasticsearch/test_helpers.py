import mock
import time
import threading

from elasticsearch import helpers, Elasticsearch
from elasticsearch.serializer import JSONSerializer

from .test_cases import TestCase

class TestParallelBulk(TestCase):
    @mock.patch('elasticsearch.helpers._process_bulk_chunk', return_value=[])
    def test_all_chunks_sent(self, _process_bulk_chunk):
        actions = ({'x': i} for i in range(100))
        list(helpers.parallel_bulk(Elasticsearch(), actions, chunk_size=2))

        self.assertEquals(50, _process_bulk_chunk.call_count)

    @mock.patch(
        'elasticsearch.helpers._process_bulk_chunk',
        # make sure we spend some time in the thread
        side_effect=lambda *a: [(True, time.sleep(.001) or threading.get_ident())]
    )
    def test_chunk_sent_from_different_threads(self, _process_bulk_chunk):
        actions = ({'x': i} for i in range(100))
        results = list(helpers.parallel_bulk(Elasticsearch(), actions, thread_count=10, chunk_size=2))

        self.assertTrue(len(set([r[1] for r in results])) > 1)

class TestChunkActions(TestCase):
    def setUp(self):
        super(TestChunkActions, self).setUp()
        self.actions = [({'index': {}}, {'some': 'data', 'i': i}) for i in range(100)]

    def test_chunks_are_chopped_by_byte_size(self):
        self.assertEquals(100, len(list(helpers._chunk_actions(self.actions, 100000, 1, JSONSerializer()))))

    def test_chunks_are_chopped_by_chunk_size(self):
        self.assertEquals(10, len(list(helpers._chunk_actions(self.actions, 10, 99999999, JSONSerializer()))))

class TestExpandActions(TestCase):
    def test_string_actions_are_marked_as_simple_inserts(self):
        self.assertEquals(('{"index":{}}', "whatever"), helpers.expand_action('whatever'))

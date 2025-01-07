#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import pickle
import threading
import time
from unittest import mock

import pytest

from elasticsearch import Elasticsearch, helpers
from elasticsearch.serializer import JSONSerializer

lock_side_effect = threading.Lock()


def mock_process_bulk_chunk(*args, **kwargs):
    """
    Threadsafe way of mocking process bulk chunk:
    https://stackoverflow.com/questions/39332139/thread-safe-version-of-mock-call-count
    """

    with lock_side_effect:
        mock_process_bulk_chunk.call_count += 1
    time.sleep(0.1)
    return []


mock_process_bulk_chunk.call_count = 0


class TestParallelBulk:
    @mock.patch(
        "elasticsearch.helpers.actions._process_bulk_chunk",
        side_effect=mock_process_bulk_chunk,
    )
    def test_all_chunks_sent(self, _process_bulk_chunk):
        actions = ({"x": i} for i in range(100))
        list(
            helpers.parallel_bulk(
                Elasticsearch("http://localhost:9200"), actions, chunk_size=2
            )
        )

        assert 50 == mock_process_bulk_chunk.call_count

    @mock.patch(
        "elasticsearch.helpers.actions._process_bulk_chunk",
        # make sure we spend some time in the thread
        side_effect=lambda *_, **__: [
            (True, time.sleep(0.001) or threading.current_thread().ident)
        ],
    )
    def test_chunk_sent_from_different_threads(self, _process_bulk_chunk):
        actions = ({"x": i} for i in range(100))
        results = list(
            helpers.parallel_bulk(
                Elasticsearch("http://localhost:9200"),
                actions,
                thread_count=10,
                chunk_size=2,
            )
        )
        assert len({r[1] for r in results}) > 1


class TestChunkActions:
    def setup_method(self, _):
        self.actions = [({"index": {}}, {"some": "datá", "i": i}) for i in range(100)]

    def test_expand_action(self):
        assert helpers.expand_action({}) == ({"index": {}}, {})
        assert helpers.expand_action({"key": "val"}) == ({"index": {}}, {"key": "val"})

    def test_expand_action_actions(self):
        assert helpers.expand_action(
            {"_op_type": "delete", "_id": "id", "_index": "index"}
        ) == ({"delete": {"_id": "id", "_index": "index"}}, None)
        assert helpers.expand_action(
            {"_op_type": "update", "_id": "id", "_index": "index", "key": "val"}
        ) == ({"update": {"_id": "id", "_index": "index"}}, {"key": "val"})
        assert helpers.expand_action(
            {"_op_type": "create", "_id": "id", "_index": "index", "key": "val"}
        ) == ({"create": {"_id": "id", "_index": "index"}}, {"key": "val"})
        assert helpers.expand_action(
            {
                "_op_type": "create",
                "_id": "id",
                "_index": "index",
                "_source": {"key": "val"},
            }
        ) == ({"create": {"_id": "id", "_index": "index"}}, {"key": "val"})

    def test_expand_action_options(self):
        for option in (
            "_id",
            "_index",
            "_percolate",
            "_timestamp",
            "_type",
            "if_seq_no",
            "if_primary_term",
            "parent",
            "pipeline",
            "retry_on_conflict",
            "routing",
            "version",
            "version_type",
            ("_parent", "parent"),
            ("_retry_on_conflict", "retry_on_conflict"),
            ("_routing", "routing"),
            ("_version", "version"),
            ("_version_type", "version_type"),
            ("_if_seq_no", "if_seq_no"),
            ("_if_primary_term", "if_primary_term"),
        ):
            if isinstance(option, str):
                action_option = option
            else:
                option, action_option = option
            assert helpers.expand_action({"key": "val", option: 0}) == (
                {"index": {action_option: 0}},
                {"key": "val"},
            )

    def test__source_metadata_or_source(self):
        assert helpers.expand_action({"_source": {"key": "val"}}) == (
            {"index": {}},
            {"key": "val"},
        )

        assert helpers.expand_action(
            {"_source": ["key"], "key": "val", "_op_type": "update"}
        ) == ({"update": {"_source": ["key"]}}, {"key": "val"})

        assert helpers.expand_action(
            {"_source": True, "key": "val", "_op_type": "update"}
        ) == ({"update": {"_source": True}}, {"key": "val"})

        # This case is only to ensure backwards compatibility with old functionality.
        assert helpers.expand_action(
            {"_source": {"key2": "val2"}, "key": "val", "_op_type": "update"}
        ) == ({"update": {}}, {"key2": "val2"})

    def test_chunks_are_chopped_by_byte_size(self):
        assert 100 == len(
            list(helpers._chunk_actions(self.actions, 100000, 1, JSONSerializer()))
        )

    def test_chunks_are_chopped_by_chunk_size(self):
        assert 10 == len(
            list(helpers._chunk_actions(self.actions, 10, 99999999, JSONSerializer()))
        )

    def test_chunks_are_chopped_by_byte_size_properly(self):
        max_byte_size = 170
        chunks = list(
            helpers._chunk_actions(
                self.actions, 100000, max_byte_size, JSONSerializer()
            )
        )
        assert 25 == len(chunks)
        for chunk_data, chunk_actions in chunks:
            chunk = b"".join(chunk_actions)
            assert len(chunk) <= max_byte_size


class TestExpandActions:
    @pytest.mark.parametrize("action", ["whatever", b"whatever"])
    def test_string_actions_are_marked_as_simple_inserts(self, action):
        assert ({"index": {}}, b"whatever") == helpers.expand_action(action)


def test_serialize_bulk_index_error():
    error = helpers.BulkIndexError("message", [{"error": 1}])
    pickled = pickle.loads(pickle.dumps(error))
    assert pickled.__class__ == helpers.BulkIndexError
    assert pickled.errors == error.errors
    assert pickled.args == error.args


def test_serialize_scan_error():
    error = helpers.ScanError("scroll_id", "shard_message")
    pickled = pickle.loads(pickle.dumps(error))
    assert pickled.__class__ == helpers.ScanError
    assert pickled.scroll_id == error.scroll_id
    assert pickled.args == error.args

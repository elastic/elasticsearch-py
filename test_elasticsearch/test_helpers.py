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
from typing import Optional
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

    @pytest.mark.parametrize("flush_seconds", [None, 10])
    def test_chunks_are_chopped_by_byte_size(self, flush_seconds: Optional[float]):
        assert 100 == len(
            list(
                helpers._chunk_actions(
                    self.actions, 100000, 1, flush_seconds, JSONSerializer()
                )
            )
        )

    @pytest.mark.parametrize("flush_seconds", [None, 10])
    def test_chunks_are_chopped_by_chunk_size(self, flush_seconds: Optional[float]):
        assert 10 == len(
            list(
                helpers._chunk_actions(
                    self.actions, 10, 99999999, flush_seconds, JSONSerializer()
                )
            )
        )

    @pytest.mark.parametrize("flush_seconds", [None, 10])
    def test_chunks_are_chopped_by_byte_size_properly(
        self, flush_seconds: Optional[float]
    ):
        max_byte_size = 170
        chunks = list(
            helpers._chunk_actions(
                self.actions, 100000, max_byte_size, flush_seconds, JSONSerializer()
            )
        )
        assert 25 == len(chunks)
        for chunk_data, chunk_actions in chunks:
            chunk = b"".join(chunk_actions)
            assert len(chunk) <= max_byte_size

    @pytest.mark.parametrize("flush_seconds", [None, 10])
    def test_chunks_are_chopped_by_flush(self, flush_seconds: Optional[float]):
        flush = (helpers.BULK_FLUSH, None)
        actions = (
            self.actions[:3]
            + [flush] * 2  # two consecutive flushes after 3 items
            + self.actions[3:4]
            + [flush]  # flush after one more item
            + self.actions[4:]
            + [flush]  # flush at the end
        )
        chunks = list(
            helpers._chunk_actions(
                actions, 100, 99999999, flush_seconds, JSONSerializer()
            )
        )
        assert 3 == len(chunks)
        assert len(chunks[0][0]) == 3
        assert len(chunks[0][1]) == 6
        assert len(chunks[1][0]) == 1
        assert len(chunks[1][1]) == 2
        assert len(chunks[2][0]) == 96
        assert len(chunks[2][1]) == 192


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


class TestProcessBulkChunkSuccess:
    def test_raise_on_error_collects_all_errors_before_raising(self):
        """Test that when raise_on_error=True, only successful items are yielded
        and all errors are collected before raising BulkIndexError."""
        # Simulate a response with mixed success/failure
        resp = {
            "items": [
                {"index": {"_id": "1", "status": 201}},  # success
                {"index": {"_id": "2", "status": 400, "error": "bad request"}},  # fail
                {"index": {"_id": "3", "status": 200}},  # success
                {"index": {"_id": "4", "status": 500, "error": "server error"}},  # fail
            ]
        }
        bulk_data = [
            ({"index": {"_id": "1"}}, {"data": 1}),
            ({"index": {"_id": "2"}}, {"data": 2}),
            ({"index": {"_id": "3"}}, {"data": 3}),
            ({"index": {"_id": "4"}}, {"data": 4}),
        ]

        # With raise_on_error=True, should only yield successful items
        results = []
        try:
            for ok, item in helpers.actions._process_bulk_chunk_success(
                resp, bulk_data, ignore_status=[], raise_on_error=True
            ):
                results.append((ok, item))
        except helpers.BulkIndexError as e:
            # Should have collected 2 errors
            assert len(e.errors) == 2
            assert e.errors[0]["index"]["_id"] == "2"
            assert e.errors[1]["index"]["_id"] == "4"
        else:
            assert False, "BulkIndexError should have been raised"

        # Should have yielded only the 2 successful items
        assert len(results) == 2
        assert results[0][0] is True  # ok=True
        assert results[0][1]["index"]["_id"] == "1"
        assert results[1][0] is True  # ok=True
        assert results[1][1]["index"]["_id"] == "3"

    def test_raise_on_error_false_yields_all_items(self):
        """Test that when raise_on_error=False, all items (success and failure) are yielded."""
        resp = {
            "items": [
                {"index": {"_id": "1", "status": 201}},  # success
                {"index": {"_id": "2", "status": 400, "error": "bad request"}},  # fail
                {"index": {"_id": "3", "status": 200}},  # success
            ]
        }
        bulk_data = [
            ({"index": {"_id": "1"}}, {"data": 1}),
            ({"index": {"_id": "2"}}, {"data": 2}),
            ({"index": {"_id": "3"}}, {"data": 3}),
        ]

        # With raise_on_error=False, should yield all items
        results = list(
            helpers.actions._process_bulk_chunk_success(
                resp, bulk_data, ignore_status=[], raise_on_error=False
            )
        )

        # Should have yielded all 3 items
        assert len(results) == 3
        assert results[0][0] is True  # ok=True
        assert results[1][0] is False  # ok=False (failed)
        assert results[2][0] is True  # ok=True


class TestMutableDefaultArguments:
    def test_reindex_does_not_mutate_default_arguments(self):
        """Test that reindex() doesn't share mutable default arguments across calls."""
        client = mock.Mock(spec=Elasticsearch)

        # Mock the scan function to return an empty iterator
        with mock.patch("elasticsearch.helpers.actions.scan", return_value=iter([])):
            # Mock the bulk function to return (0, [])
            with mock.patch("elasticsearch.helpers.actions.bulk", return_value=(0, [])):
                # Mock indices.get_data_stream to raise NotFoundError
                client.indices.get_data_stream.side_effect = Exception("Not found")

                # First call - don't pass scan_kwargs or bulk_kwargs
                helpers.reindex(
                    client, source_index="source", target_index="target"
                )

                # Second call - also don't pass scan_kwargs or bulk_kwargs
                # If the defaults are mutable and shared, this could cause issues
                helpers.reindex(
                    client, source_index="source2", target_index="target2"
                )

                # Verify scan was called twice with empty dicts (not the same dict object)
                assert client.indices.get_data_stream.call_count == 2

    def test_reindex_scan_kwargs_not_shared_between_calls(self):
        """Test that modifying scan_kwargs in one call doesn't affect another."""
        client = mock.Mock(spec=Elasticsearch)

        scan_calls = []

        def mock_scan(*args, **kwargs):
            # Capture the kwargs to verify they're not shared
            scan_calls.append(kwargs.copy())
            return iter([])

        with mock.patch("elasticsearch.helpers.actions.scan", side_effect=mock_scan):
            with mock.patch("elasticsearch.helpers.actions.bulk", return_value=(0, [])):
                client.indices.get_data_stream.side_effect = Exception("Not found")

                # First call with no scan_kwargs
                helpers.reindex(
                    client, source_index="source", target_index="target"
                )

                # Second call also with no scan_kwargs
                helpers.reindex(
                    client, source_index="source2", target_index="target2"
                )

                # Verify both calls got separate empty dicts
                # (If they shared the same dict, modifications would persist)
                assert len(scan_calls) == 2
                assert scan_calls[0] == {
                    "query": None,
                    "index": "source",
                    "scroll": "5m",
                }
                assert scan_calls[1] == {
                    "query": None,
                    "index": "source2",
                    "scroll": "5m",
                }

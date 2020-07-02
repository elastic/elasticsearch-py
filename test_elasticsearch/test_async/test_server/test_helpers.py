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

import pytest
import asyncio
from mock import patch, MagicMock

from elasticsearch import helpers, TransportError
from elasticsearch.helpers import ScanError


pytestmark = pytest.mark.asyncio


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class FailingBulkClient(object):
    def __init__(
        self, client, fail_at=(2,), fail_with=TransportError(599, "Error!", {})
    ):
        self.client = client
        self._called = 0
        self._fail_at = fail_at
        self.transport = client.transport
        self._fail_with = fail_with

    async def bulk(self, *args, **kwargs):
        self._called += 1
        if self._called in self._fail_at:
            raise self._fail_with
        return await self.client.bulk(*args, **kwargs)


class TestStreamingBulk(object):
    async def test_actions_remain_unchanged(self, async_client):
        actions = [{"_id": 1}, {"_id": 2}]
        async for ok, item in helpers.async_streaming_bulk(
            async_client, actions, index="test-index"
        ):
            assert ok
        assert [{"_id": 1}, {"_id": 2}] == actions

    async def test_all_documents_get_inserted(self, async_client):
        docs = [{"answer": x, "_id": x} for x in range(100)]
        async for ok, item in helpers.async_streaming_bulk(
            async_client, docs, index="test-index", refresh=True
        ):
            assert ok

        assert 100 == (await async_client.count(index="test-index"))["count"]
        assert {"answer": 42} == (await async_client.get(index="test-index", id=42))[
            "_source"
        ]

    async def test_documents_data_types(self, async_client):
        async def async_gen():
            for x in range(100):
                await asyncio.sleep(0)
                yield {"answer": x, "_id": x}

        def sync_gen():
            for x in range(100):
                yield {"answer": x, "_id": x}

        async for ok, item in helpers.async_streaming_bulk(
            async_client, async_gen(), index="test-index", refresh=True
        ):
            assert ok

        assert 100 == (await async_client.count(index="test-index"))["count"]
        assert {"answer": 42} == (await async_client.get(index="test-index", id=42))[
            "_source"
        ]

        await async_client.delete_by_query(
            index="test-index", body={"query": {"match_all": {}}}
        )

        async for ok, item in helpers.async_streaming_bulk(
            async_client, sync_gen(), index="test-index", refresh=True
        ):
            assert ok

        assert 100 == (await async_client.count(index="test-index"))["count"]
        assert {"answer": 42} == (await async_client.get(index="test-index", id=42))[
            "_source"
        ]

    async def test_all_errors_from_chunk_are_raised_on_failure(self, async_client):
        await async_client.indices.create(
            "i",
            {
                "mappings": {"properties": {"a": {"type": "integer"}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            },
        )
        await async_client.cluster.health(wait_for_status="yellow")

        try:
            async for ok, item in helpers.async_streaming_bulk(
                async_client, [{"a": "b"}, {"a": "c"}], index="i", raise_on_error=True
            ):
                assert ok
        except helpers.BulkIndexError as e:
            assert 2 == len(e.errors)
        else:
            assert False, "exception should have been raised"

    async def test_different_op_types(self, async_client):
        await async_client.index(index="i", id=45, body={})
        await async_client.index(index="i", id=42, body={})
        docs = [
            {"_index": "i", "_id": 47, "f": "v"},
            {"_op_type": "delete", "_index": "i", "_id": 45},
            {"_op_type": "update", "_index": "i", "_id": 42, "doc": {"answer": 42}},
        ]
        async for ok, item in helpers.async_streaming_bulk(async_client, docs):
            assert ok

        assert not await async_client.exists(index="i", id=45)
        assert {"answer": 42} == (await async_client.get(index="i", id=42))["_source"]
        assert {"f": "v"} == (await async_client.get(index="i", id=47))["_source"]

    async def test_transport_error_can_becaught(self, async_client):
        failing_client = FailingBulkClient(async_client)
        docs = [
            {"_index": "i", "_id": 47, "f": "v"},
            {"_index": "i", "_id": 45, "f": "v"},
            {"_index": "i", "_id": 42, "f": "v"},
        ]

        results = [
            x
            async for x in helpers.async_streaming_bulk(
                failing_client,
                docs,
                raise_on_exception=False,
                raise_on_error=False,
                chunk_size=1,
            )
        ]
        assert 3 == len(results)
        assert [True, False, True] == [r[0] for r in results]

        exc = results[1][1]["index"].pop("exception")
        assert isinstance(exc, TransportError)
        assert 599 == exc.status_code
        assert {
            "index": {
                "_index": "i",
                "_id": 45,
                "data": {"f": "v"},
                "error": "TransportError(599, 'Error!')",
                "status": 599,
            }
        } == results[1][1]

    async def test_rejected_documents_are_retried(self, async_client):
        failing_client = FailingBulkClient(
            async_client, fail_with=TransportError(429, "Rejected!", {})
        )
        docs = [
            {"_index": "i", "_id": 47, "f": "v"},
            {"_index": "i", "_id": 45, "f": "v"},
            {"_index": "i", "_id": 42, "f": "v"},
        ]
        results = [
            x
            async for x in helpers.async_streaming_bulk(
                failing_client,
                docs,
                raise_on_exception=False,
                raise_on_error=False,
                chunk_size=1,
                max_retries=1,
                initial_backoff=0,
            )
        ]
        assert 3 == len(results)
        assert [True, True, True] == [r[0] for r in results]
        await async_client.indices.refresh(index="i")
        res = await async_client.search(index="i")
        assert {"value": 3, "relation": "eq"} == res["hits"]["total"]
        assert 4 == failing_client._called

    async def test_rejected_documents_are_retried_at_most_max_retries_times(
        self, async_client
    ):
        failing_client = FailingBulkClient(
            async_client, fail_at=(1, 2), fail_with=TransportError(429, "Rejected!", {})
        )

        docs = [
            {"_index": "i", "_id": 47, "f": "v"},
            {"_index": "i", "_id": 45, "f": "v"},
            {"_index": "i", "_id": 42, "f": "v"},
        ]
        results = [
            x
            async for x in helpers.async_streaming_bulk(
                failing_client,
                docs,
                raise_on_exception=False,
                raise_on_error=False,
                chunk_size=1,
                max_retries=1,
                initial_backoff=0,
            )
        ]
        assert 3 == len(results)
        assert [False, True, True] == [r[0] for r in results]
        await async_client.indices.refresh(index="i")
        res = await async_client.search(index="i")
        assert {"value": 2, "relation": "eq"} == res["hits"]["total"]
        assert 4 == failing_client._called

    async def test_transport_error_is_raised_with_max_retries(self, async_client):
        failing_client = FailingBulkClient(
            async_client,
            fail_at=(1, 2, 3, 4),
            fail_with=TransportError(429, "Rejected!", {}),
        )

        async def streaming_bulk():
            results = [
                x
                async for x in helpers.async_streaming_bulk(
                    failing_client,
                    [{"a": 42}, {"a": 39}],
                    raise_on_exception=True,
                    max_retries=3,
                    initial_backoff=0,
                )
            ]
            return results

        with pytest.raises(TransportError):
            await streaming_bulk()
        assert 4 == failing_client._called


class TestBulk(object):
    async def test_bulk_works_with_single_item(self, async_client):
        docs = [{"answer": 42, "_id": 1}]
        success, failed = await helpers.async_bulk(
            async_client, docs, index="test-index", refresh=True
        )

        assert 1 == success
        assert not failed
        assert 1 == (await async_client.count(index="test-index"))["count"]
        assert {"answer": 42} == (await async_client.get(index="test-index", id=1))[
            "_source"
        ]

    async def test_all_documents_get_inserted(self, async_client):
        docs = [{"answer": x, "_id": x} for x in range(100)]
        success, failed = await helpers.async_bulk(
            async_client, docs, index="test-index", refresh=True
        )

        assert 100 == success
        assert not failed
        assert 100 == (await async_client.count(index="test-index"))["count"]
        assert {"answer": 42} == (await async_client.get(index="test-index", id=42))[
            "_source"
        ]

    async def test_stats_only_reports_numbers(self, async_client):
        docs = [{"answer": x} for x in range(100)]
        success, failed = await helpers.async_bulk(
            async_client, docs, index="test-index", refresh=True, stats_only=True
        )

        assert 100 == success
        assert 0 == failed
        assert 100 == (await async_client.count(index="test-index"))["count"]

    async def test_errors_are_reported_correctly(self, async_client):
        await async_client.indices.create(
            "i",
            {
                "mappings": {"properties": {"a": {"type": "integer"}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            },
        )
        await async_client.cluster.health(wait_for_status="yellow")

        success, failed = await helpers.async_bulk(
            async_client,
            [{"a": 42}, {"a": "c", "_id": 42}],
            index="i",
            raise_on_error=False,
        )
        assert 1 == success
        assert 1 == len(failed)
        error = failed[0]
        assert "42" == error["index"]["_id"]
        assert "i" == error["index"]["_index"]
        print(error["index"]["error"])
        assert "MapperParsingException" in repr(
            error["index"]["error"]
        ) or "mapper_parsing_exception" in repr(error["index"]["error"])

    async def test_error_is_raised(self, async_client):
        await async_client.indices.create(
            "i",
            {
                "mappings": {"properties": {"a": {"type": "integer"}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            },
        )
        await async_client.cluster.health(wait_for_status="yellow")

        with pytest.raises(helpers.BulkIndexError):
            await helpers.async_bulk(async_client, [{"a": 42}, {"a": "c"}], index="i")

    async def test_errors_are_collected_properly(self, async_client):
        await async_client.indices.create(
            "i",
            {
                "mappings": {"properties": {"a": {"type": "integer"}}},
                "settings": {"number_of_shards": 1, "number_of_replicas": 0},
            },
        )
        await async_client.cluster.health(wait_for_status="yellow")

        success, failed = await helpers.async_bulk(
            async_client,
            [{"a": 42}, {"a": "c"}],
            index="i",
            stats_only=True,
            raise_on_error=False,
        )
        assert 1 == success
        assert 1 == failed


class MockScroll:
    def __init__(self):
        self.calls = []

    async def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        if len(self.calls) == 1:
            return {
                "_scroll_id": "dummy_id",
                "_shards": {"successful": 4, "total": 5, "skipped": 0},
                "hits": {"hits": [{"scroll_data": 42}]},
            }
        elif len(self.calls) == 2:
            return {
                "_scroll_id": "dummy_id",
                "_shards": {"successful": 4, "total": 5, "skipped": 0},
                "hits": {"hits": []},
            }
        else:
            raise Exception("no more responses")


class MockResponse:
    def __init__(self, resp):
        self.resp = resp

    async def __call__(self, *args, **kwargs):
        return self.resp


class TestScan(object):
    async def teardown_method(self, async_client):
        await async_client.transport.perform_request("DELETE", "/_search/scroll/_all")

    async def test_order_can_be_preserved(self, async_client):
        bulk = []
        for x in range(100):
            bulk.append({"index": {"_index": "test_index", "_id": x}})
            bulk.append({"answer": x, "correct": x == 42})
        await async_client.bulk(bulk, refresh=True)

        docs = [
            doc
            async for doc in helpers.async_scan(
                async_client,
                index="test_index",
                query={"sort": "answer"},
                preserve_order=True,
            )
        ]

        assert 100 == len(docs)
        assert list(map(str, range(100))) == list(d["_id"] for d in docs)
        assert list(range(100)) == list(d["_source"]["answer"] for d in docs)

    async def test_all_documents_are_read(self, async_client):
        bulk = []
        for x in range(100):
            bulk.append({"index": {"_index": "test_index", "_id": x}})
            bulk.append({"answer": x, "correct": x == 42})
        await async_client.bulk(bulk, refresh=True)

        docs = [
            x
            async for x in helpers.async_scan(async_client, index="test_index", size=2)
        ]

        assert 100 == len(docs)
        assert set(map(str, range(100))) == set(d["_id"] for d in docs)
        assert set(range(100)) == set(d["_source"]["answer"] for d in docs)

    async def test_scroll_error(self, async_client):
        bulk = []
        for x in range(4):
            bulk.append({"index": {"_index": "test_index"}})
            bulk.append({"value": x})
        await async_client.bulk(bulk, refresh=True)

        with patch.object(async_client, "scroll", MockScroll()):
            data = [
                x
                async for x in helpers.async_scan(
                    async_client,
                    index="test_index",
                    size=2,
                    raise_on_error=False,
                    clear_scroll=False,
                )
            ]
            assert len(data) == 3
            assert data[-1] == {"scroll_data": 42}

        with patch.object(async_client, "scroll", MockScroll()):
            with pytest.raises(ScanError):
                data = [
                    x
                    async for x in helpers.async_scan(
                        async_client,
                        index="test_index",
                        size=2,
                        raise_on_error=True,
                        clear_scroll=False,
                    )
                ]
            assert len(data) == 3
            assert data[-1] == {"scroll_data": 42}

    async def test_initial_search_error(self, async_client):
        with patch.object(async_client, "clear_scroll", new_callable=AsyncMock):
            with patch.object(
                async_client,
                "search",
                MockResponse(
                    {
                        "_scroll_id": "dummy_id",
                        "_shards": {"successful": 4, "total": 5, "skipped": 0},
                        "hits": {"hits": [{"search_data": 1}]},
                    }
                ),
            ):
                with patch.object(async_client, "scroll", MockScroll()):

                    data = [
                        x
                        async for x in helpers.async_scan(
                            async_client,
                            index="test_index",
                            size=2,
                            raise_on_error=False,
                        )
                    ]
                    assert data == [{"search_data": 1}, {"scroll_data": 42}]

            with patch.object(
                async_client,
                "search",
                MockResponse(
                    {
                        "_scroll_id": "dummy_id",
                        "_shards": {"successful": 4, "total": 5, "skipped": 0},
                        "hits": {"hits": [{"search_data": 1}]},
                    }
                ),
            ):
                with patch.object(async_client, "scroll", MockScroll()) as mock_scroll:

                    with pytest.raises(ScanError):
                        data = [
                            x
                            async for x in helpers.async_scan(
                                async_client,
                                index="test_index",
                                size=2,
                                raise_on_error=True,
                            )
                        ]
                        assert data == [{"search_data": 1}]
                        assert mock_scroll.calls == []

    async def test_no_scroll_id_fast_route(self, async_client):
        with patch.object(async_client, "search", MockResponse({"no": "_scroll_id"})):
            with patch.object(async_client, "scroll") as scroll_mock:
                with patch.object(async_client, "clear_scroll") as clear_mock:
                    data = [
                        x
                        async for x in helpers.async_scan(
                            async_client, index="test_index"
                        )
                    ]

                    assert data == []
                    scroll_mock.assert_not_called()
                    clear_mock.assert_not_called()

    @patch("elasticsearch._async.helpers.logger")
    async def test_logger(self, logger_mock, async_client):
        bulk = []
        for x in range(4):
            bulk.append({"index": {"_index": "test_index"}})
            bulk.append({"value": x})
        await async_client.bulk(bulk, refresh=True)

        with patch.object(async_client, "scroll", MockScroll()):
            _ = [
                x
                async for x in helpers.async_scan(
                    async_client,
                    index="test_index",
                    size=2,
                    raise_on_error=False,
                    clear_scroll=False,
                )
            ]
            logger_mock.warning.assert_called()

        with patch.object(async_client, "scroll", MockScroll()):
            try:
                _ = [
                    x
                    async for x in helpers.async_scan(
                        async_client,
                        index="test_index",
                        size=2,
                        raise_on_error=True,
                        clear_scroll=False,
                    )
                ]
            except ScanError:
                pass
            logger_mock.warning.assert_called_with(
                "Scroll request has only succeeded on %d (+%d skipped) shards out of %d.",
                4,
                0,
                5,
            )

    async def test_clear_scroll(self, async_client):
        bulk = []
        for x in range(4):
            bulk.append({"index": {"_index": "test_index"}})
            bulk.append({"value": x})
        await async_client.bulk(bulk, refresh=True)

        with patch.object(
            async_client, "clear_scroll", wraps=async_client.clear_scroll
        ) as spy:
            _ = [
                x
                async for x in helpers.async_scan(
                    async_client, index="test_index", size=2
                )
            ]
            spy.assert_called_once()

            spy.reset_mock()
            _ = [
                x
                async for x in helpers.async_scan(
                    async_client, index="test_index", size=2, clear_scroll=True
                )
            ]
            spy.assert_called_once()

            spy.reset_mock()
            _ = [
                x
                async for x in helpers.async_scan(
                    async_client, index="test_index", size=2, clear_scroll=False
                )
            ]
            spy.assert_not_called()


@pytest.fixture(scope="function")
async def reindex_setup(async_client):
    bulk = []
    for x in range(100):
        bulk.append({"index": {"_index": "test_index", "_id": x}})
        bulk.append(
            {
                "answer": x,
                "correct": x == 42,
                "type": "answers" if x % 2 == 0 else "questions",
            }
        )
    await async_client.bulk(bulk, refresh=True)
    yield


class TestReindex(object):
    async def test_reindex_passes_kwargs_to_scan_and_bulk(
        self, async_client, reindex_setup
    ):
        await helpers.async_reindex(
            async_client,
            "test_index",
            "prod_index",
            scan_kwargs={"q": "type:answers"},
            bulk_kwargs={"refresh": True},
        )

        assert await async_client.indices.exists("prod_index")
        assert (
            50
            == (await async_client.count(index="prod_index", q="type:answers"))["count"]
        )

        assert {"answer": 42, "correct": True, "type": "answers"} == (
            await async_client.get(index="prod_index", id=42)
        )["_source"]

    async def test_reindex_accepts_a_query(self, async_client, reindex_setup):
        await helpers.async_reindex(
            async_client,
            "test_index",
            "prod_index",
            query={"query": {"bool": {"filter": {"term": {"type": "answers"}}}}},
        )
        await async_client.indices.refresh()

        assert await async_client.indices.exists("prod_index")
        assert (
            50
            == (await async_client.count(index="prod_index", q="type:answers"))["count"]
        )

        assert {"answer": 42, "correct": True, "type": "answers"} == (
            await async_client.get(index="prod_index", id=42)
        )["_source"]

    async def test_all_documents_get_moved(self, async_client, reindex_setup):
        await helpers.async_reindex(async_client, "test_index", "prod_index")
        await async_client.indices.refresh()

        assert await async_client.indices.exists("prod_index")
        assert (
            50
            == (await async_client.count(index="prod_index", q="type:questions"))[
                "count"
            ]
        )
        assert (
            50
            == (await async_client.count(index="prod_index", q="type:answers"))["count"]
        )

        assert {"answer": 42, "correct": True, "type": "answers"} == (
            await async_client.get(index="prod_index", id=42)
        )["_source"]


@pytest.fixture(scope="function")
async def parent_reindex_setup(async_client):
    body = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "question_answer": {
                    "type": "join",
                    "relations": {"question": "answer"},
                }
            }
        },
    }
    await async_client.indices.create(index="test-index", body=body)
    await async_client.indices.create(index="real-index", body=body)

    await async_client.index(
        index="test-index", id=42, body={"question_answer": "question"}
    )
    await async_client.index(
        index="test-index",
        id=47,
        routing=42,
        body={"some": "data", "question_answer": {"name": "answer", "parent": 42}},
    )
    await async_client.indices.refresh(index="test-index")


class TestParentChildReindex:
    async def test_children_are_reindexed_correctly(
        self, async_client, parent_reindex_setup
    ):
        await helpers.async_reindex(async_client, "test-index", "real-index")

        q = await async_client.get(index="real-index", id=42)
        assert {
            "_id": "42",
            "_index": "real-index",
            "_primary_term": 1,
            "_seq_no": 0,
            "_source": {"question_answer": "question"},
            "_version": 1,
            "found": True,
        } == q

        q = await async_client.get(index="test-index", id=47, routing=42)
        assert {
            "_routing": "42",
            "_id": "47",
            "_index": "test-index",
            "_primary_term": 1,
            "_seq_no": 1,
            "_source": {
                "some": "data",
                "question_answer": {"name": "answer", "parent": 42},
            },
            "_version": 1,
            "found": True,
        } == q

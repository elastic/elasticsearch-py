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

import json
from datetime import datetime, timedelta
from unittest.mock import call, patch

import pytest
from dateutil import tz
from elastic_transport import ApiResponseMeta, ObjectApiResponse

from elasticsearch import ApiError, helpers
from elasticsearch.helpers import ScanError


class FailingBulkClient:
    def __init__(
        self,
        client,
        fail_at=(2,),
        fail_with=ApiError(
            message="Error!",
            body={},
            meta=ApiResponseMeta(
                status=599, headers={}, http_version="1.1", duration=0, node=None
            ),
        ),
    ):
        self.client = client
        self._otel = client._otel
        self._called = 0
        self._fail_at = fail_at
        self.transport = client.transport
        self._fail_with = fail_with

    def bulk(self, *args, **kwargs):
        self._called += 1
        if self._called in self._fail_at:
            raise self._fail_with
        return self.client.bulk(*args, **kwargs)

    def options(self, **kwargs) -> "FailingBulkClient":
        return self


def test_bulk_actions_remain_unchanged(sync_client):
    actions = [{"_id": 1}, {"_id": 2}]
    for ok, item in helpers.streaming_bulk(sync_client, actions, index="test-index"):
        assert ok
    assert [{"_id": 1}, {"_id": 2}] == actions


def test_bulk_all_documents_get_inserted(sync_client):
    docs = [{"answer": x, "_id": x} for x in range(100)]
    for ok, item in helpers.streaming_bulk(
        sync_client, docs, index="test-index", refresh=True
    ):
        assert ok

    assert 100 == sync_client.count(index="test-index")["count"]
    assert {"answer": 42} == sync_client.get(index="test-index", id=42)["_source"]


def test_bulk_all_errors_from_chunk_are_raised_on_failure(sync_client):
    sync_client.indices.create(
        index="i",
        body={
            "mappings": {"properties": {"a": {"type": "integer"}}},
            "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        },
    )

    try:
        for ok, _ in helpers.streaming_bulk(
            sync_client, [{"a": "b"}, {"a": "c"}], index="i", raise_on_error=True
        ):
            assert ok
    except helpers.BulkIndexError as e:
        assert 2 == len(e.errors)
    else:
        assert False, "exception should have been raised"


def test_bulk_different_op_types(sync_client):
    sync_client.index(index="i", id=45, body={})
    sync_client.index(index="i", id=42, body={})
    docs = [
        {"_index": "i", "_id": 47, "f": "v"},
        {"_op_type": "delete", "_index": "i", "_id": 45},
        {"_op_type": "update", "_index": "i", "_id": 42, "doc": {"answer": 42}},
    ]
    for ok, item in helpers.streaming_bulk(sync_client, docs):
        assert ok

    assert not sync_client.exists(index="i", id=45)
    assert {"answer": 42} == sync_client.get(index="i", id=42)["_source"]
    assert {"f": "v"} == sync_client.get(index="i", id=47)["_source"]


def test_bulk_transport_error_can_becaught(sync_client):
    failing_client = FailingBulkClient(sync_client)
    docs = [
        {"_index": "i", "_id": 47, "f": "v"},
        {"_index": "i", "_id": 45, "f": "v"},
        {"_index": "i", "_id": 42, "f": "v"},
    ]

    results = list(
        helpers.streaming_bulk(
            failing_client,
            docs,
            raise_on_exception=False,
            raise_on_error=False,
            chunk_size=1,
        )
    )
    assert 3 == len(results)
    assert [True, False, True] == [r[0] for r in results]

    exc = results[1][1]["index"].pop("exception")
    assert isinstance(exc, ApiError)
    assert 599 == exc.status_code
    assert {
        "index": {
            "_index": "i",
            "_id": 45,
            "data": {"f": "v"},
            "error": "ApiError(599, 'Error!')",
            "status": 599,
        }
    } == results[1][1]


def test_bulk_rejected_documents_are_retried(sync_client):
    failing_client = FailingBulkClient(
        sync_client,
        fail_with=ApiError(
            message="Rejected!",
            body={},
            meta=ApiResponseMeta(
                status=429, headers={}, http_version="1.1", duration=0, node=None
            ),
        ),
    )
    docs = [
        {"_index": "i", "_id": 47, "f": "v"},
        {"_index": "i", "_id": 45, "f": "v"},
        {"_index": "i", "_id": 42, "f": "v"},
    ]

    results = list(
        helpers.streaming_bulk(
            failing_client,
            docs,
            index="i",
            raise_on_exception=False,
            raise_on_error=False,
            chunk_size=1,
            max_retries=1,
            initial_backoff=0,
        )
    )
    assert 3 == len(results)
    print(results)
    assert [True, True, True] == [r[0] for r in results]
    sync_client.indices.refresh(index="i")
    res = sync_client.search(index="i")
    assert {"value": 3, "relation": "eq"} == res["hits"]["total"]
    assert 4 == failing_client._called


@pytest.mark.parametrize("use_bytes", [False, True])
def test_bulk_rejected_documents_are_retried_when_bytes_or_string(
    sync_client, use_bytes
):
    failing_client = FailingBulkClient(
        sync_client,
        fail_with=ApiError(
            message="Rejected!",
            body={},
            meta=ApiResponseMeta(
                status=429, headers={}, http_version="1.1", duration=0, node=None
            ),
        ),
    )
    docs = [json.dumps({"field": x}, separators=(",", ":")) for x in range(3)]
    if use_bytes:
        docs = [doc.encode() for doc in docs]

    results = list(
        helpers.streaming_bulk(
            failing_client,
            docs,
            index="i",
            raise_on_exception=False,
            raise_on_error=False,
            chunk_size=1,
            max_retries=1,
            initial_backoff=0,
        )
    )
    assert 3 == len(results)
    assert [True, True, True] == [r[0] for r in results]
    sync_client.indices.refresh(index="i")
    res = sync_client.search(index="i")
    assert {"value": 3, "relation": "eq"} == res["hits"]["total"]
    assert 4 == failing_client._called


def test_bulk_rejected_documents_are_retried_at_most_max_retries_times(sync_client):
    failing_client = FailingBulkClient(
        sync_client,
        fail_at=(1, 2),
        fail_with=ApiError(
            message="Rejected!",
            body={},
            meta=ApiResponseMeta(
                status=429, headers={}, http_version="1.1", duration=0, node=None
            ),
        ),
    )

    docs = [
        {"_index": "i", "_id": 47, "f": "v"},
        {"_index": "i", "_id": 45, "f": "v"},
        {"_index": "i", "_id": 42, "f": "v"},
    ]
    results = list(
        helpers.streaming_bulk(
            failing_client,
            docs,
            raise_on_exception=False,
            raise_on_error=False,
            chunk_size=1,
            max_retries=1,
            initial_backoff=0,
        )
    )
    assert 3 == len(results)
    assert [False, True, True] == [r[0] for r in results]
    sync_client.indices.refresh(index="i")
    res = sync_client.search(index="i")
    assert {"value": 2, "relation": "eq"} == res["hits"]["total"]
    assert 4 == failing_client._called


def test_bulk_transport_error_is_raised_with_max_retries(sync_client):
    failing_client = FailingBulkClient(
        sync_client,
        fail_at=(1, 2, 3, 4),
        fail_with=ApiError(
            message="Rejected!",
            body={},
            meta=ApiResponseMeta(
                status=429, headers={}, http_version="1.1", duration=0, node=None
            ),
        ),
    )

    def streaming_bulk():
        results = list(
            helpers.streaming_bulk(
                failing_client,
                [{"a": 42}, {"a": 39}],
                raise_on_exception=True,
                max_retries=3,
                initial_backoff=0,
            )
        )
        return results

    with pytest.raises(ApiError):
        streaming_bulk()
    assert 4 == failing_client._called


def test_connection_timeout_is_retried_with_retry_status_callback(sync_client):
    failing_client = FailingBulkClient(
        sync_client,
        fail_with=ApiError(
            message="Connection timed out!",
            body={},
            meta=ApiResponseMeta(
                status=522, headers={}, http_version="1.1", duration=0, node=None
            ),
        ),
    )
    docs = [
        {"_index": "i", "_id": 47, "f": "v"},
        {"_index": "i", "_id": 45, "f": "v"},
        {"_index": "i", "_id": 42, "f": "v"},
    ]

    results = list(
        helpers.streaming_bulk(
            failing_client,
            docs,
            index="i",
            raise_on_exception=False,
            raise_on_error=False,
            chunk_size=1,
            retry_on_status=522,
            max_retries=1,
            initial_backoff=0,
        )
    )
    assert 3 == len(results)
    print(results)
    assert [True, True, True] == [r[0] for r in results]
    sync_client.indices.refresh(index="i")
    res = sync_client.search(index="i")
    assert {"value": 3, "relation": "eq"} == res["hits"]["total"]
    assert 4 == failing_client._called


def test_bulk_works_with_single_item(sync_client):
    docs = [{"answer": 42, "_id": 1}]
    success, failed = helpers.bulk(sync_client, docs, index="test-index", refresh=True)

    assert 1 == success
    assert not failed
    assert 1 == sync_client.count(index="test-index")["count"]
    assert {"answer": 42} == sync_client.get(index="test-index", id=1)["_source"]


def test_all_documents_get_inserted(sync_client):
    docs = [{"answer": x, "_id": x} for x in range(100)]
    success, failed = helpers.bulk(sync_client, docs, index="test-index", refresh=True)

    assert 100 == success
    assert not failed
    assert 100 == sync_client.count(index="test-index")["count"]
    assert {"answer": 42} == sync_client.get(index="test-index", id=42)["_source"]


def test_stats_only_reports_numbers(sync_client):
    docs = [{"answer": x} for x in range(100)]
    success, failed = helpers.bulk(
        sync_client, docs, index="test-index", refresh=True, stats_only=True
    )

    assert 100 == success
    assert 0 == failed
    assert 100 == sync_client.count(index="test-index")["count"]


def test_errors_are_reported_correctly(sync_client):
    sync_client.indices.create(
        index="i",
        mappings={"properties": {"a": {"type": "integer"}}},
        settings={"number_of_shards": 1, "number_of_replicas": 0},
    )

    success, failed = helpers.bulk(
        sync_client,
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
    assert error["index"]["error"]["type"] == "document_parsing_exception"


def test_error_is_raised(sync_client):
    sync_client.indices.create(
        index="i",
        mappings={"properties": {"a": {"type": "integer"}}},
        settings={"number_of_shards": 1, "number_of_replicas": 0},
    )

    with pytest.raises(helpers.BulkIndexError):
        helpers.bulk(
            sync_client,
            [{"a": 42}, {"a": "c"}],
            index="i",
        )


def test_ignore_error_if_raised(sync_client):
    # ignore the status code 400 in tuple
    helpers.bulk(sync_client, [{"a": 42}, {"a": "c"}], index="i", ignore_status=(400,))

    # ignore the status code 400 in list
    helpers.bulk(
        sync_client,
        [{"a": 42}, {"a": "c"}],
        index="i",
        ignore_status=[
            400,
        ],
    )

    # ignore the status code 400
    helpers.bulk(sync_client, [{"a": 42}, {"a": "c"}], index="i", ignore_status=400)

    # ignore only the status code in the `ignore_status` argument
    with pytest.raises(helpers.BulkIndexError):
        helpers.bulk(
            sync_client,
            [{"a": 42}, {"a": "c"}],
            index="i",
            ignore_status=(444,),
        )

    # ignore transport error exception
    failing_client = FailingBulkClient(sync_client)
    helpers.bulk(failing_client, [{"a": 42}], index="i", ignore_status=(599,))


def test_errors_are_collected_properly(sync_client):
    sync_client.indices.create(
        index="i",
        mappings={"properties": {"a": {"type": "integer"}}},
        settings={"number_of_shards": 1, "number_of_replicas": 0},
    )

    success, failed = helpers.bulk(
        sync_client,
        [{"a": 42}, {"a": "c"}],
        index="i",
        stats_only=True,
        raise_on_error=False,
    )
    assert 1 == success
    assert 1 == failed


mock_scroll_responses = [
    ObjectApiResponse(
        meta=None,
        raw={
            "_scroll_id": "dummy_id",
            "_shards": {"successful": 4, "total": 5, "skipped": 0},
            "hits": {"hits": [{"scroll_data": 42}]},
        },
    ),
    ObjectApiResponse(
        meta=None,
        raw={
            "_scroll_id": "dummy_id",
            "_shards": {"successful": 4, "total": 5, "skipped": 0},
            "hits": {"hits": []},
        },
    ),
]


@pytest.fixture(scope="function")
def scan_teardown(sync_client):
    yield
    sync_client.clear_scroll(scroll_id="_all")


@pytest.mark.usefixtures("scan_teardown")
def test_order_can_be_preserved(sync_client):
    bulk = []
    for x in range(100):
        bulk.append({"index": {"_index": "test_index", "_id": x}})
        bulk.append({"answer": x, "correct": x == 42})
    sync_client.bulk(operations=bulk, refresh=True)

    docs = list(
        helpers.scan(
            sync_client,
            index="test_index",
            query={"sort": "answer"},
            preserve_order=True,
        )
    )

    assert 100 == len(docs)
    assert list(map(str, range(100))) == list(d["_id"] for d in docs)
    assert list(range(100)) == list(d["_source"]["answer"] for d in docs)


@pytest.mark.usefixtures("scan_teardown")
def test_all_documents_are_read(sync_client):
    bulk = []
    for x in range(100):
        bulk.append({"index": {"_index": "test_index", "_id": x}})
        bulk.append({"answer": x, "correct": x == 42})
    sync_client.bulk(operations=bulk, refresh=True)

    docs = list(helpers.scan(sync_client, index="test_index", size=2))

    assert 100 == len(docs)
    assert set(map(str, range(100))) == {d["_id"] for d in docs}
    assert set(range(100)) == {d["_source"]["answer"] for d in docs}


@pytest.mark.usefixtures("scan_teardown")
def test_scroll_error(sync_client):
    bulk = []
    for x in range(4):
        bulk.append({"index": {"_index": "test_index"}})
        bulk.append({"value": x})
    sync_client.bulk(operations=bulk, refresh=True)

    with patch.object(sync_client, "options", return_value=sync_client), patch.object(
        sync_client, "scroll"
    ) as scroll_mock:
        scroll_mock.side_effect = mock_scroll_responses
        data = list(
            helpers.scan(
                sync_client,
                index="test_index",
                size=2,
                raise_on_error=False,
                clear_scroll=False,
            )
        )
        assert len(data) == 3
        assert data[-1] == {"scroll_data": 42}

        scroll_mock.side_effect = mock_scroll_responses
        with pytest.raises(ScanError):
            data = list(
                helpers.scan(
                    sync_client,
                    index="test_index",
                    size=2,
                    raise_on_error=True,
                    clear_scroll=False,
                )
            )
        assert len(data) == 3
        assert data[-1] == {"scroll_data": 42}


def test_initial_search_error(sync_client):
    with patch.object(
        sync_client,
        "search",
        return_value=ObjectApiResponse(
            meta=None,
            raw={
                "_scroll_id": "dummy_id",
                "_shards": {"successful": 4, "total": 5, "skipped": 0},
                "hits": {"hits": [{"search_data": 1}]},
            },
        ),
    ), patch.object(sync_client, "options", return_value=sync_client):
        with patch.object(sync_client, "scroll") as scroll_mock, patch.object(
            sync_client, "clear_scroll"
        ) as clear_scroll_mock:
            scroll_mock.side_effect = mock_scroll_responses
            data = list(
                helpers.scan(
                    sync_client, index="test_index", size=2, raise_on_error=False
                )
            )
            assert data == [{"search_data": 1}, {"scroll_data": 42}]

            # Scrolled at least once and received a scroll_id to clear.
            scroll_mock.assert_called_with(
                scroll_id="dummy_id",
                scroll="5m",
            )
            clear_scroll_mock.assert_called_once_with(
                scroll_id="dummy_id",
            )

        with patch.object(sync_client, "scroll") as scroll_mock, patch.object(
            sync_client, "clear_scroll"
        ) as clear_scroll_mock:
            scroll_mock.side_effect = mock_scroll_responses
            with pytest.raises(ScanError):
                data = list(
                    helpers.scan(
                        sync_client, index="test_index", size=2, raise_on_error=True
                    )
                )
                assert data == [{"search_data": 1}]

            # Never scrolled but did receive a scroll_id to clear.
            scroll_mock.assert_not_called()
            clear_scroll_mock.assert_called_once_with(
                scroll_id="dummy_id",
            )


def test_no_scroll_id_fast_route(sync_client):
    with patch.object(
        sync_client,
        "search",
        return_value=ObjectApiResponse(meta=None, raw={"no": "_scroll_id"}),
    ) as search_mock, patch.object(sync_client, "scroll") as scroll_mock, patch.object(
        sync_client, "clear_scroll"
    ) as clear_scroll_mock, patch.object(
        sync_client, "options", return_value=sync_client
    ) as options:
        data = list(helpers.scan(sync_client, index="test_index"))

        assert data == []
        search_mock.assert_called_once_with(
            sort="_doc",
            scroll="5m",
            size=1000,
            index="test_index",
        )
        options.assert_called_once_with(request_timeout=None)
        scroll_mock.assert_not_called()
        clear_scroll_mock.assert_not_called()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"api_key": ("name", "value")},
        {"http_auth": ("username", "password")},
        {"basic_auth": ("username", "password")},
        {"bearer_auth": "token"},
        {"headers": {"custom", "header"}},
    ],
)
@pytest.mark.usefixtures("scan_teardown")
def test_scan_auth_kwargs_forwarded(sync_client, kwargs):
    ((key, val),) = kwargs.items()

    with patch.object(
        sync_client, "options", return_value=sync_client
    ) as options, patch.object(
        sync_client,
        "search",
        return_value=ObjectApiResponse(
            meta=None,
            raw={
                "_scroll_id": "scroll_id",
                "_shards": {"successful": 5, "total": 5, "skipped": 0},
                "hits": {"hits": [{"search_data": 1}]},
            },
        ),
    ), patch.object(
        sync_client,
        "scroll",
        return_value=ObjectApiResponse(
            meta=None,
            raw={
                "_scroll_id": "scroll_id",
                "_shards": {"successful": 5, "total": 5, "skipped": 0},
                "hits": {"hits": []},
            },
        ),
    ), patch.object(
        sync_client, "clear_scroll", return_value=ObjectApiResponse(meta=None, raw={})
    ):
        data = list(helpers.scan(sync_client, index="test_index", **kwargs))

        assert data == [{"search_data": 1}]

    assert options.call_args_list == [
        call(
            request_timeout=None, **{key if key != "http_auth" else "basic_auth": val}
        ),
        call(ignore_status=404),
    ]


def test_scan_auth_kwargs_favor_scroll_kwargs_option(sync_client):
    with patch.object(
        sync_client, "options", return_value=sync_client
    ) as options_mock, patch.object(
        sync_client,
        "search",
        return_value=ObjectApiResponse(
            raw={
                "_scroll_id": "scroll_id",
                "_shards": {"successful": 5, "total": 5, "skipped": 0},
                "hits": {"hits": [{"search_data": 1}]},
            },
            meta=None,
        ),
    ) as search_mock, patch.object(
        sync_client,
        "scroll",
        return_value=ObjectApiResponse(
            raw={
                "_scroll_id": "scroll_id",
                "_shards": {"successful": 5, "total": 5, "skipped": 0},
                "hits": {"hits": []},
            },
            meta=None,
        ),
    ) as scroll_mock, patch.object(
        sync_client, "clear_scroll", return_value=ObjectApiResponse(raw={}, meta=None)
    ):
        data = list(
            helpers.scan(
                sync_client,
                index="test_index",
                scroll_kwargs={"headers": {"scroll": "kwargs"}, "sort": "asc"},
                headers={"not scroll": "kwargs"},
            )
        )

        assert data == [{"search_data": 1}]

        # Assert that we see 'scroll_kwargs' options used instead of 'kwargs'
        assert options_mock.call_args_list == [
            call(request_timeout=None, headers={"not scroll": "kwargs"}),
            call(headers={"scroll": "kwargs"}),
            call(ignore_status=404),
        ]
        search_mock.assert_called_once_with(
            sort="_doc", index="test_index", scroll="5m", size=1000
        )
        scroll_mock.assert_called_once_with(
            scroll_id="scroll_id", scroll="5m", sort="asc"
        )


def test_log_warning_on_shard_failures(sync_client):
    bulk = []
    for x in range(4):
        bulk.append({"index": {"_index": "test_index"}})
        bulk.append({"value": x})
    sync_client.bulk(operations=bulk, refresh=True)

    with patch("elasticsearch.helpers.actions.logger") as logger_mock, patch.object(
        sync_client, "options", return_value=sync_client
    ), patch.object(sync_client, "scroll") as scroll_mock:
        scroll_mock.side_effect = mock_scroll_responses
        list(
            helpers.scan(
                sync_client,
                index="test_index",
                size=2,
                raise_on_error=False,
                clear_scroll=False,
            )
        )
        logger_mock.warning.assert_called()

        scroll_mock.side_effect = mock_scroll_responses
        try:
            list(
                helpers.scan(
                    sync_client,
                    index="test_index",
                    size=2,
                    raise_on_error=True,
                    clear_scroll=False,
                )
            )
        except ScanError:
            pass
        logger_mock.warning.assert_called()


def test_clear_scroll(sync_client):
    bulk = []
    for x in range(4):
        bulk.append({"index": {"_index": "test_index"}})
        bulk.append({"value": x})
    sync_client.bulk(operations=bulk, refresh=True)

    with patch.object(sync_client, "options", return_value=sync_client), patch.object(
        sync_client, "clear_scroll", wraps=sync_client.clear_scroll
    ) as clear_scroll_mock:
        list(helpers.scan(sync_client, index="test_index", size=2))
        clear_scroll_mock.assert_called_once()

        clear_scroll_mock.reset_mock()
        list(helpers.scan(sync_client, index="test_index", size=2, clear_scroll=True))
        clear_scroll_mock.assert_called_once()

        clear_scroll_mock.reset_mock()
        list(helpers.scan(sync_client, index="test_index", size=2, clear_scroll=False))
        clear_scroll_mock.assert_not_called()


def test_shards_no_skipped_field(sync_client):
    # Test that scan doesn't fail if 'hits.skipped' isn't available.
    with patch.object(sync_client, "options", return_value=sync_client), patch.object(
        sync_client,
        "search",
        return_value=ObjectApiResponse(
            raw={
                "_scroll_id": "dummy_id",
                "_shards": {"successful": 5, "total": 5},
                "hits": {"hits": [{"search_data": 1}]},
            },
            meta=None,
        ),
    ), patch.object(sync_client, "scroll") as scroll_mock, patch.object(
        sync_client, "clear_scroll"
    ):
        scroll_mock.side_effect = [
            ObjectApiResponse(
                raw={
                    "_scroll_id": "dummy_id",
                    "_shards": {"successful": 5, "total": 5},
                    "hits": {"hits": [{"scroll_data": 42}]},
                },
                meta=None,
            ),
            ObjectApiResponse(
                raw={
                    "_scroll_id": "dummy_id",
                    "_shards": {"successful": 5, "total": 5},
                    "hits": {"hits": []},
                },
                meta=None,
            ),
        ]

        data = list(
            helpers.scan(sync_client, index="test_index", size=2, raise_on_error=True)
        )
        assert data == [{"search_data": 1}, {"scroll_data": 42}]


@pytest.mark.parametrize(
    "scan_kwargs",
    [
        {"from": 1},
        {"from_": 1},
        {"query": {"from": 1}},
        {"query": {"from_": 1}},
        {"query": {"query": {"match_all": {}}}, "from": 1},
        {"query": {"query": {"match_all": {}}}, "from_": 1},
    ],
)
def test_scan_from_keyword_is_aliased(sync_client, scan_kwargs):
    with patch.object(sync_client, "options", return_value=sync_client), patch.object(
        sync_client,
        "search",
        return_value=ObjectApiResponse(
            raw={
                "_scroll_id": "dummy_id",
                "_shards": {"successful": 5, "total": 5},
                "hits": {"hits": []},
            },
            meta=None,
        ),
    ) as search_mock, patch.object(sync_client, "clear_scroll"):
        list(helpers.scan(sync_client, index="test_index", **scan_kwargs))
        assert search_mock.call_args[1]["from_"] == 1
        assert "from" not in search_mock.call_args[1]


@pytest.fixture(scope="function")
def reindex_setup(sync_client):
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
    sync_client.bulk(operations=bulk, refresh=True)


@pytest.mark.usefixtures("reindex_setup")
def test_reindex_passes_kwargs_to_scan_and_bulk(sync_client):
    helpers.reindex(
        sync_client,
        "test_index",
        "prod_index",
        scan_kwargs={"q": "type:answers"},
        bulk_kwargs={"refresh": True},
    )

    assert sync_client.indices.exists(index="prod_index")
    assert 50 == sync_client.count(index="prod_index", q="type:answers")["count"]

    assert {"answer": 42, "correct": True, "type": "answers"} == sync_client.get(
        index="prod_index", id=42
    )["_source"]


@pytest.mark.usefixtures("reindex_setup")
def test_reindex_accepts_a_query(sync_client):
    helpers.reindex(
        sync_client,
        "test_index",
        "prod_index",
        query={"query": {"bool": {"filter": {"term": {"type": "answers"}}}}},
    )
    sync_client.indices.refresh()

    assert sync_client.indices.exists(index="prod_index")
    assert 50 == sync_client.count(index="prod_index", q="type:answers")["count"]

    assert {"answer": 42, "correct": True, "type": "answers"} == sync_client.get(
        index="prod_index", id=42
    )["_source"]


@pytest.mark.usefixtures("reindex_setup")
def test_all_documents_get_moved(sync_client):
    helpers.reindex(sync_client, "test_index", "prod_index")
    sync_client.indices.refresh()

    assert sync_client.indices.exists(index="prod_index")
    assert 50 == sync_client.count(index="prod_index", q="type:questions")["count"]
    assert 50 == sync_client.count(index="prod_index", q="type:answers")["count"]

    assert {"answer": 42, "correct": True, "type": "answers"} == sync_client.get(
        index="prod_index", id=42
    )["_source"]


@pytest.fixture(scope="function")
def parent_child_reindex_setup(sync_client):
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
    sync_client.indices.create(index="test-index", body=body)
    sync_client.indices.create(index="real-index", body=body)

    sync_client.index(index="test-index", id=42, body={"question_answer": "question"})
    sync_client.index(
        index="test-index",
        id=47,
        routing=42,
        body={"some": "data", "question_answer": {"name": "answer", "parent": 42}},
    )
    sync_client.indices.refresh(index="test-index")


@pytest.mark.usefixtures("parent_child_reindex_setup")
def test_children_are_reindexed_correctly(sync_client):
    helpers.reindex(sync_client, "test-index", "real-index")

    q = sync_client.get(index="real-index", id=42)
    assert {
        "_id": "42",
        "_index": "real-index",
        "_primary_term": 1,
        "_seq_no": 0,
        "_source": {"question_answer": "question"},
        "_version": 1,
        "found": True,
    } == q
    q = sync_client.get(index="test-index", id=47, routing=42)
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


@pytest.fixture(scope="function")
def reindex_data_stream_setup(sync_client):
    dt = datetime.now(tz=tz.UTC)
    bulk = []
    for x in range(100):
        bulk.append({"index": {"_index": "test_index_stream", "_id": x}})
        bulk.append(
            {
                "answer": x,
                "correct": x == 42,
                "type": "answers" if x % 2 == 0 else "questions",
                "@timestamp": (dt - timedelta(days=x)).isoformat(),
            }
        )
    sync_client.bulk(operations=bulk, refresh=True)
    sync_client.indices.put_index_template(
        name="my-index-template",
        body={
            "index_patterns": ["py-*-*"],
            "data_stream": {},
        },
    )
    sync_client.indices.create_data_stream(name="py-test-stream")
    sync_client.indices.refresh()


@pytest.mark.usefixtures("reindex_data_stream_setup")
@pytest.mark.parametrize("op_type", [None, "create"])
def test_reindex_index_datastream(op_type, sync_client):
    helpers.reindex(
        sync_client,
        source_index="test_index_stream",
        target_index="py-test-stream",
        query={"query": {"bool": {"filter": {"term": {"type": "answers"}}}}},
        op_type=op_type,
    )
    sync_client.indices.refresh()
    assert sync_client.indices.exists(index="py-test-stream")
    assert 50 == sync_client.count(index="py-test-stream", q="type:answers")["count"]


@pytest.mark.usefixtures("reindex_data_stream_setup")
def test_reindex_index_datastream_op_type_index(sync_client):
    with pytest.raises(
        ValueError, match="Data streams must have 'op_type' set to 'create'"
    ):
        helpers.reindex(
            sync_client,
            source_index="test_index_stream",
            target_index="py-test-stream",
            query={"query": {"bool": {"filter": {"term": {"type": "answers"}}}}},
            op_type="_index",
        )

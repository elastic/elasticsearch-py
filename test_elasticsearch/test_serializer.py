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

import uuid
from datetime import datetime
from decimal import Decimal

import pytest

try:
    import pyarrow as pa

    from elasticsearch.serializer import PyArrowSerializer
except ImportError:
    pa = None

try:
    import numpy as np
    import pandas as pd
except ImportError:
    np = pd = None

import re

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import SerializationError
from elasticsearch.serializer import JSONSerializer, OrjsonSerializer, TextSerializer

requires_numpy_and_pandas = pytest.mark.skipif(
    np is None or pd is None, reason="Test requires numpy and pandas to be available"
)


@pytest.fixture(params=[JSONSerializer, OrjsonSerializer])
def json_serializer(request: pytest.FixtureRequest):
    yield request.param()


def test_datetime_serialization(json_serializer):
    assert b'{"d":"2010-10-01T02:30:00"}' == json_serializer.dumps(
        {"d": datetime(2010, 10, 1, 2, 30)}
    )


@requires_numpy_and_pandas
def test_decimal_serialization(json_serializer):
    assert b'{"d":3.8}' == json_serializer.dumps({"d": Decimal("3.8")})


def test_uuid_serialization(json_serializer):
    assert b'{"d":"00000000-0000-0000-0000-000000000003"}' == json_serializer.dumps(
        {"d": uuid.UUID("00000000-0000-0000-0000-000000000003")}
    )


@requires_numpy_and_pandas
def test_serializes_numpy_bool(json_serializer):
    assert b'{"d":true}' == json_serializer.dumps({"d": np.bool_(True)})


@requires_numpy_and_pandas
def test_serializes_numpy_integers(json_serializer):
    for np_type in (
        np.int_,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
    ):
        assert json_serializer.dumps({"d": np_type(-1)}) == b'{"d":-1}'

    for np_type in (
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
    ):
        assert json_serializer.dumps({"d": np_type(1)}) == b'{"d":1}'


@requires_numpy_and_pandas
def test_serializes_numpy_floats(json_serializer):
    for np_type in (
        np.float32,
        np.float64,
    ):
        assert re.search(
            rb'^{"d":1\.2[\d]*}$', json_serializer.dumps({"d": np_type(1.2)})
        )


@requires_numpy_and_pandas
def test_serializes_numpy_datetime(json_serializer):
    assert b'{"d":"2010-10-01T02:30:00"}' == json_serializer.dumps(
        {"d": np.datetime64("2010-10-01T02:30:00")}
    )


@requires_numpy_and_pandas
def test_serializes_numpy_ndarray(json_serializer):
    assert b'{"d":[0,0,0,0,0]}' == json_serializer.dumps(
        {"d": np.zeros((5,), dtype=np.uint8)}
    )
    # This isn't useful for Elasticsearch, just want to make sure it works.
    assert b'{"d":[[0,0],[0,0]]}' == json_serializer.dumps(
        {"d": np.zeros((2, 2), dtype=np.uint8)}
    )


@requires_numpy_and_pandas
def test_serializes_numpy_nan_to_nan():
    assert b'{"d":NaN}' == JSONSerializer().dumps({"d": float("NaN")})
    # NaN is invalid JSON, and orjson silently converts it to null
    assert b'{"d":null}' == OrjsonSerializer().dumps({"d": float("NaN")})


@requires_numpy_and_pandas
def test_serializes_pandas_timestamp(json_serializer):
    assert b'{"d":"2010-10-01T02:30:00"}' == json_serializer.dumps(
        {"d": pd.Timestamp("2010-10-01T02:30:00")}
    )


@requires_numpy_and_pandas
def test_serializes_pandas_series(json_serializer):
    assert b'{"d":["a","b","c","d"]}' == json_serializer.dumps(
        {"d": pd.Series(["a", "b", "c", "d"])}
    )


@requires_numpy_and_pandas
@pytest.mark.skipif(not hasattr(pd, "NA"), reason="pandas.NA is required")
def test_serializes_pandas_na(json_serializer):
    assert b'{"d":null}' == json_serializer.dumps({"d": pd.NA})


@requires_numpy_and_pandas
@pytest.mark.skipif(not hasattr(pd, "NaT"), reason="pandas.NaT required")
def test_raises_serialization_error_pandas_nat(json_serializer):
    with pytest.raises(SerializationError):
        json_serializer.dumps({"d": pd.NaT})


@requires_numpy_and_pandas
def test_serializes_pandas_category(json_serializer):
    cat = pd.Categorical(["a", "c", "b", "a"], categories=["a", "b", "c"])
    assert b'{"d":["a","c","b","a"]}' == json_serializer.dumps({"d": cat})

    cat = pd.Categorical([1, 2, 3], categories=[1, 2, 3])
    assert b'{"d":[1,2,3]}' == json_serializer.dumps({"d": cat})


@pytest.mark.skipif(pa is None, reason="Test requires pyarrow to be available")
def test_pyarrow_loads():
    data = [
        pa.array([1, 2, 3, 4]),
        pa.array(["foo", "bar", "baz", None]),
        pa.array([True, None, False, True]),
    ]
    batch = pa.record_batch(data, names=["f0", "f1", "f2"])
    sink = pa.BufferOutputStream()
    with pa.ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)

    serializer = PyArrowSerializer()
    assert serializer.loads(sink.getvalue()).to_pydict() == {
        "f0": [1, 2, 3, 4],
        "f1": ["foo", "bar", "baz", None],
        "f2": [True, None, False, True],
    }


def test_json_raises_serialization_error_on_dump_error(json_serializer):
    with pytest.raises(SerializationError):
        json_serializer.dumps(object())


def test_raises_serialization_error_on_load_error(json_serializer):
    with pytest.raises(SerializationError):
        json_serializer.loads(object())
    with pytest.raises(SerializationError):
        json_serializer.loads("")
    with pytest.raises(SerializationError):
        json_serializer.loads("{{")


def test_strings_are_left_untouched():
    assert b"\xe4\xbd\xa0\xe5\xa5\xbd" == TextSerializer().dumps("你好")


def test_text_raises_serialization_error_on_dump_error():
    with pytest.raises(SerializationError):
        TextSerializer().dumps({})


class TestDeserializer:
    def setup_method(self, _):
        self.serializers = Elasticsearch("http://localhost:9200").transport.serializers

    def test_deserializes_json_by_default(self):
        assert {"some": "data"} == self.serializers.loads('{"some":"data"}')

    @pytest.mark.parametrize("data", ['{"some":"data"}', b'{"some":"data"}'])
    def test_deserializes_text_with_correct_ct(self, data):
        assert '{"some":"data"}' == self.serializers.loads(data, "text/plain")
        assert '{"some":"data"}' == self.serializers.loads(
            data, "text/plain; charset=whatever"
        )

    def test_deserialize_compatibility_header(self):
        for content_type in (
            "application/vnd.elasticsearch+json;compatible-with=7",
            "application/vnd.elasticsearch+json; compatible-with=7",
            "application/vnd.elasticsearch+json;compatible-with=8",
            "application/vnd.elasticsearch+json; compatible-with=8",
        ):
            assert {"some": "data"} == self.serializers.loads(
                '{"some":"data"}', content_type
            )
            assert b'{"some":"data"}' == self.serializers.dumps(
                '{"some":"data"}', content_type
            )

        for content_type in (
            "application/vnd.elasticsearch+x-ndjson;compatible-with=7",
            "application/vnd.elasticsearch+x-ndjson; compatible-with=7",
            "application/vnd.elasticsearch+x-ndjson;compatible-with=8",
            "application/vnd.elasticsearch+x-ndjson; compatible-with=8",
        ):
            assert b'{"some":"data"}\n{"some":"data"}\n' == self.serializers.dumps(
                ['{"some":"data"}', {"some": "data"}], content_type
            )
            assert [{"some": "data"}, {"some": "data"}] == self.serializers.loads(
                b'{"some":"data"}\n{"some":"data"}\n', content_type
            )

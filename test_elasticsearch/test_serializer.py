# -*- coding: utf-8 -*-
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

import sys
import uuid
from datetime import datetime
from decimal import Decimal

import pytest

try:
    import numpy as np
    import pandas as pd
except ImportError:
    np = pd = None

import re

from elasticsearch.exceptions import ImproperlyConfigured, SerializationError
from elasticsearch.serializer import (
    DEFAULT_SERIALIZERS,
    Deserializer,
    JSONSerializer,
    TextSerializer,
)

requires_numpy_and_pandas = pytest.mark.skipif(
    np is None or pd is None, reason="Test requires numpy or pandas to be available"
)


def test_datetime_serialization():
    assert '{"d":"2010-10-01T02:30:00"}' == JSONSerializer().dumps(
        {"d": datetime(2010, 10, 1, 2, 30)}
    )


def test_decimal_serialization():
    requires_numpy_and_pandas()

    if sys.version_info[:2] == (2, 6):
        pytest.skip("Float rounding is broken in 2.6.")
    assert '{"d":3.8}' == JSONSerializer().dumps({"d": Decimal("3.8")})


def test_uuid_serialization():
    assert '{"d":"00000000-0000-0000-0000-000000000003"}' == JSONSerializer().dumps(
        {"d": uuid.UUID("00000000-0000-0000-0000-000000000003")}
    )


@requires_numpy_and_pandas
def test_serializes_numpy_bool():
    assert '{"d":true}' == JSONSerializer().dumps({"d": np.bool_(True)})


@requires_numpy_and_pandas
def test_serializes_numpy_integers():
    ser = JSONSerializer()
    for np_type in (
        np.int_,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
    ):
        assert ser.dumps({"d": np_type(-1)}) == '{"d":-1}'

    for np_type in (
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
    ):
        assert ser.dumps({"d": np_type(1)}) == '{"d":1}'


@requires_numpy_and_pandas
def test_serializes_numpy_floats():
    ser = JSONSerializer()
    for np_type in (
        np.float_,
        np.float32,
        np.float64,
    ):
        assert re.search(r'^\{"d":1\.2[\d]*}$', ser.dumps({"d": np_type(1.2)}))


@requires_numpy_and_pandas
def test_serializes_numpy_datetime():
    assert '{"d":"2010-10-01T02:30:00"}' == JSONSerializer().dumps(
        {"d": np.datetime64("2010-10-01T02:30:00")}
    )


@requires_numpy_and_pandas
def test_serializes_numpy_ndarray():
    assert '{"d":[0,0,0,0,0]}' == JSONSerializer().dumps(
        {"d": np.zeros((5,), dtype=np.uint8)}
    )
    # This isn't useful for Elasticsearch, just want to make sure it works.
    assert '{"d":[[0,0],[0,0]]}' == JSONSerializer().dumps(
        {"d": np.zeros((2, 2), dtype=np.uint8)}
    )


@requires_numpy_and_pandas
def test_serializes_numpy_nan_to_nan():
    assert '{"d":NaN}' == JSONSerializer().dumps({"d": np.nan})


@requires_numpy_and_pandas
def test_serializes_pandas_timestamp():
    assert '{"d":"2010-10-01T02:30:00"}' == JSONSerializer().dumps(
        {"d": pd.Timestamp("2010-10-01T02:30:00")}
    )


@requires_numpy_and_pandas
def test_serializes_pandas_series():
    assert '{"d":["a","b","c","d"]}' == JSONSerializer().dumps(
        {"d": pd.Series(["a", "b", "c", "d"])}
    )


@requires_numpy_and_pandas
@pytest.mark.skipif(not hasattr(pd, "NA"), reason="pandas.NA is required")
def test_serializes_pandas_na():
    assert '{"d":null}' == JSONSerializer().dumps({"d": pd.NA})


@requires_numpy_and_pandas
@pytest.mark.skipif(not hasattr(pd, "NaT"), reason="pandas.NaT required")
def test_raises_serialization_error_pandas_nat():
    with pytest.raises(SerializationError):
        JSONSerializer().dumps({"d": pd.NaT})


@requires_numpy_and_pandas
def test_serializes_pandas_category():
    cat = pd.Categorical(["a", "c", "b", "a"], categories=["a", "b", "c"])
    assert '{"d":["a","c","b","a"]}' == JSONSerializer().dumps({"d": cat})

    cat = pd.Categorical([1, 2, 3], categories=[1, 2, 3])
    assert '{"d":[1,2,3]}' == JSONSerializer().dumps({"d": cat})


def test_json_raises_serialization_error_on_dump_error():
    with pytest.raises(SerializationError):
        JSONSerializer().dumps(object())


def test_raises_serialization_error_on_load_error():
    with pytest.raises(SerializationError):
        JSONSerializer().loads(object())
    with pytest.raises(SerializationError):
        JSONSerializer().loads("")
    with pytest.raises(SerializationError):
        JSONSerializer().loads("{{")


def test_strings_are_left_untouched():
    assert "你好" == TextSerializer().dumps("你好")


def test_text_raises_serialization_error_on_dump_error():
    with pytest.raises(SerializationError):
        TextSerializer().dumps({})


class TestDeserializer:
    def setup_method(self, _):
        self.de = Deserializer(DEFAULT_SERIALIZERS)

    def test_deserializes_json_by_default(self):
        assert {"some": "data"} == self.de.loads('{"some":"data"}')

    def test_deserializes_text_with_correct_ct(self):
        assert '{"some":"data"}' == self.de.loads('{"some":"data"}', "text/plain")
        assert '{"some":"data"}' == self.de.loads(
            '{"some":"data"}', "text/plain; charset=whatever"
        )

    def test_deserialize_compatibility_header(self):
        for content_type in (
            "application/vnd.elasticsearch+json;compatible-with=7",
            "application/vnd.elasticsearch+json; compatible-with=7",
            "application/vnd.elasticsearch+json;compatible-with=8",
            "application/vnd.elasticsearch+json; compatible-with=8",
        ):
            assert {"some": "data"} == self.de.loads('{"some":"data"}', content_type)

    def test_raises_serialization_error_on_unknown_mimetype(self):
        with pytest.raises(SerializationError):
            self.de.loads("{}", "text/html")

    def test_raises_improperly_configured_when_default_mimetype_cannot_be_deserialized(
        self,
    ):
        with pytest.raises(ImproperlyConfigured):
            Deserializer({})

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

import numpy as np
import pandas as pd

from elasticsearch.exceptions import ImproperlyConfigured, SerializationError
from elasticsearch.serializer import (
    DEFAULT_SERIALIZERS,
    Deserializer,
    JSONSerializer,
    TextSerializer,
)

from .test_cases import SkipTest, TestCase


class TestJSONSerializer(TestCase):
    def test_datetime_serialization(self):
        self.assertEqual(
            '{"d":"2010-10-01T02:30:00"}',
            JSONSerializer().dumps({"d": datetime(2010, 10, 1, 2, 30)}),
        )

    def test_decimal_serialization(self):
        if sys.version_info[:2] == (2, 6):
            raise SkipTest("Float rounding is broken in 2.6.")
        self.assertEqual('{"d":3.8}', JSONSerializer().dumps({"d": Decimal("3.8")}))

    def test_uuid_serialization(self):
        self.assertEqual(
            '{"d":"00000000-0000-0000-0000-000000000003"}',
            JSONSerializer().dumps(
                {"d": uuid.UUID("00000000-0000-0000-0000-000000000003")}
            ),
        )

    def test_serializes_numpy_bool(self):
        self.assertEqual('{"d":true}', JSONSerializer().dumps({"d": np.bool_(True)}))

    def test_serializes_numpy_integers(self):
        ser = JSONSerializer()
        for np_type in (
            np.int_,
            np.int8,
            np.int16,
            np.int32,
            np.int64,
        ):
            self.assertEqual(ser.dumps({"d": np_type(-1)}), '{"d":-1}')

        for np_type in (
            np.uint8,
            np.uint16,
            np.uint32,
            np.uint64,
        ):
            self.assertEqual(ser.dumps({"d": np_type(1)}), '{"d":1}')

    def test_serializes_numpy_floats(self):
        ser = JSONSerializer()
        for np_type in (
            np.float_,
            np.float32,
            np.float64,
        ):
            self.assertRegexpMatches(
                ser.dumps({"d": np_type(1.2)}), r'^\{"d":1\.2[\d]*}$'
            )

    def test_serializes_numpy_datetime(self):
        self.assertEqual(
            '{"d":"2010-10-01T02:30:00"}',
            JSONSerializer().dumps({"d": np.datetime64("2010-10-01T02:30:00")}),
        )

    def test_serializes_numpy_ndarray(self):
        self.assertEqual(
            '{"d":[0,0,0,0,0]}',
            JSONSerializer().dumps({"d": np.zeros((5,), dtype=np.uint8)}),
        )
        # This isn't useful for Elasticsearch, just want to make sure it works.
        self.assertEqual(
            '{"d":[[0,0],[0,0]]}',
            JSONSerializer().dumps({"d": np.zeros((2, 2), dtype=np.uint8)}),
        )

    def test_serializes_numpy_nan_to_nan(self):
        self.assertEqual(
            '{"d":NaN}',
            JSONSerializer().dumps({"d": np.nan}),
        )

    def test_serializes_pandas_timestamp(self):
        self.assertEqual(
            '{"d":"2010-10-01T02:30:00"}',
            JSONSerializer().dumps({"d": pd.Timestamp("2010-10-01T02:30:00")}),
        )

    def test_serializes_pandas_series(self):
        self.assertEqual(
            '{"d":["a","b","c","d"]}',
            JSONSerializer().dumps({"d": pd.Series(["a", "b", "c", "d"])}),
        )

    def test_serializes_pandas_na(self):
        if not hasattr(pd, "NA"):  # pandas.NA added in v1
            raise SkipTest("pandas.NA required")
        self.assertEqual(
            '{"d":null}',
            JSONSerializer().dumps({"d": pd.NA}),
        )

    def test_raises_serialization_error_pandas_nat(self):
        if not hasattr(pd, "NaT"):
            raise SkipTest("pandas.NaT required")
        self.assertRaises(SerializationError, JSONSerializer().dumps, {"d": pd.NaT})

    def test_serializes_pandas_category(self):
        cat = pd.Categorical(["a", "c", "b", "a"], categories=["a", "b", "c"])
        self.assertEqual(
            '{"d":["a","c","b","a"]}',
            JSONSerializer().dumps({"d": cat}),
        )

        cat = pd.Categorical([1, 2, 3], categories=[1, 2, 3])
        self.assertEqual(
            '{"d":[1,2,3]}',
            JSONSerializer().dumps({"d": cat}),
        )

    def test_raises_serialization_error_on_dump_error(self):
        self.assertRaises(SerializationError, JSONSerializer().dumps, object())

    def test_raises_serialization_error_on_load_error(self):
        self.assertRaises(SerializationError, JSONSerializer().loads, object())
        self.assertRaises(SerializationError, JSONSerializer().loads, "")
        self.assertRaises(SerializationError, JSONSerializer().loads, "{{")

    def test_strings_are_left_untouched(self):
        self.assertEqual("你好", JSONSerializer().dumps("你好"))


class TestTextSerializer(TestCase):
    def test_strings_are_left_untouched(self):
        self.assertEqual("你好", TextSerializer().dumps("你好"))

    def test_raises_serialization_error_on_dump_error(self):
        self.assertRaises(SerializationError, TextSerializer().dumps, {})


class TestDeserializer(TestCase):
    def setup_method(self, _):
        self.de = Deserializer(DEFAULT_SERIALIZERS)

    def test_deserializes_json_by_default(self):
        self.assertEqual({"some": "data"}, self.de.loads('{"some":"data"}'))

    def test_deserializes_text_with_correct_ct(self):
        self.assertEqual(
            '{"some":"data"}', self.de.loads('{"some":"data"}', "text/plain")
        )
        self.assertEqual(
            '{"some":"data"}',
            self.de.loads('{"some":"data"}', "text/plain; charset=whatever"),
        )

    def test_deserialize_compatibility_header(self):
        for content_type in (
            "application/vnd.elasticsearch+json;compatible-with=7",
            "application/vnd.elasticsearch+json; compatible-with=7",
            "application/vnd.elasticsearch+json;compatible-with=8",
            "application/vnd.elasticsearch+json; compatible-with=8",
        ):
            self.assertEqual(
                {"some": "data"}, self.de.loads('{"some":"data"}', content_type)
            )

    def test_raises_serialization_error_on_unknown_mimetype(self):
        self.assertRaises(SerializationError, self.de.loads, "{}", "text/html")

    def test_raises_improperly_configured_when_default_mimetype_cannot_be_deserialized(
        self,
    ):
        self.assertRaises(ImproperlyConfigured, Deserializer, {})

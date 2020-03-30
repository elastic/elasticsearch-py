# -*- coding: utf-8 -*-
import sys
import uuid

from datetime import datetime
from decimal import Decimal

import numpy as np
import pandas as pd

from elasticsearch.serializer import (
    JSONSerializer,
    Deserializer,
    DEFAULT_SERIALIZERS,
    TextSerializer,
)
from elasticsearch.exceptions import SerializationError, ImproperlyConfigured

from .test_cases import TestCase, SkipTest


class TestJSONSerializer(TestCase):
    def test_datetime_serialization(self):
        self.assertEquals(
            '{"d":"2010-10-01T02:30:00"}',
            JSONSerializer().dumps({"d": datetime(2010, 10, 1, 2, 30)}),
        )

    def test_decimal_serialization(self):
        if sys.version_info[:2] == (2, 6):
            raise SkipTest("Float rounding is broken in 2.6.")
        self.assertEquals('{"d":3.8}', JSONSerializer().dumps({"d": Decimal("3.8")}))

    def test_uuid_serialization(self):
        self.assertEquals(
            '{"d":"00000000-0000-0000-0000-000000000003"}',
            JSONSerializer().dumps(
                {"d": uuid.UUID("00000000-0000-0000-0000-000000000003")}
            ),
        )

    def test_serializes_numpy_bool(self):
        self.assertEquals('{"d":true}', JSONSerializer().dumps({"d": np.bool_(True)}))

    def test_serializes_numpy_integers(self):
        ser = JSONSerializer()
        for np_type in (
            np.int_,
            np.int8,
            np.int16,
            np.int32,
            np.int64,
        ):
            self.assertEquals(ser.dumps({"d": np_type(-1)}), '{"d":-1}')

        for np_type in (
            np.uint8,
            np.uint16,
            np.uint32,
            np.uint64,
        ):
            self.assertEquals(ser.dumps({"d": np_type(1)}), '{"d":1}')

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
        self.assertEquals(
            '{"d":"2010-10-01T02:30:00"}',
            JSONSerializer().dumps({"d": np.datetime64("2010-10-01T02:30:00")}),
        )

    def test_serializes_numpy_ndarray(self):
        self.assertEquals(
            '{"d":[0,0,0,0,0]}',
            JSONSerializer().dumps({"d": np.zeros((5,), dtype=np.uint8)}),
        )
        # This isn't useful for Elasticsearch, just want to make sure it works.
        self.assertEquals(
            '{"d":[[0,0],[0,0]]}',
            JSONSerializer().dumps({"d": np.zeros((2, 2), dtype=np.uint8)}),
        )

    def test_serializes_pandas_timestamp(self):
        self.assertEquals(
            '{"d":"2010-10-01T02:30:00"}',
            JSONSerializer().dumps({"d": pd.Timestamp("2010-10-01T02:30:00")}),
        )

    def test_serializes_pandas_series(self):
        self.assertEquals(
            '{"d":["a","b","c","d"]}',
            JSONSerializer().dumps({"d": pd.Series(["a", "b", "c", "d"])}),
        )

    def test_serializes_pandas_na(self):
        if not hasattr(pd, "NA"):  # pandas.NA added in v1
            raise SkipTest("pandas.NA required")
        self.assertEquals(
            '{"d":null}', JSONSerializer().dumps({"d": pd.NA}),
        )

    def test_serializes_pandas_category(self):
        cat = pd.Categorical(["a", "c", "b", "a"], categories=["a", "b", "c"])
        self.assertEquals(
            '{"d":["a","c","b","a"]}', JSONSerializer().dumps({"d": cat}),
        )

        cat = pd.Categorical([1, 2, 3], categories=[1, 2, 3])
        self.assertEquals(
            '{"d":[1,2,3]}', JSONSerializer().dumps({"d": cat}),
        )

    def test_raises_serialization_error_on_dump_error(self):
        self.assertRaises(SerializationError, JSONSerializer().dumps, object())

    def test_raises_serialization_error_on_load_error(self):
        self.assertRaises(SerializationError, JSONSerializer().loads, object())
        self.assertRaises(SerializationError, JSONSerializer().loads, "")
        self.assertRaises(SerializationError, JSONSerializer().loads, "{{")

    def test_strings_are_left_untouched(self):
        self.assertEquals("你好", JSONSerializer().dumps("你好"))


class TestTextSerializer(TestCase):
    def test_strings_are_left_untouched(self):
        self.assertEquals("你好", TextSerializer().dumps("你好"))

    def test_raises_serialization_error_on_dump_error(self):
        self.assertRaises(SerializationError, TextSerializer().dumps, {})


class TestDeserializer(TestCase):
    def setUp(self):
        super(TestDeserializer, self).setUp()
        self.de = Deserializer(DEFAULT_SERIALIZERS)

    def test_deserializes_json_by_default(self):
        self.assertEquals({"some": "data"}, self.de.loads('{"some":"data"}'))

    def test_deserializes_text_with_correct_ct(self):
        self.assertEquals(
            '{"some":"data"}', self.de.loads('{"some":"data"}', "text/plain")
        )
        self.assertEquals(
            '{"some":"data"}',
            self.de.loads('{"some":"data"}', "text/plain; charset=whatever"),
        )

    def test_raises_serialization_error_on_unknown_mimetype(self):
        self.assertRaises(SerializationError, self.de.loads, "{}", "text/html")

    def test_raises_improperly_configured_when_default_mimetype_cannot_be_deserialized(
        self,
    ):
        self.assertRaises(ImproperlyConfigured, Deserializer, {})

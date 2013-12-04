# -*- coding: utf-8 -*-
import sys

from datetime import datetime
from decimal import Decimal

from elasticsearch.serializer import JSONSerializer
from elasticsearch.exceptions import SerializationError

from .test_cases import TestCase, SkipTest

class TestJSONSerializer(TestCase):
    def test_datetime_serialization(self):
        self.assertEquals(u'{"d": "2010-10-01T02:30:00"}', JSONSerializer().dumps({'d': datetime(2010, 10, 1, 2, 30)}))

    def test_decimal_serialization(self):
        if sys.version_info[:2] == (2, 6):
            raise SkipTest("Float rounding is broken in 2.6.")
        self.assertEquals(u'{"d": 3.8}', JSONSerializer().dumps({'d': Decimal('3.8')}))

    def test_raises_serialization_error_on_dump_error(self):
        self.assertRaises(SerializationError, JSONSerializer().dumps, object())

    def test_raises_serialization_error_on_load_error(self):
        self.assertRaises(SerializationError, JSONSerializer().loads, object())
        self.assertRaises(SerializationError, JSONSerializer().loads, '')
        self.assertRaises(SerializationError, JSONSerializer().loads, '{{')

    def test_strings_are_left_untouched(self):
        self.assertEquals(u"你好", JSONSerializer().dumps(u"你好"))

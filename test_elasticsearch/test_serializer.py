# -*- coding: utf-8 -*-
import sys

from datetime import datetime
from decimal import Decimal

from elasticsearch.serializer import JSONSerializer, Deserializer, DEFAULT_SERIALIZERS, TextSerializer
from elasticsearch.exceptions import SerializationError, ImproperlyConfigured

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


class TestTextSerializer(TestCase):
    def test_strings_are_left_untouched(self):
        self.assertEquals(u"你好", TextSerializer().dumps(u"你好"))

    def test_raises_serialization_error_on_dump_error(self):
        self.assertRaises(SerializationError, TextSerializer().dumps, {})


class TestDeserializer(TestCase):
    def setUp(self):
        super(TestDeserializer, self).setUp()
        self.de = Deserializer(DEFAULT_SERIALIZERS)

    def test_deserializes_json_by_default(self):
        self.assertEquals({"some": "data"}, self.de.loads('{"some":"data"}'))

    def test_deserializes_text_with_correct_ct(self):
        self.assertEquals('{"some":"data"}', self.de.loads('{"some":"data"}', 'text/plain'))
        self.assertEquals('{"some":"data"}', self.de.loads('{"some":"data"}', 'text/plain; charset=whatever'))

    def test_raises_serialization_error_on_unknown_mimetype(self):
        self.assertRaises(SerializationError, self.de.loads, '{}', 'text/html')

    def test_raises_improperly_configured_when_default_mimetype_cannot_be_deserialized(self):
        self.assertRaises(ImproperlyConfigured, Deserializer, {})

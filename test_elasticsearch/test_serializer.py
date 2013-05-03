from datetime import datetime
from unittest import TestCase

from elasticsearch.serializer import JSONSerializer
from elasticsearch.exceptions import SerializationError

class TestJSONSerializer(TestCase):
    def test_datetime_serialization(self):
        self.assertEquals(u'{"d": "2010-10-01T02:30:00"}', JSONSerializer().dumps({'d': datetime(2010, 10, 1, 2, 30)}))

    def test_raises_serialization_error_on_dump_error(self):
        self.assertRaises(SerializationError, JSONSerializer().dumps, object())

    def test_raises_serialization_error_on_load_error(self):
        self.assertRaises(SerializationError, JSONSerializer().loads, object())
        self.assertRaises(SerializationError, JSONSerializer().loads, '')
        self.assertRaises(SerializationError, JSONSerializer().loads, '{{')

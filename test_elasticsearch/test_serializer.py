from datetime import datetime
from unittest import TestCase

from elasticsearch.serializer import JSONSerializer

class TestJSONSerializer(TestCase):
    def test_datetime_serialization(self):
        self.assertEquals(u'{"d": "2010-10-01T02:30:00"}', JSONSerializer().dumps({'d': datetime(2010, 10, 1, 2, 30)}))

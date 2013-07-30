import json
from datetime import date, datetime

from .exceptions import SerializationError

class JSONSerializer(object):
    def default(self, data):
        if isinstance(data, (date, datetime)):
            return data.isoformat()
        raise TypeError

    def loads(self, s):
        try:
            return json.loads(s)
        except (ValueError, TypeError) as e:
            raise SerializationError(s, e)

    def dumps(self, data):
        # don't serialize strings
        if isinstance(data, (type(''), type(u''))):
            return data

        try:
            return json.dumps(data, default=self.default)
        except (ValueError, TypeError) as e:
            raise SerializationError(data, e)



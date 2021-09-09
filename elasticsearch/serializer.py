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

try:
    import simplejson as json
except ImportError:
    import json

import uuid
from datetime import date, datetime
from decimal import Decimal

from .compat import string_types
from .exceptions import ImproperlyConfigured, SerializationError

INTEGER_TYPES = ()
FLOAT_TYPES = (Decimal,)
TIME_TYPES = (date, datetime)


class Serializer(object):
    mimetype = ""

    def loads(self, s):
        raise NotImplementedError()

    def dumps(self, data):
        raise NotImplementedError()


class TextSerializer(Serializer):
    mimetype = "text/plain"

    def loads(self, s):
        return s

    def dumps(self, data):
        if isinstance(data, string_types):
            return data

        raise SerializationError("Cannot serialize %r into text." % data)


class JSONSerializer(Serializer):
    mimetype = "application/json"

    def default(self, data):
        if isinstance(data, TIME_TYPES):
            # Little hack to avoid importing pandas but to not
            # return 'NaT' string for pd.NaT as that's not a valid
            # Elasticsearch date.
            formatted_data = data.isoformat()
            if formatted_data != "NaT":
                return formatted_data

        if isinstance(data, uuid.UUID):
            return str(data)
        elif isinstance(data, FLOAT_TYPES):
            return float(data)

        # This is kept for backwards compatibility even
        # if 'INTEGER_TYPES' isn't used by default anymore.
        elif INTEGER_TYPES and isinstance(data, INTEGER_TYPES):
            return int(data)

        # Special cases for numpy and pandas types
        # These are expensive to import so we try them last.
        try:
            import numpy as np

            if isinstance(
                data,
                (
                    np.int_,
                    np.intc,
                    np.int8,
                    np.int16,
                    np.int32,
                    np.int64,
                    np.uint8,
                    np.uint16,
                    np.uint32,
                    np.uint64,
                ),
            ):
                return int(data)
            elif isinstance(
                data,
                (
                    np.float_,
                    np.float16,
                    np.float32,
                    np.float64,
                ),
            ):
                return float(data)
            elif isinstance(data, np.bool_):
                return bool(data)
            elif isinstance(data, np.datetime64):
                return data.item().isoformat()
            elif isinstance(data, np.ndarray):
                return data.tolist()
        except ImportError:
            pass

        try:
            import pandas as pd

            if isinstance(data, (pd.Series, pd.Categorical)):
                return data.tolist()
            elif isinstance(data, pd.Timestamp) and data is not getattr(
                pd, "NaT", None
            ):
                return data.isoformat()
            elif data is getattr(pd, "NA", None):
                return None
        except ImportError:
            pass

        raise TypeError("Unable to serialize %r (type: %s)" % (data, type(data)))

    def loads(self, s):
        try:
            return json.loads(s)
        except (ValueError, TypeError) as e:
            raise SerializationError(s, e)

    def dumps(self, data):
        # don't serialize strings
        if isinstance(data, string_types):
            return data

        try:
            return json.dumps(
                data, default=self.default, ensure_ascii=False, separators=(",", ":")
            )
        except (ValueError, TypeError) as e:
            raise SerializationError(data, e)


class MapboxVectorTileSerializer(Serializer):
    mimetype = "application/vnd.mapbox-vector-tile"

    def loads(self, s):
        return s

    def dumps(self, data):
        if isinstance(data, string_types):
            return data

        raise SerializationError("Cannot serialize %r into a MapBox vector tile" % data)


DEFAULT_SERIALIZERS = {
    JSONSerializer.mimetype: JSONSerializer(),
    TextSerializer.mimetype: TextSerializer(),
    MapboxVectorTileSerializer.mimetype: MapboxVectorTileSerializer(),
}


class Deserializer(object):
    def __init__(self, serializers, default_mimetype="application/json"):
        try:
            self.default = serializers[default_mimetype]
        except KeyError:
            raise ImproperlyConfigured(
                "Cannot find default serializer (%s)" % default_mimetype
            )
        self.serializers = serializers

    def loads(self, s, mimetype=None):
        if not mimetype:
            deserializer = self.default
        else:
            # split out 'charset' and 'compatible-width' options
            mimetype = mimetype.partition(";")[0].strip()
            # Treat 'application/vnd.elasticsearch+json'
            # as application/json for compatibility.
            if mimetype == "application/vnd.elasticsearch+json":
                mimetype = "application/json"
            try:
                deserializer = self.serializers[mimetype]
            except KeyError:
                raise SerializationError(
                    "Unknown mimetype, unable to deserialize: %s" % mimetype
                )

        return deserializer.loads(s)

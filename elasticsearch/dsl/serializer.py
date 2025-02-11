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

from typing import Any

from elasticsearch.serializer import JSONSerializer

from .utils import AttrList


class AttrJSONSerializer(JSONSerializer):
    def default(self, data: Any) -> Any:
        if isinstance(data, AttrList):
            return data._l_
        if hasattr(data, "to_dict"):
            return data.to_dict()
        return super().default(data)


serializer = AttrJSONSerializer()

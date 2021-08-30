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

import pytest

from elasticsearch.client import Elasticsearch

from .common import DummyTransport, assert_helper


class TestIndices:
    def test_create_one_index(self):
        client = Elasticsearch(transport_class=DummyTransport)
        client.indices.create("test-index")
        assert_helper(client, "PUT", "/test-index")

    def test_delete_multiple_indices(self):
        client = Elasticsearch(transport_class=DummyTransport)
        client.indices.delete(["test-index", "second.index", "third/index"])
        assert_helper(client, "DELETE", "/test-index,second.index,third%2Findex")

    def test_exists_index(self):
        client = Elasticsearch(transport_class=DummyTransport)
        client.indices.exists("second.index,third/index")
        assert_helper(client, "HEAD", "/second.index,third%2Findex")

    @pytest.mark.parametrize("index", [None, [], ""])
    def test_passing_empty_value_for_required_param_raises_exception(self, index):
        client = Elasticsearch(transport_class=DummyTransport)
        with pytest.raises(ValueError):
            client.indices.exists(index=index)

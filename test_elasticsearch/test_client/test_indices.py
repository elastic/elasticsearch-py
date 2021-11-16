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

from test_elasticsearch.test_cases import DummyTransportTestCase


class TestIndices(DummyTransportTestCase):
    def test_create_one_index(self):
        self.client.indices.create(index="test-index")
        self.assert_url_called("PUT", "/test-index")

    def test_delete_multiple_indices(self):
        self.client.indices.delete(index=["test-index", "second.index", "third/index"])
        self.assert_url_called("DELETE", "/test-index,second.index,third%2Findex")

    def test_exists_index(self):
        self.client.indices.exists(index="second.index,third/index")
        self.assert_url_called("HEAD", "/second.index,third%2Findex")

    def test_passing_empty_value_for_required_param_raises_exception(self):
        with pytest.raises(ValueError):
            self.client.indices.exists(index=None)
        with pytest.raises(ValueError):
            self.client.indices.exists(index=[])
        with pytest.raises(ValueError):
            self.client.indices.exists(index="")

    def test_query_params(self):
        self.client.indices.delete(
            index=["test1", "test*"], expand_wildcards=["open", "closed"]
        )
        self.assert_url_called("DELETE", "/test1,test*?expand_wildcards=open,closed")

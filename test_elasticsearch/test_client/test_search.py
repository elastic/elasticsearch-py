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

from test_elasticsearch.test_cases import ElasticsearchTestCase


class TestSearch(ElasticsearchTestCase):
    def test_search_with_shorthard_sort(self):
        self.client.search(index="test-index", sort="@timestamp:asc")
        calls = self.client.transport.calls
        assert calls == {
            ("POST", "/test-index/_search"): [
                (
                    {"sort": b"@timestamp:asc"},
                    {"accept": "application/json", "content-type": "application/json"},
                    None,
                )
            ]
        }

        calls.clear()
        self.client.search(index="test-index", sort=["@timestamp:asc", "_score:desc"])
        calls = self.client.transport.calls
        assert calls == {
            ("POST", "/test-index/_search"): [
                (
                    {"sort": b"@timestamp:asc,_score:desc"},
                    {"accept": "application/json", "content-type": "application/json"},
                    None,
                )
            ]
        }

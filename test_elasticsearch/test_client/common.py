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

from collections import defaultdict

from elasticsearch.connection import Connection


class DummyTransport(Connection):
    def __init__(self, hosts, **kwargs):
        self.hosts = hosts
        self.responses = kwargs.pop("responses", None)
        self.call_count = 0
        self.calls = defaultdict(list)

    def perform_request(self, method, url, params=None, headers=None, body=None):
        resp = 200, {}
        if self.responses:
            resp = self.responses[self.call_count]
        self.call_count += 1
        self.calls[(method, url)].append((params, headers, body))
        return resp


def assert_helper(client, method, url, count=1):
    calls = client.transport.calls
    assert (method, url) in calls
    assert count == len(calls[(method, url)])
    return calls[(method, url)]

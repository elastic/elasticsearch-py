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
from elasticsearch.utils import _client_meta_version


@pytest.mark.parametrize(
    ["version", "meta_version"],
    [("1.26.3", "1.26.3"), ("7.10.1a1", "7.10.1p"), ("7.10.pre", "7.10p")],
)
def test_client_meta_version(version, meta_version):
    assert _client_meta_version(version) == meta_version

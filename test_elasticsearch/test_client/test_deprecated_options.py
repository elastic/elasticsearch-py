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

import warnings

from elasticsearch import Elasticsearch


def test_sniff_on_connection_fail():
    with warnings.catch_warnings(record=True) as w:
        client = Elasticsearch("http://localhost:9200", sniff_on_connection_fail=True)
    assert client.transport._sniff_on_node_failure is True
    assert len(w) == 1
    assert w[0].category == DeprecationWarning
    assert str(w[0].message) == (
        "The 'sniff_on_connection_fail' parameter is deprecated in favor of 'sniff_on_node_failure'"
    )


def test_sniffer_timeout():
    with warnings.catch_warnings(record=True) as w:
        client = Elasticsearch("http://localhost:9200", sniffer_timeout=1)
    assert client.transport._min_delay_between_sniffing == 1
    assert len(w) == 1
    assert w[0].category == DeprecationWarning
    assert str(w[0].message) == (
        "The 'sniffer_timeout' parameter is deprecated in favor of 'min_delay_between_sniffing'"
    )


def test_randomize_hosts():
    with warnings.catch_warnings(record=True) as w:
        Elasticsearch("http://localhost:9200", randomize_hosts=True)
    assert len(w) == 1
    assert w[0].category == DeprecationWarning
    assert str(w[0].message) == (
        "The 'randomize_hosts' parameter is deprecated in favor of 'randomize_nodes_in_pool'"
    )

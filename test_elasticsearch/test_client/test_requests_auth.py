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

import pytest
import requests
from elastic_transport import RequestsHttpNode, Urllib3HttpNode
from elastic_transport.client_utils import DEFAULT
from requests.auth import HTTPBasicAuth

from elasticsearch import AsyncElasticsearch, Elasticsearch


class CustomRequestHttpNode(RequestsHttpNode):
    pass


class CustomUrllib3HttpNode(Urllib3HttpNode):
    pass


@pytest.mark.parametrize(
    "node_class", ["requests", RequestsHttpNode, CustomRequestHttpNode]
)
def test_requests_auth(node_class):
    http_auth = HTTPBasicAuth("username", "password")

    with warnings.catch_warnings(record=True) as w:
        client = Elasticsearch(
            "http://localhost:9200", http_auth=http_auth, node_class=node_class
        )

    # http_auth is deprecated for all other cases except this one.
    assert len(w) == 0

    # Instance should be forwarded directly to requests.Session.auth.
    node = client.transport.node_pool.get()
    assert isinstance(node, RequestsHttpNode)
    assert isinstance(node.session, requests.Session)
    assert node.session.auth is http_auth


@pytest.mark.parametrize("client_class", [Elasticsearch, AsyncElasticsearch])
@pytest.mark.parametrize(
    "node_class", ["urllib3", "aiohttp", None, DEFAULT, CustomUrllib3HttpNode]
)
def test_error_for_requests_auth_node_class(client_class, node_class):
    http_auth = HTTPBasicAuth("username", "password")

    with pytest.raises(ValueError) as e:
        client_class(
            "http://localhost:9200", http_auth=http_auth, node_class=node_class
        )
    assert str(e.value) == (
        "Using a custom 'requests.auth.AuthBase' class for "
        "'http_auth' must be used with node_class='requests'"
    )


def test_error_for_requests_auth_async():
    http_auth = HTTPBasicAuth("username", "password")

    with pytest.raises(ValueError) as e:
        AsyncElasticsearch(
            "http://localhost:9200", http_auth=http_auth, node_class="requests"
        )
    assert str(e.value) == (
        "Specified 'node_class' is not async, should be async instead"
    )

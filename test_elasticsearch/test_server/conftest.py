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

import os

import pytest

import elasticsearch

from ..utils import CA_CERTS, wipe_cluster

# Information about the Elasticsearch instance running, if any
# Used for
ELASTICSEARCH_VERSION = ""
ELASTICSEARCH_BUILD_HASH = ""
ELASTICSEARCH_REST_API_TESTS = []


def _create(elasticsearch_url, transport=None, node_class=None):
    # Configure the client with certificates
    kw = {}
    if elasticsearch_url.startswith("https://"):
        kw["ca_certs"] = CA_CERTS

    # Optionally configure an HTTP conn class depending on
    # 'PYTHON_CONNECTION_CLASS' env var
    if "PYTHON_CONNECTION_CLASS" in os.environ:
        kw["node_class"] = os.environ["PYTHON_CONNECTION_CLASS"]

    if node_class is not None and "node_class" not in kw:
        kw["node_class"] = node_class

    if transport:
        kw["transport_class"] = transport

    # We do this little dance with the URL to force
    # Requests to respect 'headers: None' within rest API spec tests.
    return elasticsearch.Elasticsearch(elasticsearch_url, **kw)


@pytest.fixture(scope="session")
def sync_client_factory(elasticsearch_url):
    client = None
    try:
        client = _create(elasticsearch_url)

        # Wipe the cluster before we start testing just in case it wasn't wiped
        # cleanly from the previous run of pytest?
        wipe_cluster(client)

        yield client
    finally:
        if client:
            client.close()


@pytest.fixture(scope="function")
def sync_client(sync_client_factory):
    try:
        yield sync_client_factory
    finally:
        # Wipe the cluster clean after every test execution.
        wipe_cluster(sync_client_factory)

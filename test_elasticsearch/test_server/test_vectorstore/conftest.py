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

import uuid

import pytest

from ...utils import wipe_cluster
from ..conftest import _create
from . import RequestSavingTransport


@pytest.fixture(scope="function")
def index() -> str:
    return f"test_{uuid.uuid4().hex}"


@pytest.fixture(scope="function")
def sync_client_request_saving_factory(elasticsearch_url):
    client = None

    try:
        client = _create(elasticsearch_url)
        # Wipe the cluster before we start testing just in case it wasn't wiped
        # cleanly from the previous run of pytest?
        wipe_cluster(client)
    finally:
        client.close()

    try:
        # Recreate client with a transport that saves requests.
        client = _create(elasticsearch_url, RequestSavingTransport)

        yield client
    finally:
        if client:
            client.close()


@pytest.fixture(scope="function")
def sync_client_request_saving(sync_client_request_saving_factory):
    try:
        yield sync_client_request_saving_factory
    finally:
        # Wipe the cluster clean after every test execution.
        wipe_cluster(sync_client_request_saving_factory)

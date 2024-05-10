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

from ...cluster import wipe_cluster
from ..conftest import _create
from . import RequestSavingTransport


@pytest.fixture(scope="function")
def index() -> str:
    return f"test_{uuid.uuid4().hex}"


@pytest.fixture(scope="function")
def es_client_request_saving_factory(elasticsearch_url):
    return _create(elasticsearch_url, RequestSavingTransport)


@pytest.fixture(scope="function")
def es_client_request_saving(es_client_request_saving_factory):
    try:
        yield es_client_request_saving_factory
    finally:
        # Wipe the cluster clean after every test execution.
        wipe_cluster(es_client_request_saving_factory)
        es_client_request_saving_factory.close()

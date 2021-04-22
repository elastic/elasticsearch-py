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
import time

import pytest

import elasticsearch
from elasticsearch.helpers.test import ELASTICSEARCH_URL

from ..utils import wipe_cluster

# Information about the Elasticsearch instance running, if any
# Used for
ELASTICSEARCH_VERSION = ""
ELASTICSEARCH_BUILD_HASH = ""
ELASTICSEARCH_REST_API_TESTS = []


@pytest.fixture(scope="session")
def sync_client_factory():
    client = None
    try:
        # Configure the client with certificates and optionally
        # an HTTP conn class depending on 'PYTHON_CONNECTION_CLASS' envvar
        kw = {"timeout": 3, "ca_certs": ".ci/certs/ca.pem"}
        if "PYTHON_CONNECTION_CLASS" in os.environ:
            from elasticsearch import connection

            kw["connection_class"] = getattr(
                connection, os.environ["PYTHON_CONNECTION_CLASS"]
            )

        client = elasticsearch.Elasticsearch(ELASTICSEARCH_URL, **kw)

        # Wait for the cluster to report a status of 'yellow'
        for _ in range(100):
            try:
                client.cluster.health(wait_for_status="yellow")
                break
            except ConnectionError:
                time.sleep(0.1)
        else:
            pytest.skip("Elasticsearch wasn't running at %r" % (ELASTICSEARCH_URL,))

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
        wipe_cluster(sync_client_factory)

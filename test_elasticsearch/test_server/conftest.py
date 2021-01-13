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

from ..utils import wipe_cluster


@pytest.fixture(scope="function")
def sync_client():
    client = None
    try:
        kw = {
            "timeout": 3,
            "ca_certs": ".ci/certs/ca.pem",
            "connection_class": getattr(
                elasticsearch,
                os.environ.get("PYTHON_CONNECTION_CLASS", "Urllib3HttpConnection"),
            ),
        }

        client = elasticsearch.Elasticsearch(
            [os.environ.get("ELASTICSEARCH_HOST", {})], **kw
        )

        # wait for yellow status
        for _ in range(100):
            try:
                client.cluster.health(wait_for_status="yellow")
                break
            except ConnectionError:
                time.sleep(0.1)
        else:
            # timeout
            pytest.skip("Elasticsearch failed to start.")

        yield client

    finally:
        if client:
            wipe_cluster(client)
            client.close()

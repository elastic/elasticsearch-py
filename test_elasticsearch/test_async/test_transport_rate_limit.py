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

from elastic_transport import ApiResponseMeta, HttpHeaders

from elasticsearch._async.rate_limiter import (
    RateLimitConfig,
    wrap_transport,
)


class DummyRespTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    async def perform_request(self, method, target, **kwargs):
        idx = min(self.calls, len(self.responses) - 1)
        self.calls += 1
        status, headers = self.responses[idx]
        meta = ApiResponseMeta(
            status=status,
            http_version="1.1",
            headers=HttpHeaders(headers or {}),
            duration=0.0,
            node=None,
        )
        return meta, {}


@pytest.mark.asyncio
async def test_retry_after_respected():
    delays = []

    async def fake_sleep(d):
        delays.append(d)

    t = DummyRespTransport([(429, {"Retry-After": "0.1"}), (200, {})])
    rl = wrap_transport(t, RateLimitConfig(max_retries=2), sleep_coro=fake_sleep)
    meta, _ = await rl.perform_request("GET", "/test")
    assert meta.status == 200
    assert len(delays) == 1 and 0.09 <= delays[0] <= 0.11


@pytest.mark.asyncio
async def test_exponential_backoff_jitter_cap():
    delays = []

    async def fake_sleep(d):
        delays.append(d)

    t = DummyRespTransport([(503, {}), (503, {}), (503, {}), (200, {})])
    cfg = RateLimitConfig(
        max_retries=3, backoff_base=0.2, backoff_cap=0.3, respect_retry_after=False, jitter=False
    )
    rl = wrap_transport(t, cfg, sleep_coro=fake_sleep)
    meta, _ = await rl.perform_request("GET", "/test")
    assert meta.status == 200
    assert [round(d, 2) for d in delays] == [0.2, 0.3, 0.3]


@pytest.mark.asyncio
async def test_pass_through_on_success():
    t = DummyRespTransport([(200, {})])
    rl = wrap_transport(t, RateLimitConfig())
    meta, _ = await rl.perform_request("GET", "/ok")
    assert meta.status == 200

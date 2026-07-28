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

from __future__ import annotations

import asyncio
import random
from dataclasses import dataclass
from typing import Any, Mapping, Optional, Set, Callable

from elastic_transport import AsyncTransport


@dataclass(frozen=True)
class RateLimitConfig:
    retry_statuses: Set[int] = frozenset({429, 503})
    max_retries: int = 3
    backoff_base: float = 0.5
    backoff_cap: float = 8.0
    jitter: bool = True
    respect_retry_after: bool = True


def _parse_retry_after(headers: Mapping[str, Any]) -> Optional[float]:
    v = headers.get("retry-after") or headers.get("Retry-After")
    if not v:
        return None
    try:
        return float(v)
    except Exception:
        # Could be an HTTP-date; ignore for simplicity
        return None


class RateLimitedAsyncTransport(AsyncTransport):
    def __init__(
        self,
        *args: Any,
        rate_limit_config: Optional[RateLimitConfig] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._rl_cfg = rate_limit_config or RateLimitConfig()

    async def perform_request(self, method: str, target: str, **kwargs: Any):
        attempt = 0
        while True:
            meta, body = await super().perform_request(method, target, **kwargs)
            status = meta.status
            if (
                200 <= status < 300
                or status not in self._rl_cfg.retry_statuses
                or attempt >= self._rl_cfg.max_retries
            ):
                return meta, body

            delay: Optional[float] = None
            if self._rl_cfg.respect_retry_after:
                delay = _parse_retry_after(meta.headers)

            if delay is None:
                delay = min(
                    self._rl_cfg.backoff_cap,
                    self._rl_cfg.backoff_base * (2 ** attempt),
                )
                if self._rl_cfg.jitter:
                    delay = random.uniform(0.0, float(delay))

            attempt += 1
            await asyncio.sleep(max(0.0, float(delay)))


class RateLimitInterceptor:
    def __init__(
        self,
        transport: AsyncTransport,
        config: Optional[RateLimitConfig] = None,
        *,
        sleep_coro: Callable[[float], "asyncio.Future[None]"] = asyncio.sleep,
        rng: Callable[[float, float], float] = random.uniform,
    ) -> None:
        self._inner = transport
        self._cfg = config or RateLimitConfig()
        self._sleep = sleep_coro
        self._rng = rng

    async def perform_request(self, method: str, target: str, **kwargs: Any):
        attempt = 0
        while True:
            meta, body = await self._inner.perform_request(method, target, **kwargs)
            status = meta.status
            if (
                200 <= status < 300
                or status not in self._cfg.retry_statuses
                or attempt >= self._cfg.max_retries
            ):
                return meta, body

            delay: Optional[float] = None
            if self._cfg.respect_retry_after:
                delay = _parse_retry_after(meta.headers)

            if delay is None:
                delay = min(
                    self._cfg.backoff_cap,
                    self._cfg.backoff_base * (2 ** attempt),
                )
                if self._cfg.jitter:
                    delay = self._rng(0.0, float(delay))

            attempt += 1
            await self._sleep(max(0.0, float(delay)))


def wrap_transport(
    transport: AsyncTransport,
    config: Optional[RateLimitConfig] = None,
    *,
    sleep_coro: Callable[[float], "asyncio.Future[None]"] = asyncio.sleep,
    rng: Callable[[float, float], float] = random.uniform,
) -> RateLimitInterceptor:
    return RateLimitInterceptor(transport, config, sleep_coro=sleep_coro, rng=rng)

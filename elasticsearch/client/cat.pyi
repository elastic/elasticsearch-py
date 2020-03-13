from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class CatClient(NamespacedClient):
    def aliases(
        self,
        *,
        name: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def allocation(
        self,
        *,
        node_id: Optional[Any] = None,
        bytes: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def count(
        self,
        *,
        index: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def health(
        self,
        *,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        ts: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def help(
        self,
        *,
        help: Optional[Any] = None,
        s: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def indices(
        self,
        *,
        index: Optional[Any] = None,
        bytes: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        health: Optional[Any] = None,
        help: Optional[Any] = None,
        include_unloaded_segments: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        pri: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def master(
        self,
        *,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def nodes(
        self,
        *,
        bytes: Optional[Any] = None,
        format: Optional[Any] = None,
        full_id: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def recovery(
        self,
        *,
        index: Optional[Any] = None,
        active_only: Optional[Any] = None,
        bytes: Optional[Any] = None,
        detailed: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def shards(
        self,
        *,
        index: Optional[Any] = None,
        bytes: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def segments(
        self,
        *,
        index: Optional[Any] = None,
        bytes: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def pending_tasks(
        self,
        *,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def thread_pool(
        self,
        *,
        thread_pool_patterns: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        size: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def fielddata(
        self,
        *,
        fields: Optional[Any] = None,
        bytes: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def plugins(
        self,
        *,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def nodeattrs(
        self,
        *,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def repositories(
        self,
        *,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def snapshots(
        self,
        *,
        repository: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def tasks(
        self,
        *,
        actions: Optional[Any] = None,
        detailed: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        node_id: Optional[Any] = None,
        parent_task: Optional[Any] = None,
        s: Optional[Any] = None,
        time: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def templates(
        self,
        *,
        name: Optional[Any] = None,
        format: Optional[Any] = None,
        h: Optional[Any] = None,
        help: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        s: Optional[Any] = None,
        v: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

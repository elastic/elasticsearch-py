from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class ClusterClient(NamespacedClient):
    def health(
        self,
        *,
        index: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        level: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        wait_for_events: Optional[Any] = None,
        wait_for_no_initializing_shards: Optional[Any] = None,
        wait_for_no_relocating_shards: Optional[Any] = None,
        wait_for_nodes: Optional[Any] = None,
        wait_for_status: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def pending_tasks(
        self,
        *,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def state(
        self,
        *,
        metric: Optional[Any] = None,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        wait_for_metadata_version: Optional[Any] = None,
        wait_for_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stats(
        self,
        *,
        node_id: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def reroute(
        self,
        *,
        body: Optional[Any] = None,
        dry_run: Optional[Any] = None,
        explain: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        metric: Optional[Any] = None,
        retry_failed: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_settings(
        self,
        *,
        flat_settings: Optional[Any] = None,
        include_defaults: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_settings(
        self,
        *,
        body: Any,
        flat_settings: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def remote_info(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def allocation_explain(
        self,
        *,
        body: Optional[Any] = None,
        include_disk_info: Optional[Any] = None,
        include_yes_decisions: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

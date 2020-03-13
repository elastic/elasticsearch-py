from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class NodesClient(NamespacedClient):
    def reload_secure_settings(
        self,
        *,
        node_id: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def info(
        self,
        *,
        node_id: Optional[Any] = None,
        metric: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def hot_threads(
        self,
        *,
        node_id: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        ignore_idle_threads: Optional[Any] = None,
        interval: Optional[Any] = None,
        snapshots: Optional[Any] = None,
        threads: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def usage(
        self,
        *,
        node_id: Optional[Any] = None,
        metric: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stats(
        self,
        *,
        node_id: Optional[Any] = None,
        metric: Optional[Any] = None,
        index_metric: Optional[Any] = None,
        completion_fields: Optional[Any] = None,
        fielddata_fields: Optional[Any] = None,
        fields: Optional[Any] = None,
        groups: Optional[Any] = None,
        include_segment_file_sizes: Optional[Any] = None,
        level: Optional[Any] = None,
        timeout: Optional[Any] = None,
        types: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

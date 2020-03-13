from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class WatcherClient(NamespacedClient):
    def ack_watch(
        self,
        *,
        watch_id: Any,
        action_id: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def activate_watch(
        self,
        *,
        watch_id: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def deactivate_watch(
        self,
        *,
        watch_id: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_watch(
        self,
        *,
        id: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def execute_watch(
        self,
        *,
        body: Optional[Any] = None,
        id: Optional[Any] = None,
        debug: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_watch(
        self,
        *,
        id: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_watch(
        self,
        *,
        id: Any,
        body: Optional[Any] = None,
        active: Optional[Any] = None,
        if_primary_term: Optional[Any] = None,
        if_seq_no: Optional[Any] = None,
        version: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def start(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stats(
        self,
        *,
        metric: Optional[Any] = None,
        emit_stacktraces: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stop(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class SnapshotClient(NamespacedClient):
    def create(
        self,
        *,
        repository: Any,
        snapshot: Any,
        body: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        wait_for_completion: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete(
        self,
        *,
        repository: Any,
        snapshot: Any,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get(
        self,
        *,
        repository: Any,
        snapshot: Any,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        verbose: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_repository(
        self,
        *,
        repository: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_repository(
        self,
        *,
        repository: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def create_repository(
        self,
        *,
        repository: Any,
        body: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        verify: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def restore(
        self,
        *,
        repository: Any,
        snapshot: Any,
        body: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        wait_for_completion: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def status(
        self,
        *,
        repository: Optional[Any] = None,
        snapshot: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def verify_repository(
        self,
        *,
        repository: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def cleanup_repository(
        self,
        *,
        repository: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class IngestClient(NamespacedClient):
    def get_pipeline(
        self,
        *,
        id: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_pipeline(
        self,
        *,
        id: Any,
        body: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_pipeline(
        self,
        *,
        id: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def simulate(
        self,
        *,
        body: Any,
        id: Optional[Any] = None,
        verbose: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def processor_grok(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

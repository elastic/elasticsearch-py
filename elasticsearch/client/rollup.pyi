from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class RollupClient(NamespacedClient):
    def delete_job(
        self,
        *,
        id: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_jobs(
        self,
        *,
        id: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_rollup_caps(
        self,
        *,
        id: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_rollup_index_caps(
        self,
        *,
        index: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_job(
        self,
        *,
        id: Any,
        body: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def rollup_search(
        self,
        *,
        index: Any,
        body: Any,
        doc_type: Optional[Any] = None,
        rest_total_hits_as_int: Optional[Any] = None,
        typed_keys: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def start_job(
        self,
        *,
        id: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stop_job(
        self,
        *,
        id: Any,
        timeout: Optional[Any] = None,
        wait_for_completion: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

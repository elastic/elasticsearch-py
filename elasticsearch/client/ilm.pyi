from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class IlmClient(NamespacedClient):
    def delete_lifecycle(
        self,
        *,
        policy: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def explain_lifecycle(
        self,
        *,
        index: Any,
        only_errors: Optional[Any] = None,
        only_managed: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_lifecycle(
        self,
        *,
        policy: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_status(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def move_to_step(
        self,
        *,
        index: Any,
        body: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_lifecycle(
        self,
        *,
        policy: Any,
        body: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def remove_policy(
        self,
        *,
        index: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def retry(
        self,
        *,
        index: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def start(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stop(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

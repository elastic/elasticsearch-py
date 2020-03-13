from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class SqlClient(NamespacedClient):
    def clear_cursor(
        self,
        *,
        body: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def query(
        self,
        *,
        body: Any,
        format: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def translate(
        self,
        *,
        body: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

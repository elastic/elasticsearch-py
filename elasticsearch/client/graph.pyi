from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class GraphClient(NamespacedClient):
    def explore(
        self,
        *,
        index: Any,
        body: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        routing: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

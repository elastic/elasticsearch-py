from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class MonitoringClient(NamespacedClient):
    def bulk(
        self,
        *,
        body: Any,
        doc_type: Optional[Any] = None,
        interval: Optional[Any] = None,
        system_api_version: Optional[Any] = None,
        system_id: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

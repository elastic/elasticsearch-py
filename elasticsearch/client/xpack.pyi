from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class XPackClient(NamespacedClient):
    def __getattr__(self, attr_name):
        return getattr(self.client, attr_name)
    # AUTO-GENERATED-API-DEFINITIONS #
    def info(
        self,
        *,
        categories: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def usage(
        self,
        *,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class MigrationClient(NamespacedClient):
    def deprecations(
        self,
        *,
        index: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class SslClient(NamespacedClient):
    def certificates(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

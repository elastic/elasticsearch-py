from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class CcrClient(NamespacedClient):
    def delete_auto_follow_pattern(
        self,
        *,
        name: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def follow(
        self,
        *,
        index: Any,
        body: Any,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def follow_info(
        self,
        *,
        index: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def follow_stats(
        self,
        *,
        index: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def forget_follower(
        self,
        *,
        index: Any,
        body: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_auto_follow_pattern(
        self,
        *,
        name: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def pause_follow(
        self,
        *,
        index: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_auto_follow_pattern(
        self,
        *,
        name: Any,
        body: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def resume_follow(
        self,
        *,
        index: Any,
        body: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stats(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def unfollow(
        self,
        *,
        index: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def pause_auto_follow_pattern(
        self,
        *,
        name: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def resume_auto_follow_pattern(
        self,
        *,
        name: Any,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

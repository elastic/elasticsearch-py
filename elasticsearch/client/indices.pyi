from typing import Any, Optional, Mapping
from .utils import NamespacedClient

class IndicesClient(NamespacedClient):
    def analyze(
        self,
        *,
        body: Optional[Any] = None,
        index: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def refresh(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def flush(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        force: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        wait_if_ongoing: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def create(
        self,
        *,
        index: Any,
        body: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def clone(
        self,
        *,
        index: Any,
        target: Any,
        body: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        include_defaults: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def open(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def close(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def exists(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        include_defaults: Optional[Any] = None,
        local: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def exists_type(
        self,
        *,
        index: Any,
        doc_type: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        local: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_mapping(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_mapping(
        self,
        *,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_alias(
        self,
        *,
        index: Any,
        name: Any,
        body: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def exists_alias(
        self,
        *,
        name: Any,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        local: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_alias(
        self,
        *,
        index: Optional[Any] = None,
        name: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        local: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def update_aliases(
        self,
        *,
        body: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_alias(
        self,
        *,
        index: Any,
        name: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_template(
        self,
        *,
        name: Any,
        body: Any,
        create: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        order: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def exists_template(
        self,
        *,
        name: Any,
        flat_settings: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_template(
        self,
        *,
        name: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_template(
        self,
        *,
        name: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_settings(
        self,
        *,
        index: Optional[Any] = None,
        name: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        include_defaults: Optional[Any] = None,
        local: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_settings(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        flat_settings: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        preserve_existing: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def stats(
        self,
        *,
        index: Optional[Any] = None,
        metric: Optional[Any] = None,
        completion_fields: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        fielddata_fields: Optional[Any] = None,
        fields: Optional[Any] = None,
        forbid_closed_indices: Optional[Any] = None,
        groups: Optional[Any] = None,
        include_segment_file_sizes: Optional[Any] = None,
        include_unloaded_segments: Optional[Any] = None,
        level: Optional[Any] = None,
        types: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def segments(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        verbose: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def clear_cache(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        fielddata: Optional[Any] = None,
        fields: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        query: Optional[Any] = None,
        request: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def recovery(
        self,
        *,
        index: Optional[Any] = None,
        active_only: Optional[Any] = None,
        detailed: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def upgrade(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        only_ancient_segments: Optional[Any] = None,
        wait_for_completion: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_upgrade(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def flush_synced(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def shard_stores(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        status: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def forcemerge(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        flush: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        max_num_segments: Optional[Any] = None,
        only_expunge_deletes: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def shrink(
        self,
        *,
        index: Any,
        target: Any,
        body: Optional[Any] = None,
        copy_settings: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def split(
        self,
        *,
        index: Any,
        target: Any,
        body: Optional[Any] = None,
        copy_settings: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def rollover(
        self,
        *,
        alias: Any,
        body: Optional[Any] = None,
        new_index: Optional[Any] = None,
        dry_run: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def freeze(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def unfreeze(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def reload_search_analyzers(
        self,
        *,
        index: Any,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_field_mapping(
        self,
        *,
        fields: Any,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        include_defaults: Optional[Any] = None,
        include_type_name: Optional[Any] = None,
        local: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def validate_query(
        self,
        *,
        body: Optional[Any] = None,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        all_shards: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        analyze_wildcard: Optional[Any] = None,
        analyzer: Optional[Any] = None,
        default_operator: Optional[Any] = None,
        df: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        explain: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        lenient: Optional[Any] = None,
        q: Optional[Any] = None,
        rewrite: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

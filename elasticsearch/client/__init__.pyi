from typing import Any, Optional, Mapping

from ..transport import Transport
from .indices import IndicesClient
from .ingest import IngestClient
from .cluster import ClusterClient
from .cat import CatClient
from .nodes import NodesClient
from .remote import RemoteClient
from .snapshot import SnapshotClient
from .tasks import TasksClient
from .xpack import XPackClient
from .ccr import CcrClient
from .data_frame import Data_FrameClient
from .deprecation import DeprecationClient
from .graph import GraphClient
from .ilm import IlmClient
from .license import LicenseClient
from .migration import MigrationClient
from .ml import MlClient
from .monitoring import MonitoringClient
from .rollup import RollupClient
from .security import SecurityClient
from .sql import SqlClient
from .ssl import SslClient
from .watcher import WatcherClient
from .enrich import EnrichClient
from .slm import SlmClient
from .transform import TransformClient

class Elasticsearch(object):
    transport: Transport
    indices: IndicesClient
    ingest: IngestClient
    cluster: ClusterClient
    cat: CatClient
    nodes: NodesClient
    remote: RemoteClient
    snapshot: SnapshotClient
    tasks: TasksClient

    xpack: XPackClient
    ccr: CcrClient
    data_frame: Data_FrameClient
    deprecation: DeprecationClient
    graph: GraphClient
    ilm: IlmClient
    license: LicenseClient
    migration: MigrationClient
    ml: MlClient
    monitoring: MonitoringClient
    rollup: RollupClient
    security: SecurityClient
    sql: SqlClient
    ssl: SslClient
    watcher: WatcherClient
    enrich: EnrichClient
    slm: SlmClient
    transform: TransformClient
    def __init__(self, hosts=None, transport_class=Transport, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    # AUTO-GENERATED-API-DEFINITIONS #
    def ping(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def info(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def create(
        self,
        *,
        index: Any,
        id: Any,
        body: Any,
        doc_type: Optional[Any] = None,
        pipeline: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        timeout: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def index(
        self,
        *,
        index: Any,
        body: Any,
        doc_type: Optional[Any] = None,
        id: Optional[Any] = None,
        if_primary_term: Optional[Any] = None,
        if_seq_no: Optional[Any] = None,
        op_type: Optional[Any] = None,
        pipeline: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        timeout: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def bulk(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        pipeline: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def clear_scroll(
        self,
        *,
        body: Optional[Any] = None,
        scroll_id: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def count(
        self,
        *,
        body: Optional[Any] = None,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        analyze_wildcard: Optional[Any] = None,
        analyzer: Optional[Any] = None,
        default_operator: Optional[Any] = None,
        df: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_throttled: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        lenient: Optional[Any] = None,
        min_score: Optional[Any] = None,
        preference: Optional[Any] = None,
        q: Optional[Any] = None,
        routing: Optional[Any] = None,
        terminate_after: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete(
        self,
        *,
        index: Any,
        id: Any,
        doc_type: Optional[Any] = None,
        if_primary_term: Optional[Any] = None,
        if_seq_no: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        timeout: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_by_query(
        self,
        *,
        index: Any,
        body: Any,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        analyze_wildcard: Optional[Any] = None,
        analyzer: Optional[Any] = None,
        conflicts: Optional[Any] = None,
        default_operator: Optional[Any] = None,
        df: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        from_: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        lenient: Optional[Any] = None,
        max_docs: Optional[Any] = None,
        preference: Optional[Any] = None,
        q: Optional[Any] = None,
        refresh: Optional[Any] = None,
        request_cache: Optional[Any] = None,
        requests_per_second: Optional[Any] = None,
        routing: Optional[Any] = None,
        scroll: Optional[Any] = None,
        scroll_size: Optional[Any] = None,
        search_timeout: Optional[Any] = None,
        search_type: Optional[Any] = None,
        size: Optional[Any] = None,
        slices: Optional[Any] = None,
        sort: Optional[Any] = None,
        stats: Optional[Any] = None,
        terminate_after: Optional[Any] = None,
        timeout: Optional[Any] = None,
        version: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        wait_for_completion: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_by_query_rethrottle(
        self,
        *,
        task_id: Any,
        requests_per_second: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def delete_script(
        self,
        *,
        id: Any,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def exists(
        self,
        *,
        index: Any,
        id: Any,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        preference: Optional[Any] = None,
        realtime: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        stored_fields: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def exists_source(
        self,
        *,
        index: Any,
        id: Any,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        preference: Optional[Any] = None,
        realtime: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def explain(
        self,
        *,
        index: Any,
        id: Any,
        body: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        analyze_wildcard: Optional[Any] = None,
        analyzer: Optional[Any] = None,
        default_operator: Optional[Any] = None,
        df: Optional[Any] = None,
        lenient: Optional[Any] = None,
        preference: Optional[Any] = None,
        q: Optional[Any] = None,
        routing: Optional[Any] = None,
        stored_fields: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def field_caps(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        fields: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        include_unmapped: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get(
        self,
        *,
        index: Any,
        id: Any,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        preference: Optional[Any] = None,
        realtime: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        stored_fields: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_script(
        self,
        *,
        id: Any,
        master_timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_source(
        self,
        *,
        index: Any,
        id: Any,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        preference: Optional[Any] = None,
        realtime: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def mget(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        preference: Optional[Any] = None,
        realtime: Optional[Any] = None,
        refresh: Optional[Any] = None,
        routing: Optional[Any] = None,
        stored_fields: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def msearch(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        ccs_minimize_roundtrips: Optional[Any] = None,
        max_concurrent_searches: Optional[Any] = None,
        max_concurrent_shard_requests: Optional[Any] = None,
        pre_filter_shard_size: Optional[Any] = None,
        rest_total_hits_as_int: Optional[Any] = None,
        search_type: Optional[Any] = None,
        typed_keys: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def put_script(
        self,
        *,
        id: Any,
        body: Any,
        context: Optional[Any] = None,
        master_timeout: Optional[Any] = None,
        timeout: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def rank_eval(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        search_type: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def reindex(
        self,
        *,
        body: Any,
        max_docs: Optional[Any] = None,
        refresh: Optional[Any] = None,
        requests_per_second: Optional[Any] = None,
        scroll: Optional[Any] = None,
        slices: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        wait_for_completion: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def reindex_rethrottle(
        self,
        *,
        task_id: Any,
        requests_per_second: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def render_search_template(
        self,
        *,
        body: Optional[Any] = None,
        id: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def scripts_painless_execute(
        self,
        *,
        body: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def scroll(
        self,
        *,
        body: Optional[Any] = None,
        scroll_id: Optional[Any] = None,
        rest_total_hits_as_int: Optional[Any] = None,
        scroll: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def search(
        self,
        *,
        body: Optional[Any] = None,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        allow_partial_search_results: Optional[Any] = None,
        analyze_wildcard: Optional[Any] = None,
        analyzer: Optional[Any] = None,
        batched_reduce_size: Optional[Any] = None,
        ccs_minimize_roundtrips: Optional[Any] = None,
        default_operator: Optional[Any] = None,
        df: Optional[Any] = None,
        docvalue_fields: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        explain: Optional[Any] = None,
        from_: Optional[Any] = None,
        ignore_throttled: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        lenient: Optional[Any] = None,
        max_concurrent_shard_requests: Optional[Any] = None,
        pre_filter_shard_size: Optional[Any] = None,
        preference: Optional[Any] = None,
        q: Optional[Any] = None,
        request_cache: Optional[Any] = None,
        rest_total_hits_as_int: Optional[Any] = None,
        routing: Optional[Any] = None,
        scroll: Optional[Any] = None,
        search_type: Optional[Any] = None,
        seq_no_primary_term: Optional[Any] = None,
        size: Optional[Any] = None,
        sort: Optional[Any] = None,
        stats: Optional[Any] = None,
        stored_fields: Optional[Any] = None,
        suggest_field: Optional[Any] = None,
        suggest_mode: Optional[Any] = None,
        suggest_size: Optional[Any] = None,
        suggest_text: Optional[Any] = None,
        terminate_after: Optional[Any] = None,
        timeout: Optional[Any] = None,
        track_scores: Optional[Any] = None,
        track_total_hits: Optional[Any] = None,
        typed_keys: Optional[Any] = None,
        version: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def search_shards(
        self,
        *,
        index: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        local: Optional[Any] = None,
        preference: Optional[Any] = None,
        routing: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def update(
        self,
        *,
        index: Any,
        id: Any,
        body: Any,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        if_primary_term: Optional[Any] = None,
        if_seq_no: Optional[Any] = None,
        lang: Optional[Any] = None,
        refresh: Optional[Any] = None,
        retry_on_conflict: Optional[Any] = None,
        routing: Optional[Any] = None,
        timeout: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def update_by_query_rethrottle(
        self,
        *,
        task_id: Any,
        requests_per_second: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_script_context(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def get_script_languages(
        self,
        *,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def msearch_template(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        ccs_minimize_roundtrips: Optional[Any] = None,
        max_concurrent_searches: Optional[Any] = None,
        rest_total_hits_as_int: Optional[Any] = None,
        search_type: Optional[Any] = None,
        typed_keys: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def mtermvectors(
        self,
        *,
        body: Optional[Any] = None,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        field_statistics: Optional[Any] = None,
        fields: Optional[Any] = None,
        ids: Optional[Any] = None,
        offsets: Optional[Any] = None,
        payloads: Optional[Any] = None,
        positions: Optional[Any] = None,
        preference: Optional[Any] = None,
        realtime: Optional[Any] = None,
        routing: Optional[Any] = None,
        term_statistics: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def search_template(
        self,
        *,
        body: Any,
        index: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        ccs_minimize_roundtrips: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        explain: Optional[Any] = None,
        ignore_throttled: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        preference: Optional[Any] = None,
        profile: Optional[Any] = None,
        rest_total_hits_as_int: Optional[Any] = None,
        routing: Optional[Any] = None,
        scroll: Optional[Any] = None,
        search_type: Optional[Any] = None,
        typed_keys: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def termvectors(
        self,
        *,
        index: Any,
        body: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        id: Optional[Any] = None,
        field_statistics: Optional[Any] = None,
        fields: Optional[Any] = None,
        offsets: Optional[Any] = None,
        payloads: Optional[Any] = None,
        positions: Optional[Any] = None,
        preference: Optional[Any] = None,
        realtime: Optional[Any] = None,
        routing: Optional[Any] = None,
        term_statistics: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...
    def update_by_query(
        self,
        *,
        index: Any,
        body: Optional[Any] = None,
        doc_type: Optional[Any] = None,
        _source: Optional[Any] = None,
        _source_excludes: Optional[Any] = None,
        _source_includes: Optional[Any] = None,
        allow_no_indices: Optional[Any] = None,
        analyze_wildcard: Optional[Any] = None,
        analyzer: Optional[Any] = None,
        conflicts: Optional[Any] = None,
        default_operator: Optional[Any] = None,
        df: Optional[Any] = None,
        expand_wildcards: Optional[Any] = None,
        from_: Optional[Any] = None,
        ignore_unavailable: Optional[Any] = None,
        lenient: Optional[Any] = None,
        max_docs: Optional[Any] = None,
        pipeline: Optional[Any] = None,
        preference: Optional[Any] = None,
        q: Optional[Any] = None,
        refresh: Optional[Any] = None,
        request_cache: Optional[Any] = None,
        requests_per_second: Optional[Any] = None,
        routing: Optional[Any] = None,
        scroll: Optional[Any] = None,
        scroll_size: Optional[Any] = None,
        search_timeout: Optional[Any] = None,
        search_type: Optional[Any] = None,
        size: Optional[Any] = None,
        slices: Optional[Any] = None,
        sort: Optional[Any] = None,
        stats: Optional[Any] = None,
        terminate_after: Optional[Any] = None,
        timeout: Optional[Any] = None,
        version: Optional[Any] = None,
        version_type: Optional[Any] = None,
        wait_for_active_shards: Optional[Any] = None,
        wait_for_completion: Optional[Any] = None,
        params: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> Any: ...

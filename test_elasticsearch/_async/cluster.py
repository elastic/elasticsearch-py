#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import os
import re
import time
from pathlib import Path
from typing import Optional, Tuple

from elasticsearch import (
    AsyncElasticsearch,
    AuthorizationException,
    ConnectionError,
    NotFoundError,
    RequestError,
)

SOURCE_DIR = Path(__file__).absolute().parent.parent.parent
CA_CERTS = str(SOURCE_DIR / ".buildkite/certs/ca.crt")


async def es_url() -> str:
    """Grabs an Elasticsearch URL which can be designated via
    an environment variable otherwise falls back on localhost.
    """
    urls_to_try = []

    # Try user-supplied URLs before generic localhost ones.
    if os.environ.get("ELASTICSEARCH_URL", ""):
        urls_to_try.append(os.environ["ELASTICSEARCH_URL"])
    if os.environ.get("elasticsearch_url", ""):
        urls_to_try.append(os.environ["elasticsearch_url"])
    urls_to_try.extend(
        [
            "https://localhost:9200",
            "http://localhost:9200",
            "https://elastic:changeme@localhost:9200",
            "http://elastic:changeme@localhost:9200",
        ]
    )

    error = None
    for url in urls_to_try:
        if url.startswith("https://"):
            client = AsyncElasticsearch(url, ca_certs=CA_CERTS, verify_certs=False)
        else:
            client = AsyncElasticsearch(url)
        try:
            # Check that we get any sort of connection first.
            await client.info()

            # After we get a connection let's wait for the cluster
            # to be in 'yellow' state, otherwise we could start
            # tests too early and get failures.
            for _ in range(100):
                try:
                    await client.cluster.health(wait_for_status="yellow")
                    break
                except ConnectionError:
                    time.sleep(0.1)

        except ConnectionError as e:
            if error is None:
                error = str(e)
        else:
            successful_url = url
            break
    else:
        raise RuntimeError(
            "Could not connect to Elasticsearch (tried %s): %s"
            % (", ".join(urls_to_try), error)
        )
    return successful_url


async def es_version(client) -> Tuple[int, ...]:
    """Determines the version number and parses the number as a tuple of ints"""
    resp = await client.info()
    return parse_version(resp["version"]["number"])


def parse_version(version: Optional[str]) -> Optional[Tuple[int, ...]]:
    """Parses a version number string into it's major, minor, patch as a tuple"""
    if not version:
        return None
    version_number = tuple(
        int(x)
        for x in re.search(r"^([0-9]+(?:\.[0-9]+)*)", version).group(1).split(".")
    )
    return version_number


async def wipe_cluster(client):
    """Wipes a cluster clean between test cases"""

    is_xpack = True
    if is_xpack:
        await wipe_rollup_jobs(client)
        await wait_for_pending_tasks(client, filter="xpack/rollup/job")
        await wipe_slm_policies(client)

        # Searchable snapshot indices start in 7.8+
        if await es_version(client) >= (7, 8):
            await wipe_searchable_snapshot_indices(client)

    await wipe_snapshots(client)
    if is_xpack:
        await wipe_data_streams(client)
    await wipe_indices(client)

    if is_xpack:
        await wipe_xpack_templates(client)
    else:
        await client.indices.delete_template(name="*")
        await client.indices.delete_index_template(name="*")
        await client.cluster.delete_component_template(name="*")

    await wipe_cluster_settings(client)

    if is_xpack:
        await wipe_ilm_policies(client)
        await wipe_auto_follow_patterns(client)
        await wipe_tasks(client)
        await wipe_node_shutdown_metadata(client)
        await wait_for_pending_datafeeds_and_jobs(client)
        await wipe_calendars(client)
        await wipe_filters(client)
        await wipe_transforms(client)

    await wait_for_cluster_state_updates_to_finish(client)


async def wipe_cluster_settings(client):
    settings = await client.cluster.get_settings()
    new_settings = {}
    for name, value in settings.items():
        if value:
            new_settings.setdefault(name, {})
            for key in value.keys():
                new_settings[name][key + ".*"] = None
    if new_settings:
        await client.cluster.put_settings(body=new_settings)


async def wipe_rollup_jobs(client):
    rollup_jobs = (await client.rollup.get_jobs(id="_all")).get("jobs", ())
    for job in rollup_jobs:
        job_id = job["config"]["id"]
        await client.options(ignore_status=404).rollup.stop_job(
            id=job_id, wait_for_completion=True
        )
        await client.options(ignore_status=404).rollup.delete_job(id=job_id)


async def wipe_snapshots(client):
    """Deletes all the snapshots and repositories from the cluster"""
    in_progress_snapshots = []

    repos = await client.snapshot.get_repository(name="_all")
    for repo_name, repo in repos.items():
        if repo_name in {"found-snapshots"}:
            continue

        if repo["type"] == "fs":
            snapshots = await client.snapshot.get(
                repository=repo_name, snapshot="_all", ignore_unavailable=True
            )
            for snapshot in snapshots["snapshots"]:
                if snapshot["state"] == "IN_PROGRESS":
                    in_progress_snapshots.append(snapshot)
                else:
                    await client.options(ignore_status=404).snapshot.delete(
                        repository=repo_name,
                        snapshot=snapshot["snapshot"],
                    )

        await client.options(ignore_status=404).snapshot.delete_repository(
            name=repo_name
        )

    assert in_progress_snapshots == []


async def wipe_data_streams(client):
    try:
        await client.indices.delete_data_stream(name="*", expand_wildcards="all")
    except Exception:
        await client.indices.delete_data_stream(name="*")


async def wipe_indices(client):
    await client.options(ignore_status=404).indices.delete(
        index="*,-.ds-ilm-history-*",
        expand_wildcards="all",
    )


async def wipe_searchable_snapshot_indices(client):
    cluster_metadata = await client.cluster.state(
        metric="metadata",
        filter_path="metadata.indices.*.settings.index.store.snapshot",
    )
    if cluster_metadata:
        for index in cluster_metadata["metadata"]["indices"].keys():
            await client.indices.delete(index=index)


async def wipe_xpack_templates(client):
    templates = [
        x.strip()
        for x in (await client.cat.templates(h="name")).split("\n")
        if x.strip()
    ]
    for template in templates:
        if is_xpack_template(template):
            continue
        try:
            await client.indices.delete_template(name=template)
        except NotFoundError as e:
            if f"index_template [{template}] missing" in str(e):
                await client.indices.delete_index_template(name=template)

    # Delete component templates, need to retry because sometimes
    # indices aren't cleaned up in time before we issue the delete.
    templates = (await client.cluster.get_component_template())["component_templates"]
    templates_to_delete = [
        template for template in templates if not is_xpack_template(template["name"])
    ]
    for _ in range(3):
        for template in list(templates_to_delete):
            try:
                await client.cluster.delete_component_template(
                    name=template["name"],
                )
            except RequestError:
                pass
            else:
                templates_to_delete.remove(template)

        if not templates_to_delete:
            break
        time.sleep(0.01)


async def wipe_ilm_policies(client):
    for policy in await client.ilm.get_lifecycle():
        if (
            policy
            not in {
                "ilm-history-ilm-policy",
                "slm-history-ilm-policy",
                "watch-history-ilm-policy",
                "watch-history-ilm-policy-16",
                "ml-size-based-ilm-policy",
                "logs",
                "metrics",
                "synthetics",
                "7-days-default",
                "30-days-default",
                "90-days-default",
                "180-days-default",
                "365-days-default",
                ".fleet-actions-results-ilm-policy",
                ".deprecation-indexing-ilm-policy",
                ".monitoring-8-ilm-policy",
            }
            and "-history-ilm-polcy" not in policy
        ):
            await client.ilm.delete_lifecycle(name=policy)


async def wipe_slm_policies(client):
    policies = await client.slm.get_lifecycle()
    for policy in policies:
        if policy not in {"cloud-snapshot-policy"}:
            await client.slm.delete_lifecycle(policy_id=policy)


async def wipe_auto_follow_patterns(client):
    for pattern in (await client.ccr.get_auto_follow_pattern())["patterns"]:
        await client.ccr.delete_auto_follow_pattern(name=pattern["name"])


async def wipe_node_shutdown_metadata(client):
    try:
        shutdown_status = await client.shutdown.get_node()
        # If response contains these two keys the feature flag isn't enabled
        # on this cluster so skip this step now.
        if "_nodes" in shutdown_status and "cluster_name" in shutdown_status:
            return

        for shutdown_node in shutdown_status.get("nodes", []):
            node_id = shutdown_node["node_id"]
            await client.shutdown.delete_node(node_id=node_id)

    # Elastic Cloud doesn't allow this so we skip.
    except AuthorizationException:
        pass


async def wipe_tasks(client):
    tasks = await client.tasks.list()
    for node_name, node in tasks.get("node", {}).items():
        for task_id in node.get("tasks", ()):
            await client.tasks.cancel(task_id=task_id, wait_for_completion=True)


async def wait_for_pending_tasks(client, filter, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        tasks = (await client.cat.tasks(detailed=True)).split("\n")
        if not any(filter in task for task in tasks):
            break


async def wait_for_pending_datafeeds_and_jobs(client: AsyncElasticsearch, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = await client.ml.get_datafeeds(datafeed_id="*", allow_no_match=True)
        if resp["count"] == 0:
            break
        for datafeed in resp["datafeeds"]:
            await client.options(ignore_status=404).ml.delete_datafeed(
                datafeed_id=datafeed["datafeed_id"]
            )

    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = await client.ml.get_jobs(job_id="*", allow_no_match=True)
        if resp["count"] == 0:
            break
        for job in resp["jobs"]:
            await client.options(ignore_status=404).ml.close_job(job_id=job["job_id"])
            await client.options(ignore_status=404).ml.delete_job(job_id=job["job_id"])

    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = await client.ml.get_data_frame_analytics(id="*")
        if resp["count"] == 0:
            break
        for job in resp["data_frame_analytics"]:
            await client.options(ignore_status=404).ml.stop_data_frame_analytics(
                id=job["id"]
            )
            await client.options(ignore_status=404).ml.delete_data_frame_analytics(
                id=job["id"]
            )


async def wipe_filters(client: AsyncElasticsearch, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = await client.ml.get_filters(filter_id="*")
        if resp["count"] == 0:
            break
        for filter in resp["filters"]:
            await client.options(ignore_status=404).ml.delete_filter(
                filter_id=filter["filter_id"]
            )


async def wipe_calendars(client: AsyncElasticsearch, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = await client.ml.get_calendars(calendar_id="*")
        if resp["count"] == 0:
            break
        for calendar in resp["calendars"]:
            await client.options(ignore_status=404).ml.delete_calendar(
                calendar_id=calendar["calendar_id"]
            )


async def wipe_transforms(client: AsyncElasticsearch, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        resp = await client.transform.get_transform(transform_id="*")
        if resp["count"] == 0:
            break
        for trasnform in resp["transforms"]:
            await client.options(ignore_status=404).transform.stop_transform(
                transform_id=trasnform["id"]
            )
            await client.options(ignore_status=404).transform.delete_transform(
                transform_id=trasnform["id"]
            )


async def wait_for_cluster_state_updates_to_finish(client, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not (await client.cluster.pending_tasks()).get("tasks", ()):
            break


def is_xpack_template(name):
    if name.startswith(".monitoring-"):
        return True
    elif name.startswith(".watch") or name.startswith(".triggered_watches"):
        return True
    elif name.startswith(".data-frame-"):
        return True
    elif name.startswith(".ml-"):
        return True
    elif name.startswith(".transform-"):
        return True
    elif name.startswith(".deprecation-"):
        return True
    if name in {
        ".watches",
        "security_audit_log",
        ".slm-history",
        ".async-search",
        "saml-service-provider",
        "logs",
        "logs-settings",
        "logs-mappings",
        "metrics",
        "metrics-settings",
        "metrics-mappings",
        "synthetics",
        "synthetics-settings",
        "synthetics-mappings",
        ".snapshot-blob-cache",
        "ilm-history",
        "logstash-index-template",
        "security-index-template",
        "data-streams-mappings",
    }:
        return True
    return False

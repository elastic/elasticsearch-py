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
    ConnectionError,
    Elasticsearch,
)

SOURCE_DIR = Path(__file__).absolute().parent.parent
CA_CERTS = str(SOURCE_DIR / ".buildkite/certs/ca.crt")


def es_url() -> str:
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
            client = Elasticsearch(url, ca_certs=CA_CERTS, verify_certs=False)
        else:
            client = Elasticsearch(url)
        try:
            # Check that we get any sort of connection first.
            client.info()

            # After we get a connection let's wait for the cluster
            # to be in 'yellow' state, otherwise we could start
            # tests too early and get failures.
            for _ in range(100):
                try:
                    client.cluster.health(wait_for_status="yellow")
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


def es_version(client) -> Tuple[int, ...]:
    """Determines the version number and parses the number as a tuple of ints"""
    resp = client.info()
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


def wipe_cluster(client):
    """Wipes a cluster clean between test cases"""
    close_after_wipe = False
    try:
        # If client is async we need to replace the client
        # with a synchronous one.
        from elasticsearch import AsyncElasticsearch

        if isinstance(client, AsyncElasticsearch):
            node_config = client.transport.node_pool.get().config
            client = Elasticsearch([node_config], verify_certs=False)
            close_after_wipe = True
    except ImportError:
        pass

    wipe_snapshots(client)
    wipe_data_streams(client)
    wipe_indices(client)

    client.indices.delete_template(name="*")
    client.indices.delete_index_template(name="*")

    wipe_cluster_settings(client)

    wait_for_cluster_state_updates_to_finish(client)
    if close_after_wipe:
        client.close()


def wipe_cluster_settings(client):
    settings = client.cluster.get_settings()
    new_settings = {}
    for name, value in settings.items():
        if value:
            new_settings.setdefault(name, {})
            for key in value.keys():
                new_settings[name][key + ".*"] = None
    if new_settings:
        client.cluster.put_settings(body=new_settings)


def wipe_snapshots(client):
    """Deletes all the snapshots and repositories from the cluster"""
    in_progress_snapshots = []

    repos = client.snapshot.get_repository(name="_all")
    for repo_name, repo in repos.items():
        if repo_name in {"found-snapshots"}:
            continue

        if repo["type"] == "fs":
            snapshots = client.snapshot.get(
                repository=repo_name, snapshot="_all", ignore_unavailable=True
            )
            for snapshot in snapshots["snapshots"]:
                if snapshot["state"] == "IN_PROGRESS":
                    in_progress_snapshots.append(snapshot)
                else:
                    client.options(ignore_status=404).snapshot.delete(
                        repository=repo_name,
                        snapshot=snapshot["snapshot"],
                    )

        client.options(ignore_status=404).snapshot.delete_repository(name=repo_name)

    assert in_progress_snapshots == []


def wipe_data_streams(client):
    try:
        client.indices.delete_data_stream(name="*", expand_wildcards="all")
    except Exception:
        client.indices.delete_data_stream(name="*")


def wipe_indices(client):
    indices = client.cat.indices().strip().splitlines()
    if len(indices) > 0:
        index_names = [i.split()[2] for i in indices]
        client.options(ignore_status=404).indices.delete(
            index=",".join(index_names),
            expand_wildcards="all",
        )


def wait_for_cluster_state_updates_to_finish(client, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not client.cluster.pending_tasks().get("tasks", ()):
            break

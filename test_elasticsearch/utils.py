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
import time

from elasticsearch import Elasticsearch, NotFoundError, RequestError


def wipe_cluster(client):
    """Wipes a cluster clean between test cases"""
    close_after_wipe = False
    try:
        # If client is async we need to replace the client
        # with a synchronous one.
        from elasticsearch import AsyncElasticsearch

        if isinstance(client, AsyncElasticsearch):
            client = Elasticsearch(client.transport.hosts, verify_certs=False)
            close_after_wipe = True
    except ImportError:
        pass

    is_xpack = os.getenv("TEST_SUITE") == "xpack"
    if is_xpack:
        wipe_rollup_jobs(client)
        wait_for_pending_tasks(client, filter="xpack/rollup/job")
        wipe_slm_policies(client)

    wipe_snapshots(client)
    if is_xpack:
        wipe_data_streams(client)
    wipe_indices(client)

    if is_xpack:
        wipe_xpack_templates(client)
    else:
        client.indices.delete_template(name="*")
        client.indices.delete_index_template(name="*")
        client.cluster.delete_component_template(name="*")

    wipe_cluster_settings(client)

    if is_xpack:
        wipe_ilm_policies(client)
        wipe_auto_follow_patterns(client)
        wipe_tasks(client)

    wait_for_cluster_state_updates_to_finish(client)
    if close_after_wipe:
        client.close()


def wipe_cluster_settings(client):
    settings = client.cluster.get_settings()
    new_settings = {}
    for name, value in settings.items():
        if value:
            new_settings.setdefault(name, {})
            for key in name.keys():
                new_settings[name][key + ".*"] = None
    if new_settings:
        client.cluster.put_settings(body=new_settings)


def wipe_rollup_jobs(client):
    rollup_jobs = client.rollup.get_jobs(id="_all").get("jobs", ())
    for job in rollup_jobs:
        job_id = job["config"]["id"]
        client.rollup.stop_job(id=job_id, wait_for_completion=True, ignore=404)
        client.rollup.delete_job(id=job_id, ignore=404)


def wipe_snapshots(client):
    """Deletes all the snapshots and repositories from the cluster"""
    repos = client.snapshot.get_repository()
    for name, repo in repos.items():
        if repo["type"] == "fs":
            client.snapshot.delete(
                repository=name,
                snapshot="*",
                ignore=404,
            )

        client.snapshot.delete_repository(repository=name, ignore=404)


def wipe_data_streams(client):
    client.indices.delete_data_stream(name="*")


def wipe_indices(client):

    client.indices.delete(
        index="*",
        expand_wildcards="all",
        ignore=404,
    )


def wipe_xpack_templates(client):
    templates = [
        x.strip() for x in client.cat.templates(h="name").split("\n") if x.strip()
    ]
    for template in templates:
        if is_xpack_template(template):
            continue
        try:
            client.indices.delete_template(name=template)
        except NotFoundError as e:
            if "index_template [%s] missing" % template in str(e.info):
                client.indices.delete_index_template(name=template)

    # Delete component templates, need to retry because sometimes
    # indices aren't cleaned up in time before we issue the delete.
    templates = client.cluster.get_component_template()["component_templates"]
    templates_to_delete = [
        template for template in templates if not is_xpack_template(template["name"])
    ]
    for _ in range(3):
        for template in list(templates_to_delete):
            try:

                client.cluster.delete_component_template(
                    name=template["name"],
                )

            except RequestError:
                pass
            else:
                templates_to_delete.remove(template)

        if not templates_to_delete:
            break
        time.sleep(0.01)


def wipe_ilm_policies(client):
    for policy in client.ilm.get_lifecycle():
        if policy not in {
            "ilm-history-ilm-policy",
            "slm-history-ilm-policy",
            "watch-history-ilm-policy",
            "ml-size-based-ilm-policy",
            "logs",
            "metrics",
        }:
            client.ilm.delete_lifecycle(policy=policy)


def wipe_slm_policies(client):
    for policy in client.slm.get_lifecycle():
        client.slm.delete_lifecycle(policy_id=policy["name"])


def wipe_auto_follow_patterns(client):
    for pattern in client.ccr.get_auto_follow_pattern()["patterns"]:
        client.ccr.delete_auto_follow_pattern(name=pattern["name"])


def wipe_tasks(client):
    tasks = client.tasks.list()
    for node_name, node in tasks.get("node", {}).items():
        for task_id in node.get("tasks", ()):
            client.tasks.cancel(task_id=task_id, wait_for_completion=True)


def wait_for_pending_tasks(client, filter, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        tasks = client.cat.tasks(detailed=True).split("\n")
        if not any(filter in task for task in tasks):
            break


def wait_for_cluster_state_updates_to_finish(client, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if not client.cluster.pending_tasks().get("tasks", ()):
            break


def is_xpack_template(name):
    if ".monitoring-" in name:
        return True
    if ".watch" in name or ".triggered_watches" in name:
        return True
    if ".data-frame-" in name:
        return True
    if ".ml-" in name:
        return True
    if ".transform-" in name:
        return True
    if name in {
        ".watches",
        "logstash-index-template",
        ".logstash-management",
        "security_audit_log",
        ".slm-history",
        ".async-search",
        "saml-service-provider",
        "ilm-history",
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
    }:
        return True
    return False

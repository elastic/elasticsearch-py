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
import subprocess
from pathlib import Path

import unasync


def cleanup(target_files: list[str], patterns: list[str]):
    for path in target_files:
        for pattern in patterns:
            subprocess.check_call(["sed", "-i.bak", pattern, str(path)])
            subprocess.check_call(["rm", f"{path}.bak"])


def get_paths(dir: Path):
    filepaths = []
    for root, _, filenames in os.walk(dir):
        for filename in filenames:
            is_source_file = filename.rpartition(".")[-1] in {"py", "pyi"}
            if is_source_file and filename != "utils.py":
                filepaths.append(os.path.join(root, filename))
    return filepaths


def run(
    rule: unasync.Rule,
    cleanup_patterns: list[str] = [],
):
    root_dir = Path(__file__).absolute().parent.parent
    source_paths = get_paths(root_dir / rule.fromdir)
    target_paths = get_paths(root_dir / rule.todir)

    unasync.unasync_files(source_paths, [rule])

    if cleanup_patterns:
        cleanup(target_paths, cleanup_patterns)


def main():
    run(
        rule=unasync.Rule(
            fromdir="/elasticsearch/_async/client/",
            todir="/elasticsearch/_sync/client/",
            additional_replacements={
                # We want to rewrite to 'Transport' instead of 'SyncTransport', etc
                "AsyncTransport": "Transport",
                "AsyncElasticsearch": "Elasticsearch",
                # We don't want to rewrite this class
                "AsyncSearchClient": "AsyncSearchClient",
                # Handling typing.Awaitable[...] isn't done yet by unasync.
                "_TYPE_ASYNC_SNIFF_CALLBACK": "_TYPE_SYNC_SNIFF_CALLBACK",
            },
        ),
    )

    run(
        rule=unasync.Rule(
            fromdir="elasticsearch/helpers/vectorstore/_async/",
            todir="elasticsearch/helpers/vectorstore/_sync/",
            additional_replacements={
                "AsyncBM25Strategy": "BM25Strategy",
                "AsyncDenseVectorStrategy": "DenseVectorStrategy",
                "AsyncDenseVectorScriptScoreStrategy": "DenseVectorScriptScoreStrategy",
                "AsyncElasticsearch": "Elasticsearch",
                "AsyncElasticsearchEmbeddings": "ElasticsearchEmbeddings",
                "AsyncEmbeddingService": "EmbeddingService",
                "AsyncRetrievalStrategy": "RetrievalStrategy",
                "AsyncSparseVectorStrategy": "SparseVectorStrategy",
                "AsyncTransport": "Transport",
                "AsyncVectorStore": "VectorStore",
                "async_bulk": "bulk",
                "_async": "_sync",
            },
        ),
        cleanup_patterns=[
            "/^import asyncio$/d",
        ],
    )

    run(
        rule=unasync.Rule(
            fromdir="test_elasticsearch/_async/",
            todir="test_elasticsearch/_sync/",
            additional_replacements={
                "AsyncBM25Strategy": "BM25Strategy",
                "AsyncDenseVectorScriptScoreStrategy": "DenseVectorScriptScoreStrategy",
                "AsyncDenseVectorStrategy": "DenseVectorStrategy",
                "AsyncElasticsearch": "Elasticsearch",
                "AsyncElasticsearchEmbeddings": "ElasticsearchEmbeddings",
                "AsyncEmbeddingService": "EmbeddingService",
                "AsyncRetrievalStrategy": "RetrievalStrategy",
                "AsyncSparseVectorStrategy": "SparseVectorStrategy",
                "AsyncTransport": "Transport",
                "AsyncVectorStore": "VectorStore",
                "_async": "_sync",
                "async_bulk": "bulk",
                "async_reindex": "reindex",
                "async_scan": "scan",
                "async_streaming_bulk": "streaming_bulk",
                # test-specific replacements
                "AsyncConsistentFakeEmbeddings": "ConsistentFakeEmbeddings",
                "AsyncFakeEmbeddings": "FakeEmbeddings",
                "AsyncGenerator": "Generator",
                "AsyncRequestSavingTransport": "RequestSavingTransport",
                "pytest_asyncio": "pytest",
                "ASYNC_CONNECTION_CLASS": "SYNC_CONNECTION_CLASS",
            },
        ),
        cleanup_patterns=[
            "s/^from asyncio import sleep$/from time import sleep/",
            "/^import pytest_asyncio$/d",
            "/^ *@pytest.mark.asyncio$/d",
            "/^pytestmark = pytest.mark.asyncio$/d",
            # string goes over 2 lines
            """s/@pytest.mark.parametrize("node_class", \\["aiohttp"\\])/"""
            """@pytest.mark.parametrize("node_class", ["urllib3", "requests"])/""",
        ],
    )


if __name__ == "__main__":
    main()

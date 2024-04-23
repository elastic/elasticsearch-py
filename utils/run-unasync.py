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
from glob import glob
from pathlib import Path

import unasync


def cleanup(source_dir: Path, output_dir: Path, patterns: list[str]):
    if patterns:
        for file in glob("*.py", root_dir=source_dir):
            path = Path(output_dir) / file
            for pattern in patterns:
                subprocess.check_call(["sed", "-i.bak", pattern, str(path)])
            subprocess.check_call(["rm", f"{path}.bak"])


def format_dir(dir: Path):
    subprocess.check_call(["isort", "--profile=black", dir])
    subprocess.check_call(["black", dir])


def run(
    rule: unasync.Rule,
    cleanup_patterns: list[str] = [],
    format: bool = False,
):
    root = Path(__file__).absolute().parent.parent
    source_dir = root / rule.fromdir.lstrip("/")
    output_dir = root / rule.todir.lstrip("/")

    filepaths = []
    for root, _, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.rpartition(".")[-1] in (
                "py",
                "pyi",
            ) and not filename.startswith("utils.py"):
                filepaths.append(os.path.join(root, filename))

    unasync.unasync_files(filepaths, [rule])

    cleanup(source_dir, output_dir, cleanup_patterns)

    if format:
        format_dir(source_dir)
        format_dir(output_dir)


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
            fromdir="elasticsearch/vectorstore/_async/",
            todir="elasticsearch/vectorstore/_sync/",
            additional_replacements={
                "AsyncBM25": "BM25",
                "AsyncDenseVector": "DenseVector",
                "AsyncDenseVectorScriptScore": "DenseVectorScriptScore",
                "AsyncElasticsearch": "Elasticsearch",
                "AsyncElasticsearchEmbeddings": "ElasticsearchEmbeddings",
                "AsyncEmbeddingService": "EmbeddingService",
                "AsyncRetrievalStrategy": "RetrievalStrategy",
                "AsyncSparseVector": "SparseVector",
                "AsyncTransport": "Transport",
                "AsyncVectorStore": "VectorStore",
                "async_bulk": "bulk",
                "_async": "_sync",
            },
        ),
        cleanup_patterns=[
            "/^import asyncio$/d",
            "/^import pytest_asyncio*/d",
            "/ *@pytest.mark.asyncio$/d",
        ],
        format=True,
    )

    run(
        rule=unasync.Rule(
            fromdir="test_elasticsearch/test_server/test_vectorstore/_async/",
            todir="test_elasticsearch/test_server/test_vectorstore/_sync/",
            additional_replacements={
                "AsyncBM25": "BM25",
                "AsyncDenseVector": "DenseVector",
                "AsyncDenseVectorScriptScore": "DenseVectorScriptScore",
                "AsyncElasticsearch": "Elasticsearch",
                "AsyncElasticsearchEmbeddings": "ElasticsearchEmbeddings",
                "AsyncEmbeddingService": "EmbeddingService",
                "AsyncRetrievalStrategy": "RetrievalStrategy",
                "AsyncSparseVector": "SparseVector",
                "AsyncTransport": "Transport",
                "AsyncVectorStore": "VectorStore",
                "async_bulk": "bulk",
                "_async": "_sync",
                # Tests-specific
                "AsyncConsistentFakeEmbeddings": "ConsistentFakeEmbeddings",
                "AsyncFakeEmbeddings": "FakeEmbeddings",
                "AsyncGenerator": "Generator",
                "AsyncRequestSavingTransport": "RequestSavingTransport",
                "pytest_asyncio": "pytest",
            },
        ),
        cleanup_patterns=[
            "/^import asyncio$/d",
            "/^import pytest_asyncio*/d",
            "/ *@pytest.mark.asyncio$/d",
        ],
        format=True,
    )


if __name__ == "__main__":
    main()

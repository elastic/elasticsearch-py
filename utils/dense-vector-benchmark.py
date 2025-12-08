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

import argparse
import asyncio
import json
import os
import time

import numpy as np

from elasticsearch import OrjsonSerializer
from elasticsearch.dsl import AsyncDocument, NumpyDenseVector, async_connections
from elasticsearch.dsl.types import DenseVectorIndexOptions
from elasticsearch.helpers import async_bulk, pack_dense_vector

async_connections.create_connection(
    hosts=[os.environ["ELASTICSEARCH_URL"]], serializer=OrjsonSerializer()
)


class Doc(AsyncDocument):
    title: str
    text: str
    emb: np.ndarray = NumpyDenseVector(
        dtype=np.float32, index_options=DenseVectorIndexOptions(type="flat")
    )

    class Index:
        name = "benchmark"


async def upload(data_file: str, chunk_size: int, pack: bool) -> tuple[float, float]:
    with open(data_file, "rt") as f:
        # read the data file, which comes in ndjson format and convert it to JSON
        json_data = "[" + f.read().strip().replace("\n", ",") + "]"
        dataset = json.loads(json_data)

    # replace the embedding lists with numpy arrays for performance
    dataset = [
        {
            "docid": doc["docid"],
            "title": doc["title"],
            "text": doc["text"],
            "emb": np.array(doc["emb"], dtype=np.float32),
        }
        for doc in dataset
    ]

    # create mapping and index
    if await Doc._index.exists():
        await Doc._index.delete()
    await Doc.init()
    await Doc._index.refresh()

    async def get_next_document():
        for doc in dataset:
            yield {
                "_index": "benchmark",
                "_id": doc["docid"],
                "_source": {
                    "title": doc["title"],
                    "text": doc["text"],
                    "emb": doc["emb"],
                },
            }

    async def get_next_document_packed():
        for doc in dataset:
            yield {
                "_index": "benchmark",
                "_id": doc["docid"],
                "_source": {
                    "title": doc["title"],
                    "text": doc["text"],
                    "emb": pack_dense_vector(doc["emb"]),
                },
            }

    start = time.time()
    result = await async_bulk(
        client=async_connections.get_connection(),
        chunk_size=chunk_size,
        actions=get_next_document_packed() if pack else get_next_document(),
        stats_only=True,
    )
    duration = time.time() - start
    assert result[1] == 0
    return result[0], duration


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", metavar="JSON_DATA_FILE")
    parser.add_argument(
        "--chunk-sizes", "-s", nargs="+", help="Chunk size(s) for bulk uploader"
    )
    args = parser.parse_args()

    for chunk_size in args.chunk_sizes:
        print(f"Uploading '{args.data_file}' with chunk size {chunk_size}...")
        runs = []
        packed_runs = []
        for _ in range(3):
            runs.append(await upload(args.data_file, chunk_size, False))
            packed_runs.append(await upload(args.data_file, chunk_size, True))

        # ensure that all runs uploaded the same number of documents
        size = runs[0][0]
        for run in runs:
            assert run[0] == size
        for run in packed_runs:
            assert run[0] == size

        dur = sum([run[1] for run in runs]) / len(runs)
        packed_dur = sum([run[1] for run in packed_runs]) / len(packed_runs)

        print(f"Size:                  {size}")
        print(f"float duration:        {dur:.02f}s / {size / dur:.02f} docs/s")
        print(
            f"float base64 duration: {packed_dur:.02f}s / {size / packed_dur:.02f} docs/s"
        )
        print(f"Speed up:              {dur / packed_dur:.02f}x")


if __name__ == "__main__":
    asyncio.run(main())

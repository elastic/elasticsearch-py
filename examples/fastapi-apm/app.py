# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import aiohttp
import datetime
import os
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_streaming_bulk
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client


apm = make_apm_client(
    {"SERVICE_NAME": "fastapi-app", "SERVER_URL": "http://apm-server:8200"}
)
es = AsyncElasticsearch(os.environ["ELASTICSEARCH_HOSTS"])
app = FastAPI()
app.add_middleware(ElasticAPM, client=apm)


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()


async def download_games_db():
    async with aiohttp.ClientSession() as http:
        url = "https://cdn.thegamesdb.net/json/database-latest.json"
        resp = await http.request("GET", url)
        for game in (await resp.json())["data"]["games"][:100]:
            yield game


@app.get("/")
async def index():
    return await es.cluster.health()


@app.get("/ingest")
async def ingest():
    if not (await es.indices.exists(index="games")):
        await es.indices.create(index="games")

    async for _ in async_streaming_bulk(
        client=es, index="games", actions=download_games_db()
    ):
        pass

    return {"status": "ok"}


@app.get("/search/{query}")
async def search(query):
    return await es.search(
        index="games", body={"query": {"multi_match": {"query": query}}}
    )


@app.get("/delete")
async def delete():
    return await es.delete_by_query(index="games", body={"query": {"match_all": {}}})


@app.get("/delete/{id}")
async def delete_id(id):
    try:
        return await es.delete(index="games", id=id)
    except NotFoundError as e:
        return e.info, 404


@app.get("/update")
async def update():
    response = []
    docs = await es.search(
        index="games", body={"query": {"multi_match": {"query": ""}}}
    )
    now = datetime.datetime.utcnow()
    for doc in docs["hits"]["hits"]:
        response.append(
            await es.update(
                index="games", id=doc["_id"], body={"doc": {"modified": now}}
            )
        )

    return jsonable_encoder(response)


@app.get("/error")
async def error():
    try:
        await es.delete(index="games", id="somerandomid")
    except NotFoundError as e:
        return e.info


@app.get("/doc/{id}")
async def get_doc(id):
    return await es.get(index="games", id=id)

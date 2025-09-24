import asyncio
import csv
import os
from time import time
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer

from elasticsearch.dsl.pydantic import BaseESModel
from elasticsearch import dsl

model = SentenceTransformer("all-MiniLM-L6-v2")
dsl.async_connections.create_connection(hosts=[os.environ['ELASTICSEARCH_URL']])


class Quote(BaseESModel):
    quote: str
    author: Annotated[str, dsl.Keyword()]
    tags: Annotated[list[str], dsl.Keyword()]
    embedding: Annotated[list[float], dsl.DenseVector()] = Field(init=False, default=[])

    class Index:
        name = 'quotes'


class Tag(BaseModel):
    tag: str
    count: int


class SearchRequest(BaseModel):
    query: str
    filters: list[str]
    knn: bool
    start: int


class SearchResponse(BaseModel):
    quotes: list[Quote]
    tags: list[Tag]
    start: int
    total: int


app = FastAPI()


@app.post('/api/search')
async def search(req: SearchRequest) -> SearchResponse:
    quotes, tags, total = await search_quotes(req.query, req.filters, use_knn=req.knn, start=req.start)
    return SearchResponse(
        quotes=quotes,
        tags=[Tag(tag=t[0], count=t[1]) for t in tags],
        start=req.start,
        total=total
    )


async def ingest_quotes():
    if await Quote._doc._index.exists():
        await Quote._doc._index.delete()
    await Quote._doc.init()

    def ingest_progress(count, start):
        elapsed = time() - start
        print(f'\rIngested {count} quotes. ({count / elapsed:.0f}/sec)', end='')

    def embed_quotes(quotes):
        embeddings = model.encode([q.quote for q in quotes])
        for q, e in zip(quotes, embeddings):
            q.embedding = e.tolist()

    async def get_next_quote():
        quotes: list[Quote] = []
        with open('quotes.csv') as f:
            reader = csv.DictReader(f)
            count = 0
            start = time()
            for row in reader:
                q = Quote(quote=row['quote'], author=row['author'],
                             tags=row['tags'].split(','))
                quotes.append(q)
                if len(quotes) == 512:
                    embed_quotes(quotes)
                    for q in quotes:
                        yield q.to_doc()
                    count += len(quotes)
                    ingest_progress(count, start)
                    quotes = []
            if len(quotes) > 0:
                embed_quotes(quotes)
                for q in quotes:
                    yield q.to_doc()
                ingest_progress(count, start)

    await Quote._doc.bulk(get_next_quote())


async def search_quotes(q, tags, use_knn=True, start=0, size=25):
    s = Quote._doc.search()
    if q == '':
        s = s.query(dsl.query.MatchAll())
    elif use_knn:
        s = s.query(dsl.query.Knn(field=Quote._doc.embedding, query_vector=model.encode(q).tolist()))
    else:
        s = s.query(dsl.query.Match(quote=q))
    for tag in tags:
        s = s.filter(dsl.query.Terms(tags=[tag]))
    s.aggs.bucket('tags', dsl.aggs.Terms(field=Quote._doc.tags, size=100))
    r = await s[start:start + size].execute()
    tags = [(tag.key, tag.doc_count) for tag in r.aggs.tags.buckets]
    return [Quote.from_doc(hit) for hit in r.hits], tags, r['hits'].total.value


if __name__ == "__main__":
    asyncio.run(ingest_quotes())

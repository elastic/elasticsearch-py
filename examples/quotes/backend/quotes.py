import asyncio
import base64
import csv
import os
from time import time
from typing import Annotated

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ValidationError
from sentence_transformers import SentenceTransformer

from elasticsearch import NotFoundError, OrjsonSerializer
from elasticsearch.dsl.pydantic import AsyncBaseESModel
from elasticsearch import dsl
from elasticsearch.dsl.types import DenseVectorIndexOptions

model = SentenceTransformer("all-MiniLM-L6-v2")
dsl.async_connections.create_connection(hosts=[os.environ['ELASTICSEARCH_URL']], serializer=OrjsonSerializer()
)


class Quote(AsyncBaseESModel):
    quote: str
    author: Annotated[str, dsl.Keyword()]
    tags: Annotated[list[str], dsl.Keyword()]
    embedding: Annotated[list[float], dsl.DenseVector(
        index_options=DenseVectorIndexOptions(type="flat"),
    )] = Field(init=False, default=[])

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


app = FastAPI(
    title="Quotes API",
    version="1.0.0",
)


@app.get("/api/quotes/{id}")
async def get_quote(id: str) -> Quote:
    doc = None
    try:
        doc = await Quote._doc.get(id)
    except NotFoundError:
        pass
    if not doc:
        raise HTTPException(status_code=404, detail="Item not found")
    return Quote.from_doc(doc)


@app.post("/api/quotes", status_code=201)
async def create_quote(req: Quote) -> Quote:
    embed_quotes([req])
    doc = req.to_doc()
    doc.meta.id = ""
    await doc.save(refresh=True)
    return Quote.from_doc(doc)


@app.put("/api/quotes/{id}")
async def update_quote(id: str, quote: Quote) -> Quote:
    doc = None
    try:
        doc = await Quote._doc.get(id)
    except NotFoundError:
        pass
    if not doc:
        raise HTTPException(status_code=404, detail="Item not found")
    if quote.quote:
        embed_quotes([quote])
        doc.quote = quote.quote
        doc.embedding = quote.embedding
    if quote.author:
        doc.author = quote.author
    if quote.tags:
        doc.tags = quote.tags
    await doc.save(refresh=True)
    return Quote.from_doc(doc)


@app.delete("/api/quotes/{id}", status_code=204)
async def delete_quote(id: str) -> None:
    doc = None
    try:
        doc = await Quote._doc.get(id)
    except NotFoundError:
        pass
    if not doc:
        raise HTTPException(status_code=404, detail="Item not found")
    await doc.delete(refresh=True)


@app.post('/api/search')
async def search_quotes(req: SearchRequest) -> SearchResponse:
    s = Quote._doc.search()
    if req.query == '':
        s = s.query(dsl.query.MatchAll())
    elif req.knn:
        query_vector = model.encode(req.query).tolist()
        s = s.query(dsl.query.Knn(field=Quote._doc.embedding, query_vector=query_vector))
    else:
        s = s.query(dsl.query.Match(quote=req.query))
    for tag in req.filters:
        s = s.filter(dsl.query.Terms(tags=[tag]))
    s.aggs.bucket('tags', dsl.aggs.Terms(field=Quote._doc.tags, size=100))

    r = await s[req.start:req.start + 25].execute()
    tags = [(tag.key, tag.doc_count) for tag in r.aggs.tags.buckets]
    quotes = [Quote.from_doc(hit) for hit in r.hits]
    total = r['hits'].total.value
    
    return SearchResponse(
        quotes=quotes,
        tags=[Tag(tag=t[0], count=t[1]) for t in tags],
        start=req.start,
        total=total
    )


def embed_quotes(quotes):
    embeddings = model.encode([q.quote for q in quotes])
    for q, e in zip(quotes, embeddings):
        q.embedding = e
        # q.embedding = e.tolist()
        ##byte_array = e.byteswap().tobytes()
        ##q.embedding = base64.b64encode(byte_array).decode()


async def ingest_quotes():
    if await Quote._doc._index.exists():
        await Quote._doc._index.delete()
    await Quote._doc.init()

    def ingest_progress(count, start):
        elapsed = time() - start
        print(f'\rIngested {count} quotes. ({count / elapsed:.0f}/sec)', end='')

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
                count += len(quotes)
                ingest_progress(count, start)

    await Quote._doc.bulk(get_next_quote())
    print("\nIngest complete.")


if __name__ == "__main__":
    asyncio.run(ingest_quotes())

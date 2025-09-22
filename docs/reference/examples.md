---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/examples.html
navigation_title: Examples
---

# {{es}} Python client examples [examples]

Below you can find examples of how to use the most frequently called APIs with the Python client.

* [Indexing a document](#ex-index)
* [Getting a document](#ex-get)
* [Refreshing an index](#ex-refresh)
* [Searching for a document](#ex-search)
* [Updating a document](#ex-update)
* [Deleting a document](#ex-delete)


## Indexing a document [ex-index]

To index a document, you need to specify three pieces of information: `index`, `id`, and a `document`:

```py
from datetime import datetime
from elasticsearch import Elasticsearch
client = Elasticsearch('https://localhost:9200')

doc = {
    'author': 'author_name',
    'text': 'Interesting content...',
    'timestamp': datetime.now(),
}
resp = client.index(index="test-index", id=1, document=doc)
print(resp['result'])
```


## Getting a document [ex-get]

To get a document, you need to specify its `index` and `id`:

```py
resp = client.get(index="test-index", id=1)
print(resp['_source'])
```


## Refreshing an index [ex-refresh]

You can perform the refresh operation on an index:

```py
client.indices.refresh(index="test-index")
```


## Searching for a document [ex-search]

The `search()` method returns results that are matching a query:

```py
resp = client.search(index="test-index", query={"match_all": {}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
```


## Updating a document [ex-update]

To update a document, you need to specify three pieces of information: `index`, `id`, and a `doc`:

```py
from datetime import datetime
from elasticsearch import Elasticsearch

client = Elasticsearch('https://localhost:9200')

doc = {
    'author': 'author_name',
    'text': 'Interesting modified content...',
    'timestamp': datetime.now(),
}
resp = client.update(index="test-index", id=1, doc=doc)
print(resp['result'])
```


## Deleting a document [ex-delete]

You can delete a document by specifying its `index`, and `id` in the `delete()` method:

```py
client.delete(index="test-index", id=1)
```


## Interactive examples [ex-interactive]

The [elasticsearch-labs](https://github.com/elastic/elasticsearch-labs) repo contains interactive and executable [Python notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks), sample apps, and resources for testing out Elasticsearch, using the Python client. These examples are mainly focused on vector search, hybrid search and generative AI use cases, but you’ll also find examples of basic operations like creating index mappings and performing lexical search.


### Search notebooks [_search_notebooks]

The [Search](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/search) folder is a good place to start if you’re new to Elasticsearch. This folder contains a number of notebooks that demonstrate the fundamentals of Elasticsearch, like indexing vectors, running lexical, semantic and *hybrid* searches, and more.

The following notebooks are available:

* [Quick start](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/00-quick-start.ipynb)
* [Keyword, querying, filtering](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/01-keyword-querying-filtering.ipynb)
* [Hybrid search](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/02-hybrid-search.ipynb)
* [Semantic search with ELSER](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/03-ELSER.ipynb)
* [Multilingual semantic search](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/04-multilingual.ipynb)
* [Query rules](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/05-query-rules.ipynb)
* [Synonyms API quick start](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/06-synonyms-api.ipynb)

Here’s a brief overview of what you’ll learn in each notebook.


#### Quick start [_quick_start]

In the [00-quick-start.ipynb](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/00-quick-start.ipynb) notebook you’ll learn how to:

* Use the Elasticsearch Python client for various operations.
* Create and define an index for a sample dataset with `dense_vector` fields.
* Transform book titles into embeddings using [Sentence Transformers](https://www.sbert.net) and index them into Elasticsearch.
* Perform k-nearest neighbors (knn) semantic searches.
* Integrate traditional text-based search with semantic search, for a hybrid search system.
* Use reciprocal rank fusion (RRF) to intelligently combine search results from different retrieval systems.


#### Keyword, querying, filtering [_keyword_querying_filtering]

In the [01-keyword-querying-filtering.ipynb](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/01-keyword-querying-filtering.ipynb) notebook, you’ll learn how to:

* Use [query and filter contexts](docs-content://explore-analyze/query-filter/languages/querydsl.md) to search and filter documents in Elasticsearch.
* Execute full-text searches with `match` and `multi-match` queries.
* Query and filter documents based on `text`, `number`, `date`, or `boolean` values.
* Run multi-field searches using the `multi-match` query.
* Prioritize specific fields in the `multi-match` query for tailored results.


#### Hybrid search [_hybrid_search]

In the [02-hybrid-search.ipynb](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/02-hybrid-search.ipynb) notebook, you’ll learn how to:

* Combine results of traditional text-based search with semantic search, for a hybrid search system.
* Transform fields in the sample dataset into embeddings using the Sentence Transformer model and index them into Elasticsearch.
* Use the [RRF API](elasticsearch://reference/elasticsearch/rest-apis/reciprocal-rank-fusion.md#rrf-api) to combine the results of a `match` query and a `kNN` semantic search.
* Walk through a super simple toy example that demonstrates, step by step, how RRF ranking works.


#### Semantic search with ELSER [_semantic_search_with_elser]

In the [03-ELSER.ipynb](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/03-ELSER.ipynb) notebook, you’ll learn how to:

* Use the Elastic Learned Sparse Encoder (ELSER) for text expansion-powered semantic search, out of the box — without training, fine-tuning, or embeddings generation.
* Download and deploy the ELSER model in your Elastic environment.
* Create an Elasticsearch index named search-movies with specific mappings and index a dataset of movie descriptions.
* Create an ingest pipeline containing an inference processor for ELSER model execution.
* Reindex the data from search-movies into another index, elser-movies, using the ELSER pipeline for text expansion.
* Observe the results of running the documents through the model by inspecting the additional terms it adds to documents, which enhance searchability.
* Perform simple keyword searches on the elser-movies index to assess the impact of ELSER’s text expansion.
* Execute ELSER-powered semantic searches using the `text_expansion` query.


#### Multilingual semantic search [_multilingual_semantic_search]

In the [04-multilingual.ipynb](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/04-multilingual.ipynb) notebook, you’ll learn how to:

* Use a multilingual embedding model for semantic search across languages.
* Transform fields in the sample dataset into embeddings using the Sentence Transformer model and index them into Elasticsearch.
* Use filtering with a `kNN` semantic search.
* Walk through a super simple toy example that demonstrates, step by step, how multilingual search works across languages, and within non-English languages.


#### Query rules [_query_rules]

In the [05-query-rules.ipynb](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/05-query-rules.ipynb) notebook, you’ll learn how to:

* Use the query rules management APIs to create and edit promotional rules based on contextual queries.
* Apply these query rules by using the `rule_query` in Query DSL.


#### Synonyms API quick start [_synonyms_api_quick_start]

In the [06-synonyms-api.ipynb](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/search/06-synonyms-api.ipynb) notebook, you’ll learn how to:

* Use the synonyms management API to create a synonyms set to enhance your search recall.
* Configure an index to use search-time synonyms.
* Update synonyms in real time.
* Run queries that are enhanced by synonyms.


### Other notebooks [_other_notebooks]

* [Generative AI](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/generative-ai). Notebooks that demonstrate various use cases for Elasticsearch as the retrieval engine and vector store for LLM-powered applications.
* [Integrations](https://github.com/elastic/elasticsearch-labs/blob/main/notebooks/integrations). Notebooks that demonstrate how to integrate popular services and projects with Elasticsearch, including OpenAI, Hugging Face, and LlamaIndex
* [Langchain](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/langchain). Notebooks that demonstrate how to integrate Elastic with LangChain, a framework for developing applications powered by language models.


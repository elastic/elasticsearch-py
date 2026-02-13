---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/_tutorials.html
---

# Tutorials [_tutorials]

## Search [_search]

Let’s have a typical search request written directly as a `dict`:

```python
from elasticsearch import Elasticsearch
client = Elasticsearch("https://localhost:9200")

response = client.search(
    index="my-index",
    body={
      "query": {
        "bool": {
          "must": [{"match": {"title": "python"}}],
          "must_not": [{"match": {"description": "beta"}}],
          "filter": [{"term": {"category": "search"}}]
        }
      },
      "aggs" : {
        "per_tag": {
          "terms": {"field": "tags"},
          "aggs": {
            "max_lines": {"max": {"field": "lines"}}
          }
        }
      }
    }
)

for hit in response['hits']['hits']:
    print(hit['_score'], hit['_source']['title'])

for tag in response['aggregations']['per_tag']['buckets']:
    print(tag['key'], tag['max_lines']['value'])
```

The problem with this approach is that it is verbose, prone to syntax mistakes like incorrect nesting, hard to modify (for example adding another filter) and definitely not fun to write.

Let’s rewrite the example using the DSL module:

```python
from elasticsearch import Elasticsearch
from elasticsearch.dsl import Search, query, aggs

client = Elasticsearch("https://localhost:9200")

s = Search(using=client, index="my-index") \
    .query(query.Match("title", "python"))   \
    .filter(query.Term("category", "search")) \
    .exclude(query.Match("description", "beta"))

s.aggs.bucket('per_tag', aggs.Terms(field="tags")) \
    .metric('max_lines', aggs.Max(field='lines'))

response = s.execute()

for hit in response:
    print(hit.meta.score, hit.title)

for tag in response.aggregations.per_tag.buckets:
    print(tag.key, tag.max_lines.value)
```

As you see, the DSL module took care of:

* creating appropriate `Query` objects from classes
* composing queries into a compound `bool` query
* putting the `term` query in a filter context of the `bool` query
* providing a convenient access to response data
* no curly or square brackets everywhere


## Persistence [_persistence]

Let’s have a simple Python class representing an article in a blogging system:

```python
from datetime import datetime
from elasticsearch.dsl import Document, Date, Integer, Keyword, Text, connections, mapped_field

# Define a default Elasticsearch client
connections.create_connection(hosts="https://localhost:9200")

class Article(Document):
    title: str = mapped_field(Text(analyzer='snowball', fields={'raw': Keyword()}))
    body: str = mapped_field(Text(analyzer='snowball'))
    tags: list[str] = mapped_field(Keyword())
    published_from: datetime
    lines: int

    class Index:
        name = 'blog'
        settings = {
          "number_of_shards": 2,
        }

    def save(self, **kwargs):
        self.lines = len(self.body.split())
        return super(Article, self).save(** kwargs)

    def is_published(self):
        return datetime.now() > self.published_from

# create the mappings in elasticsearch
Article.init()

# create and save and article
article = Article(meta={'id': 42}, title='Hello world!', tags=['test'])
article.body = ''' looong text '''
article.published_from = datetime.now()
article.save()

article = Article.get(id=42)
print(article.is_published())

# Display cluster health
print(connections.get_connection().cluster.health())
```

In this example you can see:

* providing a default connection
* defining fields with Python type hints and additional mapping configuration when necessary
* setting index name
* defining custom methods
* overriding the built-in `.save()` method to hook into the persistence life cycle
* retrieving and saving the object into Elasticsearch
* accessing the underlying client for other APIs

You can see more in the [persistence](dsl_how_to_guides.md#_persistence_2) chapter.


## Pre-built Faceted Search [_pre_built_faceted_search]

If you have your `Document`s defined you can create a faceted search class to simplify searching and filtering.

```python
from elasticsearch.dsl import FacetedSearch, TermsFacet, DateHistogramFacet

class BlogSearch(FacetedSearch):
    doc_types = [Article, ]
    # fields that should be searched
    fields = ['tags', 'title', 'body']

    facets = {
        # use bucket aggregations to define facets
        'tags': TermsFacet(field='tags'),
        'publishing_frequency': DateHistogramFacet(field='published_from', interval='month')
    }

# empty search
bs = BlogSearch()
response = bs.execute()

for hit in response:
    print(hit.meta.score, hit.title)

for (tag, count, selected) in response.facets.tags:
    print(tag, ' (SELECTED):' if selected else ':', count)

for (month, count, selected) in response.facets.publishing_frequency:
    print(month.strftime('%B %Y'), ' (SELECTED):' if selected else ':', count)
```

You can find more details in the `faceted_search` chapter.


## Update By Query [_update_by_query]

Let’s resume the simple example of articles on a blog, and let’s assume that each article has a number of likes. For this example, imagine we want to increment the number of likes by 1 for all articles that match a certain tag and do not match a certain description. Writing this as a `dict`, we would have the following code:

```python
from elasticsearch import Elasticsearch
client = Elasticsearch()

response = client.update_by_query(
    index="my-index",
    body={
      "query": {
        "bool": {
          "must": [{"match": {"tag": "python"}}],
          "must_not": [{"match": {"description": "beta"}}]
        }
      },
      "script"={
        "source": "ctx._source.likes++",
        "lang": "painless"
      }
    },
  )
```

Using the DSL, we can now express this query as such:

```python
from elasticsearch import Elasticsearch
from elasticsearch.dsl import Search, UpdateByQuery
from elasticsearch.dsl.query import Match

client = Elasticsearch()
ubq = UpdateByQuery(using=client, index="my-index") \
      .query(Match("title", "python"))   \
      .exclude(Match("description", "beta")) \
      .script(source="ctx._source.likes++", lang="painless")

response = ubq.execute()
```

As you can see, the `Update By Query` object provides many of the savings offered by the `Search` object, and additionally allows one to update the results of the search based on a script assigned in the same manner.


## ES|QL Queries

The DSL module features an integration with the ES|QL query builder, consisting of two methods available in all `Document` sub-classes: `esql_from()` and `esql_execute()`. Using the `Article` document from above, we can search for up to ten articles that include `"world"` in their titles with the following ES|QL query:

```python
from elasticsearch.esql import functions

query = Article.esql_from().where(functions.match(Article.title, 'world')).limit(10)
for a in Article.esql_execute(query):
    print(a.title)
```

Review the [ES|QL query builder section](esql-query-builder.md) to learn more about building ES|QL queries in Python.

## Migration from the standard client [_migration_from_the_standard_client]

You don’t have to port your entire application to get the benefits of the DSL module, you can start gradually by creating a `Search` object from your existing `dict`, modifying it using the API and serializing it back to a `dict`:

```python
body = {...} # insert complicated query here

# Convert to Search object
s = Search.from_dict(body)

# Add some filters, aggregations, queries, ...
s.filter(query.Term("tags", "python"))

# Convert back to dict to plug back into existing code
body = s.to_dict()
```



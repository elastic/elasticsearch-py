---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/_how_to_guides.html
---

# How-To Guides [_how_to_guides]

## Search DSL [search_dsl]

### The `Search` object [_the_search_object]

The `Search` object represents the entire search request:

* queries
* filters
* aggregations
* k-nearest neighbor searches
* sort
* pagination
* highlighting
* suggestions
* collapsing
* additional parameters
* associated client

The API is designed to be chainable. With the exception of the aggregations functionality this means that the `Search` object is immutable -all changes to the object will result in a shallow copy being created which contains the changes. You can safely pass the `Search` object to foreign code without fear of it modifying your objects as long as it sticks to the `Search` object APIs.

You can pass an instance of the [elasticsearch client](https://elasticsearch-py.readthedocs.io/) when instantiating the `Search` object:

```python
from elasticsearch import Elasticsearch
from elasticsearch.dsl import Search

client = Elasticsearch()

s = Search(using=client)
```

You can also define the client at a later time (for more options see the `configuration` chapter):

```python
s = s.using(client)
```

::::{note}
All methods return a *copy* of the object, making it safe to pass to outside code.

::::


The API is chainable, allowing you to combine multiple method calls in one statement:

```python
s = Search().using(client).query(Match("title", "python"))
```

To send the request to Elasticsearch:

```python
response = s.execute()
```

If you just want to iterate over the hits returned by your search you can iterate over the `Search` object:

```python
for hit in s:
    print(hit.title)
```

Search results will be cached. Subsequent calls to `execute` or trying to iterate over an already executed `Search` object will not trigger additional requests being sent to Elasticsearch. To force a new request to be issued specify `ignore_cache=True` when calling `execute`.

For debugging purposes you can serialize the `Search` object to a `dict` with the raw Elasticsearch request:

```python
print(s.to_dict())
```

#### Delete By Query [_delete_by_query]

You can delete the documents matching a search by calling `delete` on the `Search` object instead of `execute` like this:

```python
s = Search(index='i').query(Match("title", "python"))
response = s.delete()
```

To pass [deletion parameters](https://elasticsearch-py.readthedocs.io/en/latest/api/elasticsearch.html#elasticsearch.Elasticsearch.delete_by_query)
in your query, you can add them by calling ``params`` on the ``Search`` object before ``delete`` like this:

```python
s = Search(index='i').query("match", title="python")
s = s.params(ignore_unavailable=False, wait_for_completion=True)
response = s.delete()
```


#### Queries [_queries]

The `elasticsearch.dsl.query` module provides classes for all Elasticsearch query types. These classes accept keyword arguments in their constructors, which are serialized to the appropriate format to be sent to Elasticsearch. There is a clear one-to-one mapping between the raw query and its equivalent class-based version:

```python
>>> from elasticsearch.dsl.query import MultiMatch, Match

>>> q = MultiMatch(query='python django', fields=['title', 'body'])
>>> q.to_dict()
{'multi_match': {'query': 'python django', 'fields': ['title', 'body']}}

>>> q = Match("title", {"query": "web framework", "type": "phrase"})
>>> q.to_dict()
{'match': {'title': {'query': 'web framework', 'type': 'phrase'}}}
```

An alternative to the class-based queries is to use the `Q` shortcut, passing a query name followed by its parameters, or the raw query as a `dict`:

```python
from elasticsearch.dsl import Q

Q("multi_match", query='python django', fields=['title', 'body'])
Q({"multi_match": {"query": "python django", "fields": ["title", "body"]}})
```

To add a query to the `Search` object, use the `.query()` method. This works with class-based or `Q` queries:

```python
q = Q("multi_match", query='python django', fields=['title', 'body'])
s = s.query(q)
```

As a shortcut the `query()` method also accepts all the parameters of the `Q` shortcut directly:

```python
s = s.query("multi_match", query='python django', fields=['title', 'body'])
```

If you already have a query object, or a `dict` representing one, you can assign it to the `query` attribute of a `Search` object to add it to it, replacing any previously configured queries:

```python
s.query = Q('bool', must=[Q('match', title='python'), Q('match', body='best')])
```


#### Dotted fields [_dotted_fields]

Sometimes you want to refer to a field within another field, either as a multi-field (`title.keyword`) or in a structured `json` document like `address.city`. This is not a problem when using class-based queries, but when working without classes it is often required to pass field names as keyword arguments. To make this easier, you can use `__` (double underscore) in place of a dot in a keyword argument:

```python
s = Search()
s = s.filter('term', category__keyword='Python')
s = s.query('match', address__city='prague')
```

Alternatively you can use Python’s keyword argument unpacking:

```python
s = Search()
s = s.filter('term', **{'category.keyword': 'Python'})
s = s.query('match', **{'address.city': 'prague'})
```


#### Query combination [_query_combination]

Query objects can be combined using logical operators `|`, `&` and `~`:

```python
>>> q = Match("title", "python") | Match("title", "django")
>>> q.to_dict()
{'bool': {'should': [{'match': {'title': 'python'}}, {'match': {'title': 'django'}}]}}

>>> q = Match("title", "python") & Match("title", "django")
>>> q.to_dict()
{'bool': {'must': [{'match': {'title': 'python'}}, {'match': {'title': 'django'}}]}}

>>> q = ~Match("title", "python")
>>> q.to_dict()
{'bool': {'must_not': [{'match': {'title': 'python'}}]}}
```

When you call the `.query()` method multiple times, the `&` operator will be used internally to combine all the queries:

```python
s = s.query().query()
print(s.to_dict())
# {"query": {"bool": {...}}}
```

If you want to have precise control over the query form, use the `Q` shortcut to directly construct the combined query:

```python
q = Q('bool',
    must=[Q('match', title='python')],
    should=[Q(...), Q(...)],
    minimum_should_match=1
)
s = Search().query(q)
```


#### Filters [_filters]

If you want to add a query in a [filter context](docs-content://explore-analyze/query-filter/languages/querydsl.md) you can use the `filter()` method to make things easier:

```python
from elasticsearch.dsl.query import Terms

s = Search()
s = s.filter(Terms("tags", ['search', 'python']))
```

Behind the scenes this will produce a `Bool` query and place the specified `terms` query into its `filter` branch, making it equivalent to:

```python
from elasticsearch.dsl.query import Terms, Bool

s = Search()
s = s.query(Bool(filter=[Terms("tags", ["search", "python"])]))
```

If you want to use the `post_filter` element for faceted navigation, use the `.post_filter()` method.

The `exclude()` method works like `filter()`, but it applies the query as negated:

```python
s = Search()
s = s.exclude(Terms("tags", ['search', 'python']))
```

which is shorthand for:

```python
s = s.query(Bool(filter=[~Terms("tags", ["search", "python"])]))
```


#### Aggregations [_aggregations]

As with queries, there are classes that represent each aggregation type, all accessible through the `elasticsearch.dsl.aggs` module:

```python
from elasticsearch.dsl import aggs

a = aggs.Terms(field="tags")
# {"terms": {"field": "tags"}}
```

It is also possible to define an aggregation using the `A` shortcut:

```python
from elasticsearch.dsl import A

A('terms', field='tags')
```

To nest aggregations, you can use the `.bucket()`, `.metric()` and `.pipeline()` methods:

```python
a = aggs.Terms(field="category")
# {'terms': {'field': 'category'}}

a.metric("clicks_per_category", aggs.Sum(field="clicks")) \
    .bucket("tags_per_category", aggs.Terms(field="tags"))
# {
#   'terms': {'field': 'category'},
#   'aggs': {
#     'clicks_per_category': {'sum': {'field': 'clicks'}},
#     'tags_per_category': {'terms': {'field': 'tags'}}
#   }
# }
```

To add aggregations to the `Search` object, use the `.aggs` property, which acts as a top-level aggregation:

```python
s = Search()
a = aggs.Terms(field="category")
s.aggs.bucket("category_terms", a)
# {
#   'aggs': {
#     'category_terms': {
#       'terms': {
#         'field': 'category'
#       }
#     }
#   }
# }
```

or

```python
s = Search()
s.aggs.bucket("articles_per_day", aggs.DateHistogram(field="publish_date", interval="day")) \
    .metric("clicks_per_day", aggs.Sum(field="clicks")) \
    .pipeline("moving_click_average", aggs.MovingAvg(buckets_path="clicks_per_day")) \
    .bucket("tags_per_day", aggs.Terms(field="tags"))

s.to_dict()
# {
#   "aggs": {
#     "articles_per_day": {
#       "date_histogram": { "interval": "day", "field": "publish_date" },
#       "aggs": {
#         "clicks_per_day": { "sum": { "field": "clicks" } },
#         "moving_click_average": { "moving_avg": { "buckets_path": "clicks_per_day" } },
#         "tags_per_day": { "terms": { "field": "tags" } }
#       }
#     }
#   }
# }
```

You can access an existing bucket by its name:

```python
s = Search()

s.aggs.bucket("per_category", aggs.Terms(field="category"))
s.aggs["per_category"].metric("clicks_per_category", aggs.Sum(field="clicks"))
s.aggs["per_category"].bucket("tags_per_category", aggs.Terms(field="tags"))
```

::::{note}
When chaining multiple aggregations, there is a difference between what `.bucket()` and `.metric()` methods return - `.bucket()` returns the newly defined bucket while `.metric()` returns its parent bucket to allow further chaining.

::::


As opposed to other methods on the `Search` objects, aggregations are defined in-place, without returning a new copy.


#### K-Nearest Neighbor Searches [_k_nearest_neighbor_searches]

To issue a kNN search, use the `.knn()` method:

```python
s = Search()
vector = get_embedding("search text")

s = s.knn(
    field="embedding",
    k=5,
    num_candidates=10,
    query_vector=vector
)
```

The `field`, `k` and `num_candidates` arguments can be given as positional or keyword arguments and are required. In addition to these, `query_vector` or `query_vector_builder` must be given as well.

The `.knn()` method can be invoked multiple times to include multiple kNN searches in the request.


#### Sorting [_sorting]

To specify sorting order, use the `.sort()` method:

```python
s = Search().sort(
    'category',
    '-title',
    {"lines" : {"order" : "asc", "mode" : "avg"}}
)
```

It accepts positional arguments which can be either strings or dictionaries. String value is a field name, optionally prefixed by the `-` sign to specify a descending order.

To reset the sorting, just call the method with no arguments:

```python
s = s.sort()
```


#### Pagination [_pagination]

To specify the from/size parameters, apply the standard Python slicing operator on the `Search` instance:

```python
s = s[10:20]
# {"from": 10, "size": 10}

s = s[:20]
# {"size": 20}

s = s[10:]
# {"from": 10}

s = s[10:20][2:]
# {"from": 12, "size": 8}
```

If you want to access all the documents matched by your query you can use the `scan` method which uses the scan/scroll elasticsearch API:

```python
for hit in s.scan():
    print(hit.title)
```

Note that in this case the results won’t be sorted.


#### Highlighting [_highlighting]

To set common attributes for highlighting use the `highlight_options` method:

```python
s = s.highlight_options(order='score')
```

Enabling highlighting for individual fields is done using the `highlight` method:

```python
s = s.highlight('title')
# or, including parameters:
s = s.highlight('title', fragment_size=50)
```

The fragments in the response will then be available on each `Result` object as `.meta.highlight.FIELD` which will contain the list of fragments:

```python
response = s.execute()
for hit in response:
    for fragment in hit.meta.highlight.title:
        print(fragment)
```


#### Suggestions [_suggestions]

To specify a suggest request on your `Search` object use the `suggest` method:

```python
# check for correct spelling
s = s.suggest('my_suggestion', 'pyhton', term={'field': 'title'})
```

The first argument is the name of the suggestions (name under which it will be returned), second is the actual text you wish the suggester to work on and the keyword arguments will be added to the suggest’s json as-is which means that it should be one of `term`, `phrase` or `completion` to indicate which type of suggester should be used.


#### Collapsing [_collapsing]

To collapse search results use the `collapse` method on your `Search` object:

```python
s = Search().query(Match("message", "GET /search"))
# collapse results by user_id
s = s.collapse("user_id")
```

The top hits will only include one result per `user_id`. You can also expand each collapsed top hit with the `inner_hits` parameter, `max_concurrent_group_searches` being the number of concurrent requests allowed to retrieve the inner hits per group:

```python
inner_hits = {"name": "recent_search", "size": 5, "sort": [{"@timestamp": "desc"}]}
s = s.collapse("user_id", inner_hits=inner_hits, max_concurrent_group_searches=4)
```


#### More Like This Query [_more_like_this_query]

To use Elasticsearch’s `more_like_this` functionality, you can use the MoreLikeThis query type.

A simple example is below

```python
from elasticsearch.dsl.query import MoreLikeThis
from elasticsearch.dsl import Search

my_text = 'I want to find something similar'

s = Search()
# We're going to match based only on two fields, in this case text and title
s = s.query(MoreLikeThis(like=my_text, fields=['text', 'title']))
# You can also exclude fields from the result to make the response quicker in the normal way
s = s.source(exclude=["text"])
response = s.execute()

for hit in response:
    print(hit.title)
```


#### Extra properties and parameters [_extra_properties_and_parameters]

To set extra properties of the search request, use the `.extra()` method. This can be used to define keys in the body that cannot be defined via a specific API method like `explain` or `search_after`:

```python
s = s.extra(explain=True)
```

To set query parameters, use the `.params()` method:

```python
s = s.params(routing="42")
```

If you need to limit the fields being returned by elasticsearch, use the `source()` method:

```python
# only return the selected fields
s = s.source(['title', 'body'])
# don't return any fields, just the metadata
s = s.source(False)
# explicitly include/exclude fields
s = s.source(includes=["title"], excludes=["user.*"])
# reset the field selection
s = s.source(None)
```


#### Serialization and Deserialization [_serialization_and_deserialization]

The search object can be serialized into a dictionary by using the `.to_dict()` method.

You can also create a `Search` object from a `dict` using the `from_dict` class method. This will create a new `Search` object and populate it using the data from the dict:

```python
s = Search.from_dict({"query": {"match": {"title": "python"}}})
```

If you wish to modify an existing `Search` object, overriding it’s properties, instead use the `update_from_dict` method that alters an instance **in-place**:

```python
s = Search(index='i')
s.update_from_dict({"query": {"match": {"title": "python"}}, "size": 42})
```



### Response [_response]

You can execute your search by calling the `.execute()` method that will return a `Response` object. The `Response` object allows you access to any key from the response dictionary via attribute access. It also provides some convenient helpers:

```python
response = s.execute()

print(response.success())
# True

print(response.took)
# 12

print(response.hits.total.relation)
# eq
print(response.hits.total.value)
# 142

print(response.suggest.my_suggestions)
```

If you want to inspect the contents of the `response` objects, just use its `to_dict` method to get access to the raw data for pretty printing.

#### Hits [_hits]

To access the hits returned by the search, use the `hits` property or just iterate over the `Response` object:

```python
response = s.execute()
print(f"Total {response.hits.total} hits found.")
for h in response:
    print(h.title, h.body)
```

::::{note}
If you are only seeing partial results (e.g. 10000 or even 10 results), consider using the option `s.extra(track_total_hits=True)` to get a full hit count.

::::



#### Result [_result]

The individual hits is wrapped in a convenience class that allows attribute access to the keys in the returned dictionary. All the metadata for the results are accessible via `meta` (without the leading `_`):

```python
response = s.execute()
h = response.hits[0]
print(f"/{h.meta.index}/{h.meta.doc_type}/{h.meta.id} returned with score {h.meta.score}")
```

::::{note}
If your document has a field called `meta` you have to access it using the get item syntax: `hit['meta']`.

::::



#### Aggregations [_aggregations_2]

Aggregations are available through the `aggregations` property:

```python
for tag in response.aggregations.per_tag.buckets:
    print(tag.key, tag.max_lines.value)
```



### `MultiSearch` [_multisearch]

If you need to execute multiple searches at the same time you can use the `MultiSearch` class which will use the `_msearch` API:

```python
from elasticsearch.dsl import MultiSearch, Search
from elasticsearch.dsl.query import Term

ms = MultiSearch(index='blogs')

ms = ms.add(Search().filter(Term("tags", "python")))
ms = ms.add(Search().filter(Term("tags", 'elasticsearch')))

responses = ms.execute()

for response in responses:
    print("Results for query %r." % response._search.query)
    for hit in response:
        print(hit.title)
```


### `EmptySearch` [_emptysearch]

The `EmptySearch` class can be used as a fully compatible version of `Search` that will return no results, regardless of any queries configured.



## Persistence [_persistence_2]

You can use the DSL module to define your mappings and a basic persistent layer for your application.

For more comprehensive examples have a look at the [DSL examples](https://github.com/elastic/elasticsearch-py/tree/main/examples/dsl) directory in the repository.

### Document [doc_type]

If you want to create a model-like wrapper around your documents, use the `Document` class. It can also be used to create all the necessary mappings and settings in elasticsearch (see `life-cycle` for details).

```python
from datetime import datetime
from elasticsearch.dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text

html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

class Comment(InnerDoc):
    author = Text(fields={'raw': Keyword()})
    content = Text(analyzer='snowball')
    created_at = Date()

    def age(self):
        return datetime.now() - self.created_at

class Post(Document):
    title = Text()
    title_suggest = Completion()
    created_at = Date()
    published = Boolean()
    category = Text(
        analyzer=html_strip,
        fields={'raw': Keyword()}
    )

    comments = Nested(Comment)

    class Index:
        name = 'blog'

    def add_comment(self, author, content):
        self.comments.append(
          Comment(author=author, content=content, created_at=datetime.now()))

    def save(self, ** kwargs):
        self.created_at = datetime.now()
        return super().save(** kwargs)
```

#### Data types [_data_types]

The `Document` instances use native python types such as `str` and `datetime` for its attributes. In case of `Object` or `Nested` fields an instance of the `InnerDoc` subclass is used, as in the `add_comment` method in the above example, where we are creating an instance of the `Comment` class.

There are some specific types that were created to make working with some field types easier, for example the `Range` object used in any of the [range fields](elasticsearch://reference/elasticsearch/mapping-reference/range.md):

```python
from elasticsearch.dsl import Document, DateRange, Keyword, Range

class RoomBooking(Document):
    room = Keyword()
    dates = DateRange()

rb = RoomBooking(
  room='Conference Room II',
  dates=Range(
    gte=datetime(2018, 11, 17, 9, 0, 0),
    lt=datetime(2018, 11, 17, 10, 0, 0)
  )
)

# Range supports the in operator correctly:
datetime(2018, 11, 17, 9, 30, 0) in rb.dates # True

# you can also get the limits and whether they are inclusive or exclusive:
rb.dates.lower # datetime(2018, 11, 17, 9, 0, 0), True
rb.dates.upper # datetime(2018, 11, 17, 10, 0, 0), False

# empty range is unbounded
Range().lower # None, False
```


#### Python Type Hints [_python_type_hints]

Document fields can be defined using standard Python type hints if desired. Here are some simple examples:

```python
from typing import Optional

class Post(Document):
    title: str                      # same as title = Text(required=True)
    created_at: Optional[datetime]  # same as created_at = Date(required=False)
    published: bool                 # same as published = Boolean(required=True)
```

It is important to note that when using `Field` subclasses such as `Text`, `Date` and `Boolean`, they must be given in the right-side of an assignment, as shown in examples above. Using these classes as type hints will result in errors.

Python types are mapped to their corresponding field types according to the following table:

| Python type | DSL field |
| --- | --- |
| `str` | `Text(required=True)` |
| `bool` | `Boolean(required=True)` |
| `int` | `Integer(required=True)` |
| `float` | `Float(required=True)` |
| `bytes` | `Binary(required=True)` |
| `datetime` | `Date(required=True)` |
| `date` | `Date(format="yyyy-MM-dd", required=True)` |

To type a field as optional, the standard `Optional` modifier from the Python `typing` package can be used. When using Python 3.10 or newer, "pipe" syntax can also be used, by adding `| None` to a type. The `List` modifier can be added to a field to convert it to an array, similar to using the `multi=True` argument on the field object.

```python
from typing import Optional, List

class MyDoc(Document):
    pub_date: Optional[datetime]  # same as pub_date = Date()
    middle_name: str | None       # same as middle_name = Text()
    authors: List[str]            # same as authors = Text(multi=True, required=True)
    comments: Optional[List[str]] # same as comments = Text(multi=True)
```

A field can also be given a type hint of an `InnerDoc` subclass, in which case it becomes an `Object` field of that class. When the `InnerDoc` subclass is wrapped with `List`, a `Nested` field is created instead.

```python
from typing import List

class Address(InnerDoc):
    ...

class Comment(InnerDoc):
    ...

class Post(Document):
    address: Address         # same as address = Object(Address, required=True)
    comments: List[Comment]  # same as comments = Nested(Comment, required=True)
```

Unfortunately it is impossible to have Python type hints that uniquely identify every possible Elasticsearch field type. To choose a field type that is different than the one that is assigned according to the table above, the desired field instance can be added explicitly as a right-side assignment in the field declaration. The next example creates a field that is typed as `Optional[str]`, but is mapped to `Keyword` instead of `Text`:

```python
class MyDocument(Document):
    category: Optional[str] = Keyword()
```

This form can also be used when additional options need to be given to initialize the field, such as when using custom analyzer settings:

```python
class Comment(InnerDoc):
    content: str = Text(analyzer='snowball')
```

When using type hints as above, subclasses of `Document` and `InnerDoc` inherit some of the behaviors associated with Python dataclasses, as defined by [PEP 681](https://peps.python.org/pep-0681/) and the [dataclass_transform decorator](https://typing.readthedocs.io/en/latest/spec/dataclasses.html#dataclass-transform). To add per-field dataclass options such as `default` or `default_factory`, the `mapped_field()` wrapper can be used on the right side of a typed field declaration:

```python
class MyDocument(Document):
    title: str = mapped_field(default="no title")
    created_at: datetime = mapped_field(default_factory=datetime.now)
    published: bool = mapped_field(default=False)
    category: str = mapped_field(Keyword(), default="general")
```

When using the `mapped_field()` wrapper function, an explicit field type instance can be passed as a first positional argument, as the `category` field does in the example above.

Static type checkers such as [mypy](https://mypy-lang.org/) and [pyright](https://github.com/microsoft/pyright) can use the type hints and the dataclass-specific options added to the `mapped_field()` function to improve type inference and provide better real-time code completion and suggestions in IDEs.

One situation in which type checkers can’t infer the correct type is when using fields as class attributes. Consider the following example:

```python
class MyDocument(Document):
    title: str

doc = MyDocument()
# doc.title is typed as "str" (correct)
# MyDocument.title is also typed as "str" (incorrect)
```

To help type checkers correctly identify class attributes as such, the `M` generic must be used as a wrapper to the type hint, as shown in the next examples:

```python
from elasticsearch.dsl import M

class MyDocument(Document):
    title: M[str]
    created_at: M[datetime] = mapped_field(default_factory=datetime.now)

doc = MyDocument()
# doc.title is typed as "str"
# doc.created_at is typed as "datetime"
# MyDocument.title is typed as "InstrumentedField"
# MyDocument.created_at is typed as "InstrumentedField"
```

Note that the `M` type hint does not provide any runtime behavior and its use is not required, but it can be useful to eliminate spurious type errors in IDEs or type checking builds.

The `InstrumentedField` objects returned when fields are accessed as class attributes are proxies for the field instances that can be used anywhere a field needs to be referenced, such as when specifying sort options in a `Search` object:

```python
# sort by creation date descending, and title ascending
s = MyDocument.search().sort(-MyDocument.created_at, MyDocument.title)
```

When specifying sorting order, the `+` and `-` unary operators can be used on the class field attributes to indicate ascending and descending order.

Finally, the `ClassVar` annotation can be used to define a regular class attribute that should not be mapped to the Elasticsearch index:

```python
from typing import ClassVar

class MyDoc(Document):
    title: M[str] created_at: M[datetime] = mapped_field(default_factory=datetime.now)
    my_var: ClassVar[str]  # regular class variable, ignored by Elasticsearch
```


#### Note on dates [_note_on_dates]

The DSL module will always respect the timezone information (or lack thereof) on the `datetime` objects passed in or stored in Elasticsearch. Elasticsearch itself interprets all datetimes with no timezone information as `UTC`. If you wish to reflect this in your python code, you can specify `default_timezone` when instantiating a `Date` field:

```python
class Post(Document):
    created_at = Date(default_timezone='UTC')
```

In that case any `datetime` object passed in (or parsed from elasticsearch) will be treated as if it were in `UTC` timezone.


#### Document life cycle [life-cycle]

Before you first use the `Post` document type, you need to create the mappings in Elasticsearch. For that you can either use the `index` object or create the mappings directly by calling the `init` class method:

```python
# create the mappings in Elasticsearch
Post.init()
```

This code will typically be run in the setup for your application during a code deploy, similar to running database migrations.

To create a new `Post` document just instantiate the class and pass in any fields you wish to set, you can then use standard attribute setting to change/add more fields. Note that you are not limited to the fields defined explicitly:

```python
# instantiate the document
first = Post(title='My First Blog Post, yay!', published=True)
# assign some field values, can be values or lists of values
first.category = ['everything', 'nothing']
# every document has an id in meta
first.meta.id = 47


# save the document into the cluster
first.save()
```

All the metadata fields (`id`, `routing`, `index` etc) can be accessed (and set) via a `meta` attribute or directly using the underscored variant:

```python
post = Post(meta={'id': 42})

# prints 42
print(post.meta.id)

# override default index
post.meta.index = 'my-blog'
```

::::{note}
Having all metadata accessible through `meta` means that this name is reserved and you shouldn’t have a field called `meta` on your document. If you, however, need it you can still access the data using the get item (as opposed to attribute) syntax: `post['meta']`.

::::


To retrieve an existing document use the `get` class method:

```python
# retrieve the document
first = Post.get(id=42)
# now we can call methods, change fields, ...
first.add_comment('me', 'This is nice!')
# and save the changes into the cluster again
first.save()
```

The [Update API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-document) can also be used via the `update` method. By default any keyword arguments, beyond the parameters of the API, will be considered fields with new values. Those fields will be updated on the local copy of the document and then sent over as partial document to be updated:

```python
# retrieve the document
first = Post.get(id=42)
# you can update just individual fields which will call the update API
# and also update the document in place
first.update(published=True, published_by='me')
```

In case you wish to use a `painless` script to perform the update you can pass in the script string as `script` or the `id` of a [stored script](docs-content://explore-analyze/scripting/modules-scripting-using.md#script-stored-scripts) via `script_id`. All additional keyword arguments to the `update` method will then be passed in as parameters of the script. The document will not be updated in place.

```python
# retrieve the document
first = Post.get(id=42)
# we execute a script in elasticsearch with additional kwargs being passed
# as params into the script
first.update(script='ctx._source.category.add(params.new_category)',
             new_category='testing')
```

If the document is not found in elasticsearch an exception (`elasticsearch.NotFoundError`) will be raised. If you wish to return `None` instead just pass in `ignore=404` to suppress the exception:

```python
p = Post.get(id='not-in-es', ignore=404)
p is None
```

When you wish to retrieve multiple documents at the same time by their `id` you can use the `mget` method:

```python
posts = Post.mget([42, 47, 256])
```

`mget` will, by default, raise a `NotFoundError` if any of the documents wasn’t found and `RequestError` if any of the document had resulted in error. You can control this behavior by setting parameters:

* `raise_on_error`: If `True` (default) then any error will cause an exception to be raised. Otherwise all documents containing errors will be treated as missing.
* `missing`: Can have three possible values: `'none'` (default), `'raise'` and `'skip'`. If a document is missing or errored it will either be replaced with `None`, an exception will be raised or the document will be skipped in the output list entirely.

The index associated with the `Document` is accessible via the `_index` class property which gives you access to the `index` class.

The `_index` attribute is also home to the `load_mappings` method which will update the mapping on the `Index` from elasticsearch. This is very useful if you use dynamic mappings and want the class to be aware of those fields (for example if you wish the `Date` fields to be properly (de)serialized):

```python
Post._index.load_mappings()
```

To delete a document just call its `delete` method:

```python
first = Post.get(id=42)
first.delete()
```


#### Analysis [_analysis]

To specify `analyzer` values for `Text` fields you can just use the name of the analyzer (as a string) and either rely on the analyzer being defined (like built-in analyzers) or define the analyzer yourself manually.

Alternatively you can create your own analyzer and have the persistence layer handle its creation, from our example earlier:

```python
from elasticsearch.dsl import analyzer, tokenizer

my_analyzer = analyzer('my_analyzer',
    tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
    filter=['lowercase']
)
```

Each analysis object needs to have a name (`my_analyzer` and `trigram` in our example) and tokenizers, token filters and char filters also need to specify type (`nGram` in our example).

Once you have an instance of a custom `analyzer` you can also call the [analyze API](https://www.elastic.co/docs/api/doc/elasticsearch/v8/group/endpoint-indices) on it by using the `simulate` method:

```python
response = my_analyzer.simulate('Hello World!')

# ['hel', 'ell', 'llo', 'lo ', 'o w', ' wo', 'wor', 'orl', 'rld', 'ld!']
tokens = [t.token for t in response.tokens]
```

::::{note}
When creating a mapping which relies on a custom analyzer the index must either not exist or be closed. To create multiple `Document`-defined mappings you can use the `index` object.

::::



#### Search [_search_2]

To search for this document type, use the `search` class method:

```python
# by calling .search we get back a standard Search object
s = Post.search()
# the search is already limited to the index and doc_type of our document
s = s.filter('term', published=True).query('match', title='first')


results = s.execute()

# when you execute the search the results are wrapped in your document class (Post)
for post in results:
    print(post.meta.score, post.title)
```

Alternatively you can just take a `Search` object and restrict it to return our document type, wrapped in correct class:

```python
s = Search()
s = s.doc_type(Post)
```

You can also combine document classes with standard doc types (just strings), which will be treated as before. You can also pass in multiple `Document` subclasses and each document in the response will be wrapped in it’s class.

If you want to run suggestions, just use the `suggest` method on the `Search` object:

```python
s = Post.search()
s = s.suggest('title_suggestions', 'pyth', completion={'field': 'title_suggest'})

response = s.execute()

for result in response.suggest.title_suggestions:
    print('Suggestions for %s:' % result.text)
    for option in result.options:
        print('  %s (%r)' % (option.text, option.payload))
```


#### `class Meta` options [_class_meta_options]

In the `Meta` class inside your document definition you can define various metadata for your document:

* `mapping`: optional instance of `Mapping` class to use as base for the mappings created from the fields on the document class itself.

Any attributes on the `Meta` class that are instance of `MetaField` will be used to control the mapping of the meta fields (`_all`, `dynamic` etc). Just name the parameter (without the leading underscore) as the field you wish to map and pass any parameters to the `MetaField` class:

```python
class Post(Document):
    title = Text()

    class Meta:
        all = MetaField(enabled=False)
        dynamic = MetaField('strict')
```


#### `class Index` options [_class_index_options]

This section of the `Document` definition can contain any information about the index, its name, settings and other attributes:

* `name`: name of the index to use, if it contains a wildcard (`*`) then it cannot be used for any write operations and an `index` kwarg will have to be passed explicitly when calling methods like `.save()`.
* `using`: default connection alias to use, defaults to `'default'`
* `settings`: dictionary containing any settings for the `Index` object like `number_of_shards`.
* `analyzers`: additional list of analyzers that should be defined on an index (see `analysis` for details).
* `aliases`: dictionary with any aliases definitions


#### Document Inheritance [_document_inheritance]

You can use standard Python inheritance to extend models, this can be useful in a few scenarios. For example if you want to have a `BaseDocument` defining some common fields that several different `Document` classes should share:

```python
class User(InnerDoc):
    username: str = mapped_field(Text(fields={'keyword': Keyword()}))
    email: str

class BaseDocument(Document):
    created_by: User
    created_date: datetime
    last_updated: datetime

    def save(**kwargs):
        if not self.created_date:
            self.created_date = datetime.now()
        self.last_updated = datetime.now()
        return super(BaseDocument, self).save(**kwargs)

class BlogPost(BaseDocument):
    class Index:
        name = 'blog'
```

Another use case would be using the [join type](elasticsearch://reference/elasticsearch/mapping-reference/parent-join.md) to have multiple different entities in a single index. You can see an [example](https://github.com/elastic/elasticsearch-py/blob/master/examples/dsl/parent_child.py) of this approach. Note that in this case, if the subclasses don’t define their own Index classes, the mappings are merged and shared between all the subclasses.



### Index [_index]

In typical scenario using `class Index` on a `Document` class is sufficient to perform any action. In a few cases though it can be useful to manipulate an `Index` object directly.

`Index` is a class responsible for holding all the metadata related to an index in elasticsearch - mappings and settings. It is most useful when defining your mappings since it allows for easy creation of multiple mappings at the same time. This is especially useful when setting up your elasticsearch objects in a migration:

```python
from elasticsearch.dsl import Index, Document, Text, analyzer

blogs = Index('blogs')

# define custom settings
blogs.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# define aliases
blogs.aliases(
    old_blogs={}
)

# register a document with the index
blogs.document(Post)

# can also be used as class decorator when defining the Document
@blogs.document
class Post(Document):
    title: str

# You can attach custom analyzers to the index

html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

blogs.analyzer(html_strip)

# delete the index, ignore if it doesn't exist
blogs.delete(ignore=404)

# create the index in elasticsearch
blogs.create()
```

You can also set up a template for your indices and use the `clone` method to create specific copies:

```python
blogs = Index('blogs', using='production')
blogs.settings(number_of_shards=2)
blogs.document(Post)

# create a copy of the index with different name
company_blogs = blogs.clone('company-blogs')

# create a different copy on different cluster
dev_blogs = blogs.clone('blogs', using='dev')
# and change its settings
dev_blogs.setting(number_of_shards=1)
```

#### IndexTemplate [index-template]

The DSL module also exposes an option to manage [index templates](docs-content://manage-data/data-store/templates.md) in elasticsearch using the `ComposableIndexTemplate` and `IndexTemplate` classes, which have very similar API to `Index`.

::::{note}
Composable index templates should be always be preferred over the legacy index templates, since the latter are deprecated.

::::


Once an index template is saved in Elasticsearch its contents will be automatically applied to new indices (existing indices are completely unaffected by templates) that match the template pattern (any index starting with `blogs-` in our example), even if the index is created automatically upon indexing a document into that index.

Potential workflow for a set of time based indices governed by a single template:

```python
from datetime import datetime

from elasticsearch.dsl import Document, Date, Text


class Log(Document):
    content: str
    timestamp: datetime

    class Index:
        name = "logs-*"

    def save(self, **kwargs):
        # assign now if no timestamp given
        if not self.timestamp:
            self.timestamp = datetime.now()

        # override the index to go to the proper timeslot
        kwargs['index'] = self.timestamp.strftime('logs-%Y%m%d')
        return super().save(**kwargs)

# once, as part of application setup, during deploy/migrations:
logs = Log._index.as_composable_template('logs', priority=100)
logs.save()

# to perform search across all logs:
search = Log.search()
```




## Faceted Search [faceted_search]

The library comes with a simple abstraction aimed at helping you develop faceted navigation for your data.

### Configuration [_configuration_2]

You can provide several configuration options (as class attributes) when declaring a `FacetedSearch` subclass:

* `index`: the name of the index (as string) to search through, defaults to `'_all'`.
* `doc_types`: list of `Document` subclasses or strings to be used, defaults to `['_all']`.
* `fields`: list of fields on the document type to search through. The list will be passes to `MultiMatch` query so can contain boost values (`'title^5'`), defaults to `['*']`.
* `facets`: dictionary of facets to display/filter on. The key is the name displayed and values should be instances of any `Facet` subclass, for example: `{'tags': TermsFacet(field='tags')}`

#### Facets [_facets]

There are several different facets available:

* `TermsFacet`: provides an option to split documents into groups based on a value of a field, for example `TermsFacet(field='category')`
* `DateHistogramFacet`: split documents into time intervals, example: `DateHistogramFacet(field="published_date", calendar_interval="day")`
* `HistogramFacet`: similar to `DateHistogramFacet` but for numerical values: `HistogramFacet(field="rating", interval=2)`
* `RangeFacet`: allows you to define your own ranges for a numerical fields: `RangeFacet(field="comment_count", ranges=[("few", (None, 2)), ("lots", (2, None))])`
* `NestedFacet`: is just a simple facet that wraps another to provide access to nested documents: `NestedFacet('variants', TermsFacet(field='variants.color'))`

By default facet results will only calculate document count, if you wish for a different metric you can pass in any single value metric aggregation as the `metric` kwarg (`TermsFacet(field='tags', metric=A('max', field=timestamp))`). When specifying `metric` the results will be, by default, sorted in descending order by that metric. To change it to ascending specify `metric_sort="asc"` and to just sort by document count use `metric_sort=False`.


#### Advanced [_advanced]

If you require any custom behavior or modifications simply override one or more of the methods responsible for the class' functions:

* `search(self)`: is responsible for constructing the `Search` object used. Override this if you want to customize the search object (for example by adding a global filter for published articles only).
* `query(self, search)`: adds the query position of the search (if search input specified), by default using `MultiField` query. Override this if you want to modify the query type used.
* `highlight(self, search)`: defines the highlighting on the `Search` object and returns a new one. Default behavior is to highlight on all fields specified for search.



### Usage [_usage]

The custom subclass can be instantiated empty to provide an empty search (matching everything) or with `query`, `filters` and `sort`.

* `query`: is used to pass in the text of the query to be performed. If `None` is passed in (default) a `MatchAll` query will be used. For example `'python web'`
* `filters`: is a dictionary containing all the facet filters that you wish to apply. Use the name of the facet (from `.facets` attribute) as the key and one of the possible values as value. For example `{'tags': 'python'}`.
* `sort`: is a tuple or list of fields on which the results should be sorted. The format of the individual fields are to be the same as those passed to `~elasticsearch.dsl.Search.sort`.

#### Response [_response_2]

the response returned from the `FacetedSearch` object (by calling `.execute()`) is a subclass of the standard `Response` class that adds a property called `facets` which contains a dictionary with lists of buckets -each represented by a tuple of key, document count and a flag indicating whether this value has been filtered on.



### Example [_example]

```python
from datetime import date

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

    def search(self):
        # override methods to add custom pieces
        s = super().search()
        return s.filter('range', publish_from={'lte': 'now/h'})

bs = BlogSearch('python web', {'publishing_frequency': date(2015, 6)})
response = bs.execute()

# access hits and other attributes as usual
total = response.hits.total
print('total hits', total.relation, total.value)
for hit in response:
    print(hit.meta.score, hit.title)

for (tag, count, selected) in response.facets.tags:
    print(tag, ' (SELECTED):' if selected else ':', count)

for (month, count, selected) in response.facets.publishing_frequency:
    print(month.strftime('%B %Y'), ' (SELECTED):' if selected else ':', count)
```



## Update By Query [update_by_query]

### The `Update By Query` object [_the_update_by_query_object]

The `Update By Query` object enables the use of the [_update_by_query](https://www.elastic.co/docs/api/doc/elasticsearch/v8/operation/operation-update-by-query) endpoint to perform an update on documents that match a search query.

The object is implemented as a modification of the `Search` object, containing a subset of its query methods, as well as a script method, which is used to make updates.

The `Update By Query` object implements the following `Search` query types:

* queries
* filters
* excludes

For more information on queries, see the `search_dsl` chapter.

Like the `Search` object, the API is designed to be chainable. This means that the `Update By Query` object is immutable: all changes to the object will result in a shallow copy being created which contains the changes. This means you can safely pass the `Update By Query` object to foreign code without fear of it modifying your objects as long as it sticks to the `Update By Query` object APIs.

You can define your client in a number of ways, but the preferred method is to use a global configuration. For more information on defining a client, see the `configuration` chapter.

Once your client is defined, you can instantiate a copy of the `Update By Query` object as seen below:

```python
from elasticsearch.dsl import UpdateByQuery

ubq = UpdateByQuery().using(client)
# or
ubq = UpdateByQuery(using=client)
```

::::{note}
All methods return a *copy* of the object, making it safe to pass to outside code.

::::


The API is chainable, allowing you to combine multiple method calls in one statement:

```python
ubq = UpdateByQuery().using(client).query(Match("title", python"))
```

To send the request to Elasticsearch:

```python
response = ubq.execute()
```

It should be noted, that there are limits to the chaining using the script method: calling script multiple times will overwrite the previous value. That is, only a single script can be sent with a call. An attempt to use two scripts will result in only the second script being stored.

Given the below example:

```python
ubq = UpdateByQuery() \
    .using(client) \
    .script(source="ctx._source.likes++") \
    .script(source="ctx._source.likes+=2")
```

This means that the stored script by this client will be `'source': 'ctx._source.likes{{plus}}=2'` and the previous call will not be stored.

For debugging purposes you can serialize the `Update By Query` object to a `dict` explicitly:

```python
print(ubq.to_dict())
```

Also, to use variables in script see below example:

```python
ubq.script(
  source="ctx._source.messages.removeIf(x -> x.somefield == params.some_var)",
  params={
    'some_var': 'some_string_val'
  }
)
```

#### Serialization and Deserialization [_serialization_and_deserialization_2]

The search object can be serialized into a dictionary by using the `.to_dict()` method.

You can also create a `Update By Query` object from a `dict` using the `from_dict` class method. This will create a new `Update By Query` object and populate it using the data from the dict:

```python
ubq = UpdateByQuery.from_dict({"query": {"match": {"title": "python"}}})
```

If you wish to modify an existing `Update By Query` object, overriding it’s properties, instead use the `update_from_dict` method that alters an instance **in-place**:

```python
ubq = UpdateByQuery(index='i')
ubq.update_from_dict({"query": {"match": {"title": "python"}}, "size": 42})
```


#### Extra properties and parameters [_extra_properties_and_parameters_2]

To set extra properties of the search request, use the `.extra()` method. This can be used to define keys in the body that cannot be defined via a specific API method like `explain`:

```python
ubq = ubq.extra(explain=True)
```

To set query parameters, use the `.params()` method:

```python
ubq = ubq.params(routing="42")
```



### Response [_response_3]

You can execute your search by calling the `.execute()` method that will return a `Response` object. The `Response` object allows you access to any key from the response dictionary via attribute access. It also provides some convenient helpers:

```python
response = ubq.execute()

print(response.success())
# True

print(response.took)
# 12
```

If you want to inspect the contents of the `response` objects, just use its `to_dict` method to get access to the raw data for pretty printing.


## ES|QL Queries

When working with `Document` classes, you can use the ES|QL query language to retrieve documents. For this you can use the `esql_from()` and `esql_execute()` methods available to all sub-classes of `Document`.

Consider the following `Employee` document definition:

```python
from elasticsearch.dsl import Document, InnerDoc, M

class Address(InnerDoc):
    address: M[str]
    city: M[str]
    zip_code: M[str]

class Employee(Document):
    emp_no: M[int]
    first_name: M[str]
    last_name: M[str]
    height: M[float]
    still_hired: M[bool]
    address: M[Address]

    class Index:
        name = 'employees'
```

The `esql_from()` method creates a base ES|QL query for the index associated with the document class. The following example creates a base query for the `Employee` class:

```python
query = Employee.esql_from()
```

This query includes a `FROM` command with the index name, and a `KEEP` command that retrieves all the document attributes.

To execute this query and receive the results, you can pass the query to the `esql_execute()` method:

```python
for emp in Employee.esql_execute(query):
    print(f"{emp.name} from {emp.address.city} is {emp.height:.2f}m tall")
```

In this example, the `esql_execute()` class method runs the query and returns all the documents in the index, up to the maximum of 1000 results allowed by ES|QL. Here is a possible output from this example:

```
Kevin Macias from North Robert is 1.60m tall
Drew Harris from Boltonshire is 1.68m tall
Julie Williams from Maddoxshire is 1.99m tall
Christopher Jones from Stevenbury is 1.98m tall
Anthony Lopez from Port Sarahtown is 2.42m tall
Tricia Stone from North Sueshire is 2.39m tall
Katherine Ramirez from Kimberlyton is 1.83m tall
...
```

To search for specific documents you can extend the base query with additional ES|QL commands that narrow the search criteria. The next example searches for documents that include only employees that are taller than 2 meters, sorted by their last name. It also limits the results to 4 people:

```python
query = (
    Employee.esql_from()
    .where(Employee.height > 2)
    .sort(Employee.last_name)
    .limit(4)
)
```

When running this query with the same for-loop shown above, possible results would be:

```
Michael Adkins from North Stacey is 2.48m tall
Kimberly Allen from Toddside is 2.24m tall
Crystal Austin from East Michaelchester is 2.30m tall
Rebecca Berger from Lake Adrianside is 2.40m tall
```

### Additional fields

ES|QL provides a few ways to add new fields to a query, for example through the `EVAL` command. The following example shows a query that adds an evaluated field:

```python
from elasticsearch.esql import E, functions

query = (
    Employee.esql_from()
    .eval(height_cm=functions.round(Employee.height * 100))
    .where(E("height_cm") >= 200)
    .sort(Employee.last_name)
    .limit(10)
)
```

In this example we are adding the height in centimeters to the query, calculated from the `height` document field, which is in meters. The `height_cm` calculated field is available to use in other query clauses, and in particular is referenced in `where()` in this example. Note how the new field is given as `E("height_cm")` in this clause. The `E()` wrapper tells the query builder that the argument is an ES|QL field name and not a string literal. This is done automatically for document fields that are given as class attributes, such as `Employee.height` in the `eval()`. The `E()` wrapper is only needed for fields that are not in the document.

By default, the `esql_execute()` method returns only document instances. To receive any additional fields that are not part of the document in the query results, the `return_additional=True` argument can be passed to it, and then the results are returned as tuples with the document as first element, and a dictionary with the additional fields as second element:

```python
for emp, additional in Employee.esql_execute(query, return_additional=True):
    print(emp.name, additional)
```

Example output from the query given above:

```
Michael Adkins {'height_cm': 248.0}
Kimberly Allen {'height_cm': 224.0}
Crystal Austin {'height_cm': 230.0}
Rebecca Berger {'height_cm': 240.0}
Katherine Blake {'height_cm': 214.0}
Edward Butler {'height_cm': 246.0}
Steven Carlson {'height_cm': 242.0}
Mark Carter {'height_cm': 240.0}
Joseph Castillo {'height_cm': 229.0}
Alexander Cohen {'height_cm': 245.0}
```

### Missing fields

The base query returned by the `esql_from()` method includes a `KEEP` command with the complete list of fields that are part of the document. If any subsequent clauses added to the query remove fields that are part of the document, then the `esql_execute()` method will raise an exception, because it will not be able construct complete document instances to return as results.

To prevent errors, it is recommended that the `keep()` and `drop()` clauses are not used when working with `Document` instances.

If a query has missing fields, it can be forced to execute without errors by passing the `ignore_missing_fields=True` argument to `esql_execute()`. When this option is used, returned documents will have any missing fields set to `None`.

## Using asyncio with Elasticsearch Python DSL [asyncio]

The DSL module supports async/await with [asyncio](https://docs.python.org/3/library/asyncio.html). To ensure that you have all the required dependencies, install the `[async]` extra:

```bash
$ python -m pip install "elasticsearch[async]"
```

### Connections [_connections]

Use the `async_connections` module to manage your asynchronous connections.

```python
from elasticsearch.dsl import async_connections

async_connections.create_connection(hosts=['localhost'], timeout=20)
```

All the options available in the `connections` module can be used with `async_connections`.

#### How to avoid *Unclosed client session / connector* warnings on exit [_how_to_avoid_unclosed_client_session_connector_warnings_on_exit]

These warnings come from the `aiohttp` package, which is used internally by the `AsyncElasticsearch` client. They appear often when the application exits and are caused by HTTP connections that are open when they are garbage collected. To avoid these warnings, make sure that you close your connections.

```python
es = async_connections.get_connection()
await es.close()
```



### Search DSL [_search_dsl]

Use the `AsyncSearch` class to perform asynchronous searches.

```python
from elasticsearch.dsl import AsyncSearch
from elasticsearch.dsl.query import Match

s = AsyncSearch().query(Match("title", "python"))
async for hit in s:
    print(hit.title)
```

Instead of using the `AsyncSearch` object as an asynchronous iterator, you can explicitly call the `execute()` method to get a `Response` object.

```python
s = AsyncSearch().query(Match("title", "python"))
response = await s.execute()
for hit in response:
    print(hit.title)
```

An `AsyncMultiSearch` is available as well.

```python
from elasticsearch.dsl import AsyncMultiSearch
from elasticsearch.dsl.query import Term

ms = AsyncMultiSearch(index='blogs')

ms = ms.add(AsyncSearch().filter(Term("tags", "python")))
ms = ms.add(AsyncSearch().filter(Term("tags", "elasticsearch")))

responses = await ms.execute()

for response in responses:
    print("Results for query %r." % response.search.query)
    for hit in response:
        print(hit.title)
```


### Asynchronous Documents, Indexes, and more [_asynchronous_documents_indexes_and_more]

The `Document`, `Index`, `IndexTemplate`, `Mapping`, `UpdateByQuery` and `FacetedSearch` classes all have asynchronous versions that use the same name with an `Async` prefix. These classes expose the same interfaces as the synchronous versions, but any methods that perform I/O are defined as coroutines.

Auxiliary classes that do not perform I/O do not have asynchronous versions. The same classes can be used in synchronous and asynchronous applications.

When using a custom analyzer in an asynchronous application, use the `async_simulate()` method to invoke the Analyze API on it.

Consult the `api` section for details about each specific method.




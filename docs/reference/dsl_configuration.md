---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/_configuration.html
navigation_title: Configuration
---

# Python DSL configuration for {{es}} [_configuration]

There are several ways to configure connections for the library. The easiest and most useful approach is to define one default connection that can be used every time an API call is made without explicitly passing in other connections.

::::{note}
Unless you want to access multiple clusters from your application, it is highly recommended that you use the `create_connection` method and all operations will use that connection automatically.

::::


## Default connection [_default_connection]

To define a default connection that can be used globally, use the `connections` module and the `create_connection` method like this:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
from elasticsearch.dsl import connections

connections.create_connection(hosts=['https://localhost:9200'], request_timeout=20)
```
:::

:::{tab-item} Async Python
:sync: async
```python
from elasticsearch.dsl import async_connections

async_connections.create_connection(hosts=['https://localhost:9200'], request_timeout=20)
```
:::

::::

### Single connection with an alias [_single_connection_with_an_alias]

You can define the `alias` or name of a connection so you can easily refer to it later. The default value for `alias` is `default`.

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
from elasticsearch.dsl import connections

connections.create_connection(alias='my_new_connection', hosts=['https://localhost:9200'], request_timeout=60)
```
:::

:::{tab-item} Async Python
:sync: async
```python
from elasticsearch.dsl import async_connections

async_connections.create_connection(alias='my_new_connection', hosts=['https://localhost:9200'], request_timeout=60)
```
:::

::::

Additional keyword arguments (`hosts` and `timeout` in our example) will be passed to the `Elasticsearch` class from `elasticsearch-py`.

To see all possible configuration options refer to the [documentation](https://elasticsearch-py.readthedocs.io/en/latest/api/elasticsearch.html).



## Multiple clusters [_multiple_clusters]

You can define multiple connections to multiple clusters at the same time using the `configure` method:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
from elasticsearch.dsl import connections

connections.configure(
    default={'hosts': 'https://localhost:9200'},
    dev={
        'hosts': ['https://esdev1.example.com:9200'],
        'sniff_on_start': True
    }
)
```
:::

:::{tab-item} Async Python
:sync: async
```python
from elasticsearch.dsl import async_connections

async_connections.configure(
    default={'hosts': 'https://localhost:9200'},
    dev={
        'hosts': ['https://esdev1.example.com:9200'],
        'sniff_on_start': True
    }
)
```
:::

::::

Such connections will be constructed lazily when requested for the first time.

You can alternatively define multiple connections by adding them one by one as shown in the following example:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
# if you have configuration options to be passed to Elasticsearch.__init__
# this also shows creating a connection with the alias 'qa'
connections.create_connection('qa', hosts=['esqa1.example.com'], sniff_on_start=True)

# if you already have an Elasticsearch instance ready
connections.add_connection('another_qa', my_client)
```
:::

:::{tab-item} Async Python
:sync: async
```python
# if you have configuration options to be passed to Elasticsearch.__init__
# this also shows creating a connection with the alias 'qa'
async_connections.create_connection('qa', hosts=['esqa1.example.com'], sniff_on_start=True)

# if you already have an Elasticsearch instance ready
async_connections.add_connection('another_qa', my_client)
```
:::

::::

### Using aliases [_using_aliases]

When using multiple connections, you can refer to them using the string alias specified when you created the connection.

This example shows how to use an alias to a connection:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
s = Search(using='qa')
```
:::

:::{tab-item} Async Python
:sync: async
```python
s = AsyncSearch(using='qa')
```
:::

::::

A `KeyError` will be raised if there is no connection registered with that alias.



## Manual [_manual]

If you don’t want to supply a global configuration, you can always pass in your own connection as an instance of `elasticsearch.Elasticsearch` with the parameter `using` wherever it is accepted like this:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
s = Search(using=Elasticsearch('https://localhost:9200'))
```
:::

:::{tab-item} Async Python
:sync: async
```python
s = AsyncSearch(using=AsyncElasticsearch('https://localhost:9200'))
```
:::

::::

You can even use this approach to override any connection the object might be already associated with:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
s = s.using(Elasticsearch('https://otherhost:9200'))
```
:::

:::{tab-item} Async Python
:sync: async
```python
s = s.using(AsyncElasticsearch('https://otherhost:9200'))
```
:::

::::

::::{note}
When using the `dsl` module, it is highly recommended that you use the built-in serializer (`elasticsearch.dsl.serializer.serializer`) to ensure your objects are correctly serialized into `JSON` every time. The `create_connection` method that is described here (and that the `configure` method uses under the hood) will do that automatically for you, unless you explicitly specify your own serializer. The built-in serializer also allows you to serialize your own objects - just define a `to_dict()` method on your objects and that method will be automatically called when serializing your custom objects to `JSON`.

::::




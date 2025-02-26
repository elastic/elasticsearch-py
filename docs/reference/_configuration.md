---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/_configuration.html
---

# Configuration [_configuration]

There are several ways to configure connections for the library. The easiest and most useful approach is to define one default connection that can be used every time an API call is made without explicitly passing in other connections.

::::{note}
Unless you want to access multiple clusters from your application, it is highly recommended that you use the `create_connection` method and all operations will use that connection automatically.

::::


## Default connection [_default_connection]

To define a default connection that can be used globally, use the `connections` module and the `create_connection` method like this:

```python
from elasticsearch.dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)
```

### Single connection with an alias [_single_connection_with_an_alias]

You can define the `alias` or name of a connection so you can easily refer to it later. The default value for `alias` is `default`.

```python
from elasticsearch.dsl import connections

connections.create_connection(alias='my_new_connection', hosts=['localhost'], timeout=60)
```

Additional keyword arguments (`hosts` and `timeout` in our example) will be passed to the `Elasticsearch` class from `elasticsearch-py`.

To see all possible configuration options refer to the [documentation](https://elasticsearch-py.readthedocs.io/en/latest/api/elasticsearch.html).



## Multiple clusters [_multiple_clusters]

You can define multiple connections to multiple clusters at the same time using the `configure` method:

```python
from elasticsearch.dsl import connections

connections.configure(
    default={'hosts': 'localhost'},
    dev={
        'hosts': ['esdev1.example.com:9200'],
        'sniff_on_start': True
    }
)
```

Such connections will be constructed lazily when requested for the first time.

You can alternatively define multiple connections by adding them one by one as shown in the following example:

```python
# if you have configuration options to be passed to Elasticsearch.__init__
# this also shows creating a connection with the alias 'qa'
connections.create_connection('qa', hosts=['esqa1.example.com'], sniff_on_start=True)

# if you already have an Elasticsearch instance ready
connections.add_connection('another_qa', my_client)
```

### Using aliases [_using_aliases]

When using multiple connections, you can refer to them using the string alias specified when you created the connection.

This example shows how to use an alias to a connection:

```python
s = Search(using='qa')
```

A `KeyError` will be raised if there is no connection registered with that alias.



## Manual [_manual]

If you don’t want to supply a global configuration, you can always pass in your own connection as an instance of `elasticsearch.Elasticsearch` with the parameter `using` wherever it is accepted like this:

```python
s = Search(using=Elasticsearch('localhost'))
```

You can even use this approach to override any connection the object might be already associated with:

```python
s = s.using(Elasticsearch('otherhost:9200'))
```

::::{note}
When using the `dsl` module, it is highly recommended that you use the built-in serializer (`elasticsearch.dsl.serializer.serializer`) to ensure your objects are correctly serialized into `JSON` every time. The `create_connection` method that is described here (and that the `configure` method uses under the hood) will do that automatically for you, unless you explicitly specify your own serializer. The built-in serializer also allows you to serialize your own objects - just define a `to_dict()` method on your objects and that method will be automatically called when serializing your custom objects to `JSON`.

::::




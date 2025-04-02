# Querying

The Python Elasticsearch client provides several ways to send queries to Elasticsearch. This document explains the details of how to construct and execute queries using the client. This document does not cover the DSL module.

## From API URLs to function calls

Elasticsearch APIs are grouped by namespaces.

 * There's the global namespace, with APIs like the Search API (`GET _search`) or the Index API (`PUT /<target>/_doc/<_id>` and related endpoints). 
 * Then there are all the other namespaces, such as:
   * Indices with APIs like the Create index API (`PUT /my-index`),
   * ES|QL with the Run an ES|QL query API (`POST /_async`),
   * and so on.

As a result, when you know which namespace and function you need, you can call the function. Assuming that `client` is an Elasticsearch instance, here is how you would call the examples from above:

* Global namespace: `client.search(...)` and `client.index(...)`
* Other namespaces:
  * Indices: `client.indices.create(...)`
  * ES|QL: `client.esql.query(...)`

How can you figure out the namespace?

* The [Elasticsearch API docs](https://www.elastic.co/docs/api/doc/elasticsearch/) can help, even though the tags it uses do not fully map to namespaces.
* You can also use the client documentation, by:
  * browsing the [Elasticsearch API Reference](https://elasticsearch-py.readthedocs.io/en/stable/api.html) page, or
  * searching for your endpoint using [Read the Docs](https://elasticsearch-py.readthedocs.io/) search, which is powered by Elasticsearch!
* Finally, for Elasticsearch 8.x, most examples in the [Elasticsearch guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html) are also available in Python. (This is still a work in progress for Elasticsearch 9.x.) In the example below, `client.ingest.put_pipeline(...)` is the function that calls the "Create or update a pipeline" API.


:::{image} ../images/python-example.png
:alt: Python code example in the Elasticsearch guide
:::
 
## Parameters

Now that you know which functions to call, the next step is parameters. To avoid ambiguity, the Python Elasticsearch client mandates keyword arguments. To give an example, let's look at the ["Create an index" API](https://elasticsearch-py.readthedocs.io/en/stable/api/indices.html#elasticsearch.client.IndicesClient.create). There's only one required parameter, `index`, so the minimal form looks like this:

```python
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200", api_key="...")

client.indices.create(index="my-index")
```

You can also use other parameters, including the first level of body parameters, such as:

```python
resp = client.indices.create(
    index="logs",
    aliases={"logs-alias": {}},
    mappings={"name": {"type": "text"}},
)
print(resp)
```

In this case, the client will send to Elasticsearch the following JSON body:

```console
PUT /logs
{
    "aliases": {"logs-alias": {}},
    "mappings": {"name": {"type": "text"}}
}
```

## Unknown parameters or APIs

Like other clients, the Python Elasticsearch client is generated from the [Elasticsearch specification](https://github.com/elastic/elasticsearch-specification). While we strive to keep it up to date, it is not (yet!) perfect, and sometimes body parameters are missing. In this case, you can specify the body directly, as follows:

```python
resp = client.indices.create(
    index="logs",
    body={
        "aliases": {"logs-alias": {}},
        "mappings": {"name": {"type": "text"}},
        "missing_parameter": "foo",
    }
)
print(resp)
```

In the event where an API is missing, you need to use the low-level `perform_request` function:

```python
resp = client.perform_request(
    "PUT",
    "/logs"
    index="logs",
    headers={"content-type": "application/json", "accept": "application/json"},
    body={
        "aliases": {"logs-alias": {}},
        "mappings": {"name": {"type": "text"}},
        "missing_parameter": "foo",
    }
)
print(resp)
```

One benefit of this function is that it lets you use arbitrary headers, such as the `es-security-runas-user` header used to [impersonate users](https://www.elastic.co/guide/en/elasticsearch/reference/current/run-as-privilege.html).


## Options

You can specify options such as request timeouts or retries using the `.options()` API, see the [Configuration](./configuration.md) page for details.
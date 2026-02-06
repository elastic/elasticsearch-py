# ES|QL query builder

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::

The ES|QL query builder allows you to construct ES|QL queries using Python syntax. Consider the following example:

```python
>>> from elasticsearch.esql import ESQL
>>> query = (
    ESQL.from_("employees")
    .sort("emp_no")
    .keep("first_name", "last_name", "height")
    .eval(height_feet="height * 3.281", height_cm="height * 100")
    .limit(3)
)
```

You can then see the assembled ES|QL query by printing the resulting query object:

```python
>>> print(query)
FROM employees
| SORT emp_no
| KEEP first_name, last_name, height
| EVAL height_feet = height * 3.281, height_cm = height * 100
| LIMIT 3
```

To execute this query, you can pass it to the `client.esql.query()` endpoint:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
>>> from elasticsearch import Elasticsearch
>>> client = Elasticsearch(hosts=[os.environ['ELASTICSEARCH_URL']])
>>> response = client.esql.query(query=query)
```
:::

:::{tab-item} Async Python
:sync: async
```python
>>> from elasticsearch import AsyncElasticsearch
>>> client = AsyncElasticsearch(hosts=[os.environ['ELASTICSEARCH_URL']])
>>> response = await client.esql.query(query=query)
```
:::

::::

The response body contains a `columns` attribute with the list of columns included in the results, and a `values` attribute with the list of results for the query, each given as a list of column values. Here is a possible response body returned by the example query given above:

```python
>>> from pprint import pprint
>>> pprint(response.body)
{'columns': [{'name': 'first_name', 'type': 'text'},
             {'name': 'last_name', 'type': 'text'},
             {'name': 'height', 'type': 'double'},
             {'name': 'height_feet', 'type': 'double'},
             {'name': 'height_cm', 'type': 'double'}],
 'is_partial': False,
 'took': 11,
 'values': [['Adrian', 'Wells', 2.424, 7.953144, 242.4],
            ['Aaron', 'Gonzalez', 1.584, 5.1971, 158.4],
            ['Miranda', 'Kramer', 1.55, 5.08555, 155]]}
```

## Creating an ES|QL query

To construct an ES|QL query you start from one of the ES|QL source commands:

### `ESQL.from_`

The `FROM` command selects the indices, data streams or aliases to be queried.

Examples:

```python
from elasticsearch.esql import ESQL

# FROM employees
query1 = ESQL.from_("employees")

# FROM <logs-{now/d}>
query2 = ESQL.from_("<logs-{now/d}>")

# FROM employees-00001, other-employees-*
query3 = ESQL.from_("employees-00001", "other-employees-*")

# FROM cluster_one:employees-00001, cluster_two:other-employees-*
query4 = ESQL.from_("cluster_one:employees-00001", "cluster_two:other-employees-*")

# FROM employees METADATA _id
query5 = ESQL.from_("employees").metadata("_id")
```

Note how in the last example the optional `METADATA` clause of the `FROM` command is added as a chained method.

### `ESQL.row`

The `ROW` command produces a row with one or more columns, with the values that you specify.

Examples:

```python
from elasticsearch.esql import ESQL, functions

# ROW a = 1, b = "two", c = null
query1 = ESQL.row(a=1, b="two", c=None)

# ROW a = [1, 2]
query2 = ESQL.row(a=[1, 2])

# ROW a = ROUND(1.23, 0)
query3 = ESQL.row(a=functions.round(1.23, 0))
```

### `ESQL.show`

The `SHOW` command returns information about the deployment and its capabilities.

Example:

```python
from elasticsearch.esql import ESQL

# SHOW INFO
query = ESQL.show("INFO")
```

## Adding processing commands

Once you have a query object, you can add one or more processing commands to it. The following
example shows how to create a query that uses the `WHERE` and `LIMIT` commands to filter the
results:

```python
from elasticsearch.esql import ESQL

# FROM employees
# | WHERE still_hired == true
# | LIMIT 10
query = ESQL.from_("employees").where("still_hired == true").limit(10)
```

For a complete list of available commands, review the methods of the [`ESQLBase` class](https://elasticsearch-py.readthedocs.io/en/stable/esql.html) in the Elasticsearch Python API documentation.

## Creating ES|QL Expressions and Conditions

The ES|QL query builder for Python provides two ways to create expressions and conditions in ES|QL queries.

The simplest option is to provide all ES|QL expressions and conditionals as strings. The following example uses this approach to add two calculated columns to the results using the `EVAL` command:

```python
from elasticsearch.esql import ESQL

# FROM employees
# | SORT emp_no
# | KEEP first_name, last_name, height
# | EVAL height_feet = height * 3.281, height_cm = height * 100
query = (
    ESQL.from_("employees")
    .sort("emp_no")
    .keep("first_name", "last_name", "height")
    .eval(height_feet="height * 3.281", height_cm="height * 100")
)
```

A more advanced alternative is to replace the strings with Python expressions, which are automatically translated to ES|QL when the query object is rendered to a string. The following example is functionally equivalent to the one above:

```python
from elasticsearch.esql import ESQL, E

# FROM employees
# | SORT emp_no
# | KEEP first_name, last_name, height
# | EVAL height_feet = height * 3.281, height_cm = height * 100
query = (
    ESQL.from_("employees")
    .sort("emp_no")
    .keep("first_name", "last_name", "height")
    .eval(height_feet=E("height") * 3.281, height_cm=E("height") * 100)
)
```

Here the `E()` helper function is used as a wrapper to the column name that initiates an ES|QL expression. The `E()` function transforms the given column into an ES|QL expression that can be modified with Python operators.

Here is a second example, which uses a conditional expression in the `WHERE` command:

```python
from elasticsearch.esql import ESQL

# FROM employees
# | KEEP first_name, last_name, height
# | WHERE first_name == "Larry"
query = (
    ESQL.from_("employees")
    .keep("first_name", "last_name", "height")
    .where('first_name == "Larry"')
)
```

Using Python syntax, the condition can be rewritten as follows:

```python
from elasticsearch.esql import ESQL, E

# FROM employees
# | KEEP first_name, last_name, height
# | WHERE first_name == "Larry"
query = (
    ESQL.from_("employees")
    .keep("first_name", "last_name", "height")
    .where(E("first_name") == "Larry")
)
```

### Preventing injection attacks

ES|QL, like most query languages, is vulnerable to [code injection attacks](https://en.wikipedia.org/wiki/Code_injection) if untrusted data provided by users is added to a query. To eliminate this risk, ES|QL allows untrusted data to be given separately from the query as parameters.

Continuing with the example above, let's assume that the application needs a `find_employee_by_name()` function that searches for the name given as an argument. If this argument is received by the application from users, then it is considered untrusted and should not be added to the query directly. Here is how to code the function in a secure manner:

::::{tab-set}
:group: sync_or_async

:::{tab-item} Standard Python
:sync: sync
```python
def find_employee_by_name(name):
    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "height")
        .where(E("first_name") == E("?"))
    )
    return client.esql.query(query=query, params=[name])
```
:::

:::{tab-item} Async Python
:sync: async
```python
async def find_employee_by_name(name):
    query = (
        ESQL.from_("employees")
        .keep("first_name", "last_name", "height")
        .where(E("first_name") == E("?"))
    )
    return await client.esql.query(query=query, params=[name])
```
:::

::::

Here the part of the query in which the untrusted data needs to be inserted is replaced with a parameter, which in ES|QL is defined by the question mark. When using Python expressions, the parameter must be given as `E("?")` so that it is treated as an expression and not as a literal string.

The list of values given in the `params` argument to the query endpoint are assigned in order to the parameters defined in the query.

## Using ES|QL functions

The ES|QL language includes a rich set of functions that can be used in expressions and conditionals. These can be included in expressions given as strings, as shown in the example below:

```python
from elasticsearch.esql import ESQL

# FROM employees
# | KEEP first_name, last_name, height
# | WHERE LENGTH(first_name) < 4"
query = (
    ESQL.from_("employees")
    .keep("first_name", "last_name", "height")
    .where("LENGTH(first_name) < 4")
)
```

All available ES|QL functions have Python wrappers in the `elasticsearch.esql.functions` module, which can be used when building expressions using Python syntax. Below is the example above coded using Python syntax:

```python
from elasticsearch.esql import ESQL, functions

# FROM employees
# | KEEP first_name, last_name, height
# | WHERE LENGTH(first_name) < 4"
query = (
    ESQL.from_("employees")
    .keep("first_name", "last_name", "height")
    .where(functions.length(E("first_name")) < 4)
)
```

Note that arguments passed to functions are assumed to be literals. When passing field names, parameters or other ES|QL expressions, it is necessary to wrap them with the `E()` helper function so that they are interpreted correctly.

You can find the complete list of available functions in the Python client's [ES|QL API reference documentation](https://elasticsearch-py.readthedocs.io/en/stable/esql.html#module-elasticsearch.esql.functions).

---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/integrations.html
---

# Integrations [integrations]

You can find integration options and information on this page.


## OpenTelemetry instrumentation [opentelemetry-intro]

The Python Elasticsearch client supports native OpenTelemetry instrumentation following the [OpenTelemetry Semantic Conventions for Elasticsearch](https://opentelemetry.io/docs/specs/semconv/database/elasticsearch/). Refer to the [Using OpenTelemetry](/reference/opentelemetry.md) page for details.


## ES|QL [esql-intro]

[ES|QL](docs-content://explore-analyze/query-filter/languages/esql.md) is available through the Python Elasticsearch client. Refer to the [ES|QL and Pandas](/reference/esql-pandas.md) page to learn more about using ES|QL and Pandas together with dataframes.


## Transport [transport]

The handling of connections, retries, and pooling is handled by the [Elastic Transport Python](https://github.com/elastic/elastic-transport-python) library. Documentation on the low-level classes is available on [Read the Docs](https://elastic-transport-python.readthedocs.io).


## Tracking requests with Opaque ID [opaque-id]

You can enrich your requests against Elasticsearch with an identifier string, that allows you to discover this identifier in [deprecation logs](docs-content://deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md#deprecation-logging), to support you with [identifying search slow log origin](elasticsearch://reference/elasticsearch/index-settings/slow-log.md) or to help with [identifying running tasks](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks).

The opaque ID can be set via the `opaque_id` parameter via the client `.options()` method:

```python
client = Elasticsearch(...)
client.options(opaque_id="request-id-...").search(...)
```


## Type Hints [type-hints]

Starting in `elasticsearch-py` v7.10.0 the library now ships with [type hints](https://www.python.org/dev/peps/pep-0484) and supports basic static type analysis with tools like [Mypy](http://mypy-lang.org) and [Pyright](https://github.com/microsoft/pyright).

If we write a script that has a type error like using `request_timeout` with a `str` argument instead of `float` and then run Mypy on the script:

```python
# script.py
from elasticsearch import Elasticsearch

client = Elasticsearch(...)
client.options(
    request_timeout="5"  # type error!
).search(...)

# $ mypy script.py
# script.py:5: error: Argument "request_timeout" to "search" of "Elasticsearch" has
#                     incompatible type "str"; expected "Union[int, float, None]"
# Found 1 error in 1 file (checked 1 source file)
```

Type hints also allow tools like your IDE to check types and provide better auto-complete functionality.




# Migrating from the `elasticsearch-dsl` package  [_migrating_from_elasticsearch_dsl_package]

In the past the Elasticsearch Python DSL module was distributed as a standalone package called `elasticsearch-dsl`. This package is now deprecated, since all its functionality has been integrated into the main Python client. We recommend all developers to migrate their applications and eliminate their dependency on the `elasticsearch-dsl` package.

To migrate your application, all references to `elasticsearch_dsl` as a top-level package must be changed to `elasticsearch.dsl`. In other words, the underscore from the package name should be replaced by a period.

Here are a few examples:

```python
# from:
from elasticsearch_dsl import Date, Document, InnerDoc, Text, connections
# to:
from elasticsearch.dsl import Date, Document, InnerDoc, Text, connections

# from:
from elasticsearch_dsl.query import MultiMatch
# to:
from elasticsearch.dsl.query import MultiMatch

# from:
import elasticsearch_dsl as dsl
# to:
from elasticsearch import dsl

# from:
import elasticsearch_dsl
# to:
from elasticsearch import dsl as elasticsearch_dsl

# from:
import elasticsearch_dsl
# to:
from elasticsearch import dsl
# and replace all references to "elasticsearch_dsl" in the code with "dsl"
```

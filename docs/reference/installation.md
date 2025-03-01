---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/installation.html
---

# Installation [installation]

[Download the latest version of Elasticsearch](https://www.elastic.co/downloads/elasticsearch) or [sign-up](https://cloud.elastic.co/registration?elektra=en-ess-sign-up-page) for a free trial of Elastic Cloud.

The Python client for {{es}} can be installed with pip:

```sh
$ python -m pip install elasticsearch
```

If your application uses async/await in Python you can install with the `async` extra:

```sh
$ python -m pip install elasticsearch[async]
```

Read more about [how to use asyncio with this project](https://elasticsearch-py.readthedocs.io/en/master/async.md).

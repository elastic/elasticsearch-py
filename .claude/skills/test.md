---
name: test
description: Write and run elasticsearch-py unit and integration tests.
---

# Test

Framework: pytest via nox. Tests live in `test_elasticsearch/`, not `tests/`. Sync tests are the source; async variants are generated.

```bash
nox -rs test
nox -rs lint
```

`nox -rs test` installs the package and runs pytest with coverage on `elasticsearch`. Integration tests need Elasticsearch and skip automatically when none is running. Do not fail a PR only because integration was skipped locally.

Do not add tests by editing `elasticsearch/_sync/client/` or `elasticsearch/_async/client/`. Test public client behavior from `test_elasticsearch/`. After changing sync DSL code, run `nox -rs format` so unasync and the DSL generator refresh async counterparts, then `nox -rs test`.

Optional extras (async, requests, orjson, pyarrow, vectorstore_mmr) have their own tests; a change that breaks the no-extras import is a lint failure.

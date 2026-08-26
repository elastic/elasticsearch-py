---
name: build-failure
description: Diagnose elasticsearch-py CI and local build failures.
---

# Build failure

Read the failing job log before changing code.

Edited generated client APIs: revert `elasticsearch/_sync/client/` and `elasticsearch/_async/client/`. Submit the change to `elastic/elasticsearch-specification`.

Async out of date with sync: `nox -rs format` (runs unasync and the DSL generator). `nox -rs lint` fails on `--check` if this was skipped.

black / isort / flake8: `nox -rs format`, then `nox -rs lint`. Do not reformat by hand or weaken lint.

Missing license headers: `nox -rs format` runs `utils/license-headers.py fix`.

Import fails without extras: the client must import with no optional deps. `nox -rs lint` checks `from elasticsearch import Elasticsearch` on a bare install.

Integration tests failed: they need Elasticsearch. Locally they skip if none is running. CI uses `.buildkite/run-elasticsearch.sh`.

Python version: 3.10 through 3.14. Do not use 3.9 APIs.

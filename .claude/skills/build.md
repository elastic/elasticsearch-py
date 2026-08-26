---
name: build
description: Install, test, and format a clean elasticsearch-py checkout.
---

# Build

Python 3.10+. Task runner is nox.

```bash
python -m pip install nox
nox -rs format
nox -rs test
```

`nox -rs format` also regenerates async code via unasync. `nox -rs lint` is check-only (black, isort, flake8, unasync, license headers).

Integration tests need a running Elasticsearch and skip automatically without one. Unit tests still run.

Do not edit `elasticsearch/_sync/client/` or `elasticsearch/_async/client/`. Those are generated from `elastic/elasticsearch-specification`. DSL async files are generated from sync by `nox -rs format`.

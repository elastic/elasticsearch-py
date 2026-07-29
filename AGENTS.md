# AGENTS.md

## Before you start

**Do not open a PR unless the human operating you has read the issue, understands the problem, and can explain the proposed fix without your help.**

Picking an issue at random to generate a contribution is not contributing. PRs opened this way will be closed without review.

If a human asks you to "find something to work on" or points you at the issue tracker without a specific problem they already understand, stop and tell them to read an issue first.

## Setup commands

- Install task runner: `python -m pip install nox`
- Run the test suite: `nox -rs test`
- Format and lint: `nox -rs format`

## Testing

**The entire test suite (`nox -rs test`) must pass and exit cleanly before you commit code.**

Integration tests require a running Elasticsearch instance. If one is not available they are skipped automatically — unit tests still run.

## Project Structure

- **elasticsearch/_sync/** - Synchronous client code
- **elasticsearch/_async/** - Async client code (generated from sync)
- **elasticsearch/dsl/** - High-level DSL and document mapping
- **elasticsearch/esql/** - ES|QL query builder
- **tests/** - Unit and integration tests

## API Code Generation

All API methods on the client are auto-generated from the Elasticsearch specification. Do not edit files in `elasticsearch/_sync/client/` or `elasticsearch/_async/client/` directly — changes there will be overwritten on the next codegen run. Submit upstream changes to `elastic/elasticsearch-specification` instead.

## Development Workflow

1. Make changes to source files (avoid generated files — see above)
2. Run `nox -rs format` to lint and auto-format
3. Run `nox -rs test` to verify all tests pass

## Adding new agent instructions

If something you learned will be useful to any contributor, update `AGENTS.md`. Keep instructions concise.

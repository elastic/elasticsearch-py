#!/usr/bin/env python
# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information


import json
import tempfile
import collections

import black
from click.testing import CliRunner
from jinja2 import Environment, FileSystemLoader
from pathlib import Path


code_root = Path(__file__).absolute().parent.parent
asciidocs_dir = code_root / "docs/examples"
flight_recorder_dir = code_root.parent / "clients-flight-recorder"
report_path = flight_recorder_dir / "recordings/docs/parsed-alternative-report.json"
substitutions = {"type": "doc_type", "from": "from_"}

jinja_env = Environment(
    loader=FileSystemLoader([code_root / "utils" / "templates"]),
    trim_blocks=True,
    lstrip_blocks=True,
)

files_to_generate = [
    "search/request-body.asciidoc",
    "mapping.asciidoc",
    "query-dsl.asciidoc",
    "query-dsl/query-string-query.asciidoc",
    "getting-started.asciidoc",
    "query-dsl/query_filter_context.asciidoc",
    "query-dsl/bool-query.asciidoc",
    "query-dsl/match-query.asciidoc",
    "indices/create-index.asciidoc",
    "docs/index_.asciidoc",
    "aggregations/bucket/terms-aggregation.asciidoc",
    "query-dsl/range-query.asciidoc",
    "/search/search.asciidoc",
    "query-dsl/multi-match-query.asciidoc",
    "docs/bulk.asciidoc",
    "indices/delete-index.asciidoc",
    "indices/put-mapping.asciidoc",
    "docs/reindex.asciidoc",
    "query-dsl/term-query.asciidoc",
    "indices/templates.asciidoc",
    "getting-started.asciidoc",
    "docs/update.asciidoc",
    "query-dsl/match-all-query.asciidoc",
    "docs/get.asciidoc",
    "query-dsl/wildcard-query.asciidoc",
    "query-dsl/exists-query.asciidoc",
    "docs/delete-by-query.asciidoc",
    "mapping/params/format.asciidoc",
    "mapping/types/nested.asciidoc",
    "query-dsl/terms-query.asciidoc",
    "search/request/sort.asciidoc",
    "mapping/types/date.asciidoc",
    "indices/update-settings.asciidoc",
    "indices/aliases.asciidoc",
    "setup/install/check-running.asciidoc",
    "query-dsl/regexp-query.asciidoc",
    "query-dsl/function-score-query.asciidoc",
    "search/request/from-size.asciidoc",
    "cluster/health.asciidoc",
    "query-dsl/nested-query.asciidoc",
    "mapping/types/array.asciidoc",
    "mapping/params/fielddata.asciidoc",
    "search/count.asciidoc",
    "mapping/types/keyword.asciidoc",
]


ParsedSource = collections.namedtuple("ParsedSource", ["api", "params", "body"])


def blacken(filename):
    runner = CliRunner()
    result = runner.invoke(
        black.main, [str(filename), "--line-length=75", "--target-version=py27"]
    )
    assert result.exit_code == 0, result.output


def main():
    for filepath in asciidocs_dir.iterdir():
        if filepath.name.endswith(".asciidoc"):
            filepath.unlink()

    if not flight_recorder_dir.exists() or not report_path.exists():
        raise RuntimeError(
            f"clients-flight-recorder repository not checked out at {flight_recorder_dir}"
        )

    with report_path.open() as f:
        report = json.loads(f.read())

    t = jinja_env.get_template("example")

    for exm in report:
        if exm["lang"] != "console":
            continue
        if exm["source_location"]["file"] not in files_to_generate:
            continue

        parsed_sources = []
        for src in exm["parsed_source"]:
            params = (src.get("params") or {}).copy()
            params.update(src.get("query") or {})
            parsed_sources.append(
                ParsedSource(
                    api=src["api"],
                    params={
                        substitutions.get(k, k): repr(v) for k, v in params.items()
                    },
                    body=src.get("body", None) or None,
                )
            )

        tmp_path = Path(tempfile.mktemp())
        with tmp_path.open(mode="w") as f:
            f.write(t.render(parsed_sources=parsed_sources))

        blacken(tmp_path)

        with tmp_path.open(mode="r") as f:
            data = f.read()
        data = data.rstrip().replace(",)", ")")
        tmp_path.unlink()

        with (asciidocs_dir / f"{exm['digest']}.asciidoc").open(mode="w") as f:
            f.truncate()
            f.write(
                f"""// {exm['source_location']['file']}:{exm['source_location']['line']}

[source, python]
----
{data}
----"""
            )


if __name__ == "__main__":
    main()

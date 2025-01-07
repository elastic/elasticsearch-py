#!/usr/bin/env python
#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import collections
import json
import os
import tempfile
from pathlib import Path

import black
from click.testing import CliRunner
from jinja2 import Environment, FileSystemLoader

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
    "search/search.asciidoc",
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
    "docs/update-by-query.asciidoc",
    "search/suggesters.asciidoc",
    "api-conventions.asciidoc",
    "cat/indices.asciidoc",
    "query-dsl/match-phrase-query.asciidoc",
    "indices/get-index.asciidoc",
    "setup/logging-config.asciidoc",
    "docs/delete.asciidoc",
    "aggregations/metrics/valuecount-aggregation.asciidoc",
    "indices/get-mapping.asciidoc",
    "aggregations/bucket/filter-aggregation.asciidoc",
    "aggregations/bucket/datehistogram-aggregation.asciidoc",
    "mapping/types/numeric.asciidoc",
    "search/request/scroll.asciidoc",
    "mapping/fields/id-field.asciidoc",
    "search.asciidoc",
    "mapping/params/multi-fields.asciidoc",
    "cluster/allocation-explain.asciidoc",
    "cluster/get-settings.asciidoc",
    "cluster/update-settings.asciidoc",
    "health/health.asciidoc",
    "cluster/reroute.asciidoc",
    "inference/get-inference.asciidoc",
    "inference/delete-inference.asciidoc",
    "inference/post-inference.asciidoc",
    "inference/put-inference.asciidoc",
    "ml/trained-models/apis/clear-trained-model-deployment-cache.asciidoc",
    "ml/trained-models/apis/delete-trained-models-aliases.asciidoc",
    "ml/trained-models/apis/delete-trained-models.asciidoc",
    "ml/trained-models/apis/get-trained-models-stats.asciidoc",
    "ml/trained-models/apis/get-trained-models.asciidoc",
    "ml/trained-models/apis/infer-trained-model-deployment.asciidoc",
    "ml/trained-models/apis/infer-trained-model.asciidoc",
    "ml/trained-models/apis/put-trained-model-definition-part.asciidoc",
    "ml/trained-models/apis/put-trained-model-vocabulary.asciidoc",
    "ml/trained-models/apis/put-trained-models-aliases.asciidoc",
    "ml/trained-models/apis/put-trained-models.asciidoc",
    "ml/trained-models/apis/start-trained-model-deployment.asciidoc",
    "ml/trained-models/apis/stop-trained-model-deployment.asciidoc",
    "ml/trained-models/apis/update-trained-model-deployment.asciidoc",
    "setup/run-elasticsearch-locally.asciidoc",
    "setup/important-settings.asciidoc",
    "setup/secure-settings.asciidoc",
    "modules/cluster.asciidoc",
    "modules/cluster/misc.asciidoc",
    "modules/network.asciidoc",
    "modules/indices/request_cache.asciidoc",
    "setup/advanced-configuration.asciidoc",
    "setup/sysconfig/swap.asciidoc",
    "setup/sysconfig/file-descriptors.asciidoc",
    "modules/discovery/voting.asciidoc",
    "setup/add-nodes.asciidoc",
    "setup/restart-cluster.asciidoc",
    "modules/cluster/remote-clusters-api-key.asciidoc",
    "modules/cluster/remote-clusters-cert.asciidoc",
    "modules/discovery/voting.asciidoc",
    "modules/cluster/remote-clusters-migration.asciidoc",
    "modules/cluster/remote-clusters-troubleshooting.asciidoc",
    "upgrade/archived-settings.asciidoc",
    "index-modules/allocation/filtering.asciidoc",
    "index-modules/allocation/delayed.asciidoc",
    "index-modules/allocation/prioritization.asciidoc",
    "index-modules/allocation/total_shards.asciidoc",
    "index-modules/allocation/data_tier_allocation.asciidoc",
    "index-modules/blocks.asciidoc",
    "index-modules/similarity.asciidoc",
    "index-modules/slowlog.asciidoc",
    "index-modules/store.asciidoc",
    "index-modules/index-sorting.asciidoc",
    "index-modules/indexing-pressure.asciidoc",
    "mapping/dynamic-mapping.asciidoc",
    "mapping/dynamic/field-mapping.asciidoc",
    "mapping/dynamic/templates.asciidoc",
    "mapping/explicit-mapping.asciidoc",
    "mapping/runtime.asciidoc",
    "mapping/runtime.asciidoc",
    "mapping/types.asciidoc",
    "mapping/types/aggregate-metric-double.asciidoc",
    "mapping/types/alias.asciidoc",
    "mapping/types/array.asciidoc",
    "mapping/types/binary.asciidoc",
    "mapping/types/boolean.asciidoc",
    "mapping/types/completion.asciidoc",
    "mapping/types/date_nanos.asciidoc",
    "mapping/types/dense-vector.asciidoc",
    "mapping/types/flattened.asciidoc",
    "mapping/types/geo-point.asciidoc",
    "mapping/types/geo-shape.asciidoc",
    "mapping/types/histogram.asciidoc",
    "mapping/types/ip.asciidoc",
    "mapping/types/parent-join.asciidoc",
    "mapping/types/object.asciidoc",
    "mapping/types/percolator.asciidoc",
    "mapping/types/point.asciidoc",
    "mapping/types/range.asciidoc",
    "mapping/types/rank-feature.asciidoc",
    "mapping/types/rank-features.asciidoc",
    "mapping/types/search-as-you-type.asciidoc",
    "mapping/types/semantic-text.asciidoc",
    "mapping/types/shape.asciidoc",
    "mapping/types/sparse-vector.asciidoc",
    "mapping/types/text.asciidoc",
    "mapping/types/token-count.asciidoc",
    "mapping/types/unsigned_long.asciidoc",
    "mapping/types/version.asciidoc",
]


ParsedSource = collections.namedtuple("ParsedSource", ["api", "params", "body"])


def blacken(filename):
    runner = CliRunner()
    result = runner.invoke(
        black.main, [str(filename), "--line-length=75", "--target-version=py37"]
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
            params = {
                k: (list(v.split(",")) if isinstance(v, str) and "," in v else v)
                for k, v in params.items()
            }

            parsed_sources.append(
                ParsedSource(
                    api=src["api"],
                    params={
                        substitutions.get(k, k): repr(v) for k, v in params.items()
                    },
                    body=src.get("body", None) or None,
                )
            )

        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp_file:
            tmp_file.write(t.render(parsed_sources=parsed_sources))

        try:
            blacken(tmp_file.name)
        except AssertionError:
            loc = exm["source_location"]
            print(f"Failed to format {loc['file']}:{loc['line']}, skipping.")
            continue

        with open(tmp_file.name) as f:
            data = f.read()
            data = data.rstrip().replace(",)", ")")

        os.unlink(tmp_file.name)

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

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

from __future__ import print_function

import atexit
import sys
from os import environ
from os.path import dirname, join, pardir, abspath, exists
import subprocess


def fetch_es_repo():
    # user is manually setting YAML dir, don't tamper with it
    if "TEST_ES_YAML_DIR" in environ:
        return

    repo_path = environ.get(
        "TEST_ES_REPO",
        abspath(join(dirname(__file__), pardir, pardir, "elasticsearch")),
    )

    # no repo
    if not exists(repo_path) or not exists(join(repo_path, ".git")):
        subprocess.check_call(
            "git clone https://github.com/elastic/elasticsearch %s" % repo_path,
            shell=True,
        )

    # set YAML test dir
    environ["TEST_ES_YAML_DIR"] = join(
        repo_path, "rest-api-spec", "src", "main", "resources", "rest-api-spec", "test"
    )

    # fetching of yaml tests disabled, we'll run with what's there
    if environ.get("TEST_ES_NOFETCH", False):
        return

    from test_elasticsearch.test_server import get_client
    from test_elasticsearch.test_cases import SkipTest

    # find out the sha of the running es
    try:
        es = get_client()
        sha = es.info()["version"]["build_hash"]
    except (SkipTest, KeyError):
        print("No running elasticsearch >1.X server...")
        return

    # fetch new commits to be sure...
    print("Fetching elasticsearch repo...")
    subprocess.check_call(
        "cd %s && git fetch https://github.com/elastic/elasticsearch.git" % repo_path,
        shell=True,
    )
    # reset to the version fron info()
    subprocess.check_call("cd %s && git fetch" % repo_path, shell=True)
    subprocess.check_call("cd %s && git reset --hard %s" % (repo_path, sha), shell=True)


def run_all(argv=None):
    atexit.register(lambda: sys.stderr.write("Shutting down....\n"))

    # fetch yaml tests anywhere that's not GitHub Actions
    if "GITHUB_ACTION" not in environ:
        fetch_es_repo()

    # always insert coverage when running tests
    if argv is None:
        junit_xml = join(
            abspath(dirname(dirname(__file__))), "junit", "elasticsearch-py-junit.xml"
        )
        argv = [
            "pytest",
            "--cov=elasticsearch",
            "--junitxml=%s" % junit_xml,
            "--log-level=DEBUG",
            "--cache-clear",
            "-vv",
        ]

        ignores = []
        # Python 3.6+ is required for async
        if sys.version_info < (3, 6):
            ignores.append("test_elasticsearch/test_async/")

        # GitHub Actions, run non-server tests
        if "GITHUB_ACTION" in environ:
            ignores.extend(
                [
                    "test_elasticsearch/test_server/",
                    "test_elasticsearch/test_async/test_server/",
                ]
            )
        if ignores:
            argv.extend(["--ignore=%s" % ignore for ignore in ignores])

        # Jenkins, only run server tests
        if environ.get("TEST_TYPE") == "server":
            test_dir = abspath(dirname(__file__))
            argv.append(join(test_dir, "test_server"))
            if sys.version_info >= (3, 6):
                argv.append(join(test_dir, "test_async/test_server"))

        # Not in CI, run all tests specified.
        else:
            argv.append(abspath(dirname(__file__)))

    exit_code = 0
    try:
        subprocess.check_call(argv, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        exit_code = e.returncode
    sys.exit(exit_code)


if __name__ == "__main__":
    run_all(sys.argv)

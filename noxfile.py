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

import nox

SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "elasticsearch/",
    "test_elasticsearch/",
    "utils/",
)


@nox.session(python=["3.10", "3.11", "3.12", "3.13", "3.14"])
def test(session):
    session.install(".")
    session.install("-r", "dev-requirements.txt")

    session.run("pytest", "-v", "--cov=elasticsearch", "--cov-report=term-missing")


@nox.session()
def format(session):
    session.install("black>=23.0", "isort")

    session.run("isort", "--profile=black", *SOURCE_FILES)
    session.run("black", "--target-version=py310", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session()
def lint(session):
    session.install("flake8", "black>=23.0", "mypy>=1.0", "isort", "types-requests")

    session.run("isort", "--check", "--profile=black", *SOURCE_FILES)
    session.run("black", "--target-version=py310", "--check", *SOURCE_FILES)
    session.run("flake8", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "check", *SOURCE_FILES)

    session.run("python", "-m", "pip", "install", "aiohttp")

    session.run("mypy", "--strict", "elasticsearch/")
    session.run("mypy", "--strict", "test_elasticsearch/test_types/sync_types.py")
    session.run("mypy", "--strict", "test_elasticsearch/test_types/async_types.py")

    session.run("python", "-m", "pip", "uninstall", "--yes", "aiohttp")
    session.run("mypy", "--strict", "elasticsearch/")
    session.run("mypy", "--strict", "test_elasticsearch/test_types/sync_types.py")


@nox.session()
def docs(session):
    session.install(".")
    session.install(
        "-rdev-requirements.txt", "sphinx-rtd-theme", "sphinx-autodoc-typehints>=1.20.0"
    )
    session.run("sphinx-build", "docs/sphinx/", "docs/sphinx/_build", "-b", "html")

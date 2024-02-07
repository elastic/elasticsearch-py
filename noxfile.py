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

import os

import nox

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FILES = (
    "docs/sphinx/conf.py",
    "setup.py",
    "noxfile.py",
    "elasticsearch/",
    "test_elasticsearch/",
    "utils/",
)
# Allow building aiohttp when no wheels are available (eg. for recent Python versions)
INSTALL_ENV = {"AIOHTTP_NO_EXTENSIONS": "1"}


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"])
def test(session):
    session.install(".[async,requests]", env=INSTALL_ENV, silent=False)
    session.install("-r", "dev-requirements.txt", silent=False)

    junit_xml = os.path.join(SOURCE_DIR, "junit", "elasticsearch-py-junit.xml")
    pytest_argv = [
        "pytest",
        "--cov-report=term-missing",
        "--cov=elasticsearch",
        "--cov-config=setup.cfg",
        f"--junitxml={junit_xml}",
        "--log-level=DEBUG",
        "--cache-clear",
        "-vv",
    ]
    session.run(*pytest_argv)


@nox.session()
def format(session):
    session.install("black~=24.0", "isort", "flynt", "unasync", "setuptools")

    session.run("python", "utils/run-unasync.py")
    session.run("isort", "--profile=black", *SOURCE_FILES)
    session.run("flynt", *SOURCE_FILES)
    session.run("black", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session()
def lint(session):
    session.install("flake8", "black~=24.0", "mypy", "isort", "types-requests")

    session.run("isort", "--check", "--profile=black", *SOURCE_FILES)
    session.run("black", "--check", *SOURCE_FILES)
    session.run("flake8", *SOURCE_FILES)
    session.run("python", "utils/license-headers.py", "check", *SOURCE_FILES)

    # Workaround to make '-r' to still work despite uninstalling aiohttp below.
    session.install(".[async,requests]", env=INSTALL_ENV)

    # Run mypy on the package and then the type examples separately for
    # the two different mypy use-cases, ourselves and our users.
    session.run("mypy", "--strict", "--show-error-codes", "elasticsearch/")
    session.run(
        "mypy",
        "--strict",
        "--show-error-codes",
        "test_elasticsearch/test_types/sync_types.py",
    )
    session.run(
        "mypy",
        "--strict",
        "--show-error-codes",
        "test_elasticsearch/test_types/async_types.py",
    )

    # Make sure we don't require aiohttp to be installed for users to
    # receive type hint information from mypy.
    session.run("python", "-m", "pip", "uninstall", "--yes", "aiohttp")
    session.run("mypy", "--strict", "--show-error-codes", "elasticsearch/")
    session.run(
        "mypy",
        "--strict",
        "--show-error-codes",
        "test_elasticsearch/test_types/sync_types.py",
    )


@nox.session()
def docs(session):
    session.install("-rdev-requirements.txt")
    session.install(".")
    session.run("python", "-m", "pip", "install", "sphinx-autodoc-typehints")

    session.run("sphinx-build", "docs/sphinx/", "docs/sphinx/_build", "-b", "html")

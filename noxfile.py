# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

import nox


SOURCE_FILES = (
    "setup.py",
    "noxfile.py",
    "elasticsearch/",
    "test_elasticsearch/",
    "utils/",
)


@nox.session(python=["2.7", "3.4", "3.5", "3.6", "3.7", "3.8"])
def test(session):
    session.install(".")
    session.install("-r", "dev-requirements.txt")

    session.run("python", "setup.py", "test")


@nox.session()
def blacken(session):
    session.install("black")

    session.run("black", "--target-version=py27", *SOURCE_FILES)
    session.run("python", "utils/license_headers.py", "fix", *SOURCE_FILES)

    lint(session)


@nox.session()
def lint(session):
    session.install("flake8", "black")

    session.run("black", "--target-version=py27", "--check", *SOURCE_FILES)
    session.run("flake8", *SOURCE_FILES)
    session.run("python", "utils/license_headers.py", "check", *SOURCE_FILES)


@nox.session()
def docs(session):
    session.install(".")
    session.install("-rdev-requirements.txt", "sphinx-rtd-theme")

    session.run("sphinx-build", "docs/", "docs/_build", "-b", "html")

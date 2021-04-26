# -*- coding: utf-8 -*-
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

import re
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

package_name = "elasticsearch"
base_dir = abspath(dirname(__file__))

with open(join(base_dir, package_name, "_version.py")) as f:
    package_version = re.search(
        r"__versionstr__\s+=\s+[\"\']([^\"\']+)[\"\']", f.read()
    ).group(1)

with open(join(base_dir, "README.rst")) as f:
    long_description = f.read().strip()

packages = [
    package
    for package in find_packages(where=".", exclude=("test_elasticsearch*",))
    if package == package_name or package.startswith(package_name + ".")
]

install_requires = [
    "urllib3>=1.21.1, <2",
    "certifi",
]
tests_require = [
    "requests>=2.0.0, <3.0.0",
    "coverage",
    "mock",
    "pyyaml",
    "pytest",
    "pytest-cov",
]
async_require = ["aiohttp>=3,<4"]

docs_require = ["sphinx<1.7", "sphinx_rtd_theme"]
generate_require = ["black", "jinja2"]

setup(
    name=package_name,
    description="Python client for Elasticsearch",
    license="Apache-2.0",
    url="https://github.com/elastic/elasticsearch-py",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    version=package_version,
    author="Honza Král, Nick Lang",
    author_email="honza.kral@gmail.com, nick@nicklang.com",
    maintainer="Seth Michael Larson",
    maintainer_email="seth.larson@elastic.co",
    project_urls={
        "Documentation": "https://elasticsearch-py.readthedocs.io",
        "Source Code": "https://github.com/elastic/elasticsearch-py",
        "Issue Tracker": "https://github.com/elastic/elasticsearch-py/issues",
    },
    packages=packages,
    package_data={"elasticsearch": ["py.typed", "*.pyi"]},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    install_requires=install_requires,
    test_suite="test_elasticsearch.run_tests.run_all",
    tests_require=tests_require,
    extras_require={
        "develop": tests_require + docs_require + generate_require,
        "docs": docs_require,
        "requests": ["requests>=2.4.0, <3.0.0"],
        "async": async_require,
    },
)

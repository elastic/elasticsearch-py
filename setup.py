# -*- coding: utf-8 -*-
# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

from os.path import join, dirname
from setuptools import setup, find_packages

VERSION = (8, 0, 0)
__version__ = VERSION
__versionstr__ = ".".join(map(str, VERSION))

with open(join(dirname(__file__), "README")) as f:
    long_description = f.read().strip()

install_requires = [
    "urllib3>=1.21.1",
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
async_require = ["aiohttp>=3,<4", "yarl"]

docs_require = ["sphinx<1.7", "sphinx_rtd_theme"]
generate_require = ["black", "jinja2"]

setup(
    name="elasticsearch",
    description="Python client for Elasticsearch",
    license="Apache-2.0",
    url="https://github.com/elastic/elasticsearch-py",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    version=__versionstr__,
    author="Honza Král, Nick Lang",
    author_email="honza.kral@gmail.com, nick@nicklang.com",
    maintainer="Seth Michael Larson",
    maintainer_email="seth.larson@elastic.co",
    packages=find_packages(where=".", exclude=("test_elasticsearch*",)),
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

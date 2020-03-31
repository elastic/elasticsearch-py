# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup, find_packages
import sys

VERSION = (6, 8, 1)
__version__ = VERSION
__versionstr__ = ".".join(map(str, VERSION))

f = open(join(dirname(__file__), "README"))
long_description = f.read().strip()
f.close()

install_requires = ["urllib3>=1.21.1"]
tests_require = [
    "requests>=2.0.0, <3.0.0",
    "nose",
    "coverage",
    "mock",
    "pyyaml",
    "nosexcover",
    "numpy",
    "pandas",
]

# use external unittest for 2.6
if sys.version_info[:2] == (2, 6):
    install_requires.append("unittest2")

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
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4",
    install_requires=install_requires,
    test_suite="test_elasticsearch.run_tests.run_all",
    tests_require=tests_require,
    extras_require={
        "develop": tests_require + ["sphinx<1.7", "sphinx_rtd_theme"],
        "requests": ["requests>=2.4.0, <3.0.0"],
    },
)

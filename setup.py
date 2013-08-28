# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup
import sys



VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

f = open(join(dirname(__file__), 'README.rst'))
long_description = f.read().strip()
f.close()

install_requires = [
    'requests',
    'urllib3',
]
tests_require = [
    'nose',
    'coverage',
    'mock',
]

# use external unittest for 2.6
if sys.version_info[:2] == (2, 6):
    tests_require.append('unittest2')

setup(
    name = 'elasticsearch',
    description = "Python client for Elasticsearch",
    license="Apache License, Version 2.0",
    url = "https://github.com/elasticsearch/elasticsearch-py",
    long_description = long_description,
    version = __versionstr__,
    author = "Honza Král",
    author_email = "honza.kral@gmail.com",
    packages = ['elasticsearch'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=install_requires,

    test_suite='test_elasticsearch.run_tests.run_all',
    tests_require=tests_require,
)

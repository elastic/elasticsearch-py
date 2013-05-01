# -*- coding: utf-8 -*-
from os.path import join, dirname
from setuptools import setup


VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

f = open(join(dirname(__file__), 'README.rst'))
long_description = f.read().strip()
f.close()

install_requires = [
]
test_requires = [
    'nose',
    'coverage',
]

setup(
    name = 'elasticsearch',
    description = "Python client for Elasticsearch",
    url = "https://github.com/elasticsearch/elasticsearch/",
    long_description = long_description,
    version = __versionstr__,
    author = "Honza Král",
    author_email = "honza.kral@gmail.com",
    packages = ['elasticsearch'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,

    test_suite='test_elasticsearch.run_tests.run_all',
    test_requires=test_requires,
)

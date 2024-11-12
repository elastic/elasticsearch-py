<p align="center">
    <img src="https://github.com/elastic/elasticsearch-py/raw/main/docs/logo-elastic-glyph-color.svg" width="20%" alt="Elastic logo" />
</p>

# Elasticsearch Python Client

<p align="center">
  <a href="https://pypi.org/project/elasticsearch"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/elasticsearch" /></a>
  <a href="https://pypi.org/project/elasticsearch"><img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/elasticsearch" /></a>
  <a href="https://anaconda.org/conda-forge/elasticsearch"><img alt="Conda Version" src="https://img.shields.io/conda/vn/conda-forge/elasticsearch" /></a>
  <a href="https://pepy.tech/project/elasticsearch?versions=*"><img alt="Downloads" src="https://static.pepy.tech/badge/elasticsearch" /></a>
<br/>
  <a href="https://github.com/elastic/elasticsearch-py/actions/workflows/ci.yml?query=workflow%3ACI"><img alt="Build Status on GitHub" src="https://github.com/elastic/elasticsearch-py/workflows/CI/badge.svg" /></a>
  <a href="https://buildkite.com/elastic/elasticsearch-py-integration-tests"><img alt="Buildkite Status on Buildkite" src="https://badge.buildkite.com/68e22afcb2ea8f6dcc20834e3a5b5ab4431beee33d3bd751f3.svg" /></a>
  <a href="https://elasticsearch-py.readthedocs.io"><img alt="Documentation Status" src="https://readthedocs.org/projects/elasticsearch-py/badge/?version=latest" /></a><br>
</p>

*The official Python client for Elasticsearch.*


## Features

* Translating basic Python data types to and from JSON
* Configurable automatic discovery of cluster nodes
* Persistent connections
* Load balancing (with pluggable selection strategy) across available nodes
* Failed connection penalization (time based - failed connections won't be
  retried until a timeout is reached)
* Support for TLS and HTTP authentication
* Thread safety across requests
* Pluggable architecture
* Helper functions for idiomatically using APIs together


## Installation

[Download the latest version of Elasticsearch](https://www.elastic.co/downloads/elasticsearch)
or
[sign-up](https://cloud.elastic.co/registration?elektra=en-ess-sign-up-page)
for a free trial of Elastic Cloud.

Refer to the [Installation section](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_installation) 
of the getting started documentation.


## Connecting

Refer to the [Connecting section](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_connecting)
of the getting started documentation.


## Usage
-----

* [Creating an index](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_creating_an_index)
* [Indexing a document](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_indexing_documents)
* [Getting documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_getting_documents)
* [Searching documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_searching_documents)
* [Updating documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_updating_documents)
* [Deleting documents](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_deleting_documents)
* [Deleting an index](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html#_deleting_an_index)


## Compatibility

Language clients are forward compatible; meaning that the clients support
communicating with greater or equal minor versions of Elasticsearch without
breaking. It does not mean that the clients automatically support new features
of newer Elasticsearch versions; it is only possible after a release of a new
client version. For example, a 8.12 client version won't automatically support
the new features of the 8.13 version of Elasticsearch, the 8.13 client version
is required for that. Elasticsearch language clients are only backwards
compatible with default distributions and without guarantees made.

| Elasticsearch Version | Elasticsearch-Python Branch | Supported |
| --------------------- | ------------------------ | --------- |
| main                  | main                     |           |
| 8.x                   | 8.x                      | 8.x       |
| 7.x                   | 7.x                      | 7.17      |


If you have a need to have multiple versions installed at the same time older
versions are also released as ``elasticsearch7`` and ``elasticsearch8``.


## Documentation

Documentation for the client is [available on elastic.co] and [Read the Docs].

[available on elastic.co]: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
[Read the Docs]: https://elasticsearch-py.readthedocs.io


## License

This software is licensed under the [Apache License 2.0](./LICENSE). See [NOTICE](./NOTICE).

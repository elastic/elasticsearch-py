#!/bin/bash

# Start elasticsearch in a docker container

ES_VERSION=${ES_VERSION:-"7.0.0-beta1"}
ES_TEST_SERVER=${ES_TEST_SERVER:-"http://localhost:9200"}

SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

exec docker run -d \
    -e path.repo=/tmp \
    -e "repositories.url.allowed_urls=http://*" \
    -e node.attr.testattr=test \
    -e node.name=test \
    -e ES_HOST=$ES_TEST_SERVER \
    -e cluster.initial_master_nodes=test \
    -v $SOURCE_DIR/../elasticsearch:/code/elasticsearch \
    -v /tmp:/tmp \
    -p "9200:9200" \
docker.elastic.co/elasticsearch/elasticsearch-oss:$ES_VERSION

#!/bin/bash

# Start elasticsearch in a docker container

ES_VERSION=${ES_VERSION:-"latest"}
ES_TEST_SERVER=${ES_TEST_SERVER:-"http://localhost:9200"}

exec docker run -d \
    -e path.repo=/tmp \
    -e "repositories.url.allowed_urls=http://*" \
    -e node.attr.testattr=test \
    -e ES_HOST=$ES_TEST_SERVER \
    -v `pwd`/../elasticsearch:/code/elasticsearch \
    -v /tmp:/tmp \
    -p "9200:9200" \
docker.elastic.co/elasticsearch/elasticsearch-oss:$ES_VERSION

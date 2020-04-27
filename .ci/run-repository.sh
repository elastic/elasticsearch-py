#!/usr/bin/env bash

# Called by entry point `run-test` use this script to add your repository specific test commands
# Once called Elasticsearch is up and running and the following parameters are available to this script

# ELASTICSEARCH_VERSION -- version e.g Major.Minor.Patch(-Prelease)
# ELASTICSEARCH_CONTAINER -- the docker moniker as a reference to know which docker image distribution is used
# ELASTICSEARCH_URL -- The url at which elasticsearch is reachable
# NETWORK_NAME -- The docker network name
# NODE_NAME -- The docker container name also used as Elasticsearch node name

# When run in CI the test-matrix is used to define additional variables
# TEST_SUITE -- either `oss` or `xpack`, defaults to `oss` in `run-tests`

set -e

echo -e "\033[34;1mINFO:\033[0m URL ${ELASTICSEARCH_URL}\033[0m"
echo -e "\033[34;1mINFO:\033[0m VERSION ${ELASTICSEARCH_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m CONTAINER ${ELASTICSEARCH_CONTAINER}\033[0m"
echo -e "\033[34;1mINFO:\033[0m TEST_SUITE ${TEST_SUITE}\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_VERSION ${PYTHON_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_CONNECTION_CLASS ${PYTHON_CONNECTION_CLASS}\033[0m"

echo -e "\033[1m>>>>> Build [elastic/elasticsearch-py container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

docker build \
       --file .ci/Dockerfile \
       --tag elastic/elasticsearch-py \
       --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
       .

echo -e "\033[1m>>>>> Run [elastic/elasticsearch-py container] >>>>>>>>>>>>>>>>>>>>>>>>>>>>>\033[0m"

mkdir -p junit
docker run \
  --network=${NETWORK_NAME} \
  --env "ELASTICSEARCH_HOST=${ELASTICSEARCH_URL}" \
  --env "TEST_SUITE=${TEST_SUITE}" \
  --env "PYTHON_CONNECTION_CLASS=${PYTHON_CONNECTION_CLASS}" \
  --name elasticsearch-py \
  --rm \
  --volume `pwd`:/code/elasticsearch-py \
  elastic/elasticsearch-py \
  python setup.py test

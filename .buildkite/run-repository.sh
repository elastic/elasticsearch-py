#!/usr/bin/env bash

# Called by entry point `run-test` use this script to add your repository specific test commands
# Once called Elasticsearch is up and running and the following parameters are available to this script

# STACK_VERSION -- version e.g Major.Minor.Patch(-Prelease)
# elasticsearch_container -- the docker moniker as a reference to know which docker image distribution is used
# elasticsearch_url -- The url at which elasticsearch is reachable
# network_name -- The docker network name
# node_name -- The docker container name also used as Elasticsearch node name

# When run in CI the test-matrix is used to define additional variables
# TEST_SUITE -- either `oss` or `xpack`, defaults to `oss` in `run-tests`

set -e

echo -e "\033[34;1mINFO:\033[0m URL $elasticsearch_url\033[0m"
echo -e "\033[34;1mINFO:\033[0m VERSION $STACK_VERSION\033[0m"
echo -e "\033[34;1mINFO:\033[0m CONTAINER $elasticsearch_container\033[0m"
echo -e "\033[34;1mINFO:\033[0m TEST_SUITE $TEST_SUITE\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_VERSION $PYTHON_VERSION\033[0m"
echo -e "\033[34;1mINFO:\033[0m PYTHON_CONNECTION_CLASS $PYTHON_CONNECTION_CLASS\033[0m"

echo "--- :docker: :python: Build elastic/elasticsearch-py container"

docker build \
       --file .buildkite/Dockerfile \
       --tag elastic/elasticsearch-py \
       --build-arg "PYTHON_VERSION=$PYTHON_VERSION" \
       --build-arg "BUILDER_UID=$(id -u)" \
       --build-arg "BUILDER_GID=$(id -g)" \
       .

echo "--- :docker: :python: Run elastic/elasticsearch-py container"

mkdir -p "$(pwd)/junit"
docker run \
  -u "$(id -u):$(id -g)" \
  --network="$network_name" \
  -e STACK_VERSION \
  -e "ELASTICSEARCH_URL=$elasticsearch_url" \
  -e TEST_SUITE \
  -e PYTHON_CONNECTION_CLASS \
  -v "$(pwd)/junit:/junit" \
  --name elasticsearch-py \
  --rm \
  elastic/elasticsearch-py \

  bash -c "nox -s test-$PYTHON_VERSION; [ -f ./junit/$BUILDKITE_JOB_ID-junit.xml ] && mv ./junit/$BUILDKITE_JOB_ID-junit.xml /junit || echo 'No JUnit artifact found'"

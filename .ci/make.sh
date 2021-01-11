#!/bin/bash

set -eo pipefail

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="$( dirname "$BASE_DIR" )"

if [[ "$1" == "assemble" ]]; then
  mkdir -p $BASE_DIR/.ci/output
  docker build . --tag elastic/elasticsearch-py -f .ci/Dockerfile
  docker run --rm -v $BASE_DIR/.ci/output:/code/elasticsearch-py/dist \
    elastic/elasticsearch-py \
    python /code/elasticsearch-py/utils/build-dists.py $2
  cd ./.ci/output && tar -czvf elasticsearch-py-$2.tar.gz * && cd -
  exit 0
fi

echo "Must be called with '.ci/make.sh [command]"
exit 1

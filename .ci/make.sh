#!/bin/bash

set -eo pipefail

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="$( dirname "$BASE_DIR" )"

if [[ "$1" == "release" ]]; then
  python $BASE_DIR/utils/build-dists.py $2
  mkdir -p $BASE_DIR/.ci/output
  cp $BASE_DIR/dist/* $BASE_DIR/.ci/output/
  exit 0
fi

echo "Must be called with '.ci/make.sh [command]"
exit 1

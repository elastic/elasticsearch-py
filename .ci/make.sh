#!/bin/bash

set -eo pipefail

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="$( dirname "$BASE_DIR" )"

if [[ "$1" != "release" ]]; then
  echo "Must be called ./.ci/make.sh release [version]"
  exit 1
fi

python $BASE_DIR/utils/build_dists.py
mkdir -p $BASE_DIR/.ci/output
cp $BASE_DIR/dist/* $BASE_DIR/.ci/output/

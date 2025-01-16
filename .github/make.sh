#!/usr/bin/env bash

# ------------------------------------------------------- #
#
# Skeleton for common build entry script for all elastic
# clients. Needs to be adapted to individual client usage.
#
# Must be called: ./.github/make.sh <target> <params>
#
# Version: 1.1.0
#
# Targets:
# ---------------------------
# assemble <VERSION> : build client artefacts with version
# bump     <VERSION> : bump client internals to version
# codegen  <VERSION> : generate endpoints
# docsgen  <VERSION> : generate documentation
# examplegen         : generate the doc examples
# clean              : clean workspace
#
# ------------------------------------------------------- #

# ------------------------------------------------------- #
# Bootstrap
# ------------------------------------------------------- #

script_path=$(dirname "$(realpath -s "$0")")
repo=$(realpath "$script_path/../")

# shellcheck disable=SC1090
CMD=$1
TASK=$1
TASK_ARGS=()
VERSION=$2
STACK_VERSION=$VERSION
set -euo pipefail

product="elastic/elasticsearch-py"
output_folder=".github/output"
codegen_folder=".github/output"
OUTPUT_DIR="$repo/${output_folder}"
REPO_BINDING="${OUTPUT_DIR}:/sln/${output_folder}"
WORKFLOW="${WORKFLOW-staging}"
mkdir -p "$OUTPUT_DIR"

echo -e "\033[34;1mINFO:\033[0m PRODUCT ${product}\033[0m"
echo -e "\033[34;1mINFO:\033[0m VERSION ${STACK_VERSION}\033[0m"
echo -e "\033[34;1mINFO:\033[0m OUTPUT_DIR ${OUTPUT_DIR}\033[0m"

# ------------------------------------------------------- #
# Parse Command
# ------------------------------------------------------- #

case $CMD in
    clean)
        echo -e "\033[36;1mTARGET: clean workspace $output_folder\033[0m"
        rm -rf "$output_folder"
        echo -e "\033[32;1mdone.\033[0m"
        exit 0
        ;;
    assemble)
        if [ -v $VERSION ]; then
            echo -e "\033[31;1mTARGET: assemble -> missing version parameter\033[0m"
            exit 1
        fi
        echo -e "\033[36;1mTARGET: assemble artefact $VERSION\033[0m"
        TASK=release
        TASK_ARGS=("$VERSION" "$output_folder")
        ;;
    codegen)
        VERSION=$(git rev-parse --abbrev-ref HEAD)
        echo -e "\033[36;1mTARGET: codegen API $VERSION\033[0m"
        TASK=codegen
        # VERSION is BRANCH here for now
        TASK_ARGS=("$VERSION" "$codegen_folder")
        ;;
    docsgen)
        if [ -v $VERSION ]; then
            echo -e "\033[31;1mTARGET: docsgen -> missing version parameter\033[0m"
            exit 1
        fi
        echo -e "\033[36;1mTARGET: generate docs for $VERSION\033[0m"
        TASK=codegen
        # VERSION is BRANCH here for now
        TASK_ARGS=("$VERSION" "$codegen_folder")
        ;;
    examplesgen)
        echo -e "\033[36;1mTARGET: generate examples\033[0m"
        TASK=codegen
        # VERSION is BRANCH here for now
        TASK_ARGS=("$VERSION" "$codegen_folder")
        ;;
    bump)
        if [ -v $VERSION ]; then
            echo -e "\033[31;1mTARGET: bump -> missing version parameter\033[0m"
            exit 1
        fi
        echo -e "\033[36;1mTARGET: bump to version $VERSION\033[0m"
        TASK=bump
        # VERSION is BRANCH here for now
        TASK_ARGS=("$VERSION")
        ;;
    *)
        echo -e "\nUsage:\n\t $CMD is not supported right now\n"
        exit 1
esac


# ------------------------------------------------------- #
# Build Container
# ------------------------------------------------------- #

echo -e "\033[34;1mINFO: building $product container\033[0m"

docker build \
  --build-arg BUILDER_UID="$(id -u)" \
  --file $repo/.buildkite/Dockerfile \
  --tag ${product} \
  .

# ------------------------------------------------------- #
# Run the Container
# ------------------------------------------------------- #

echo -e "\033[34;1mINFO: running $product container\033[0m"

if [[ "$CMD" == "assemble" ]]; then

  # Build dists into .github/output
  docker run \
     -u "$(id -u)" \
    --rm -v $repo/.github/output:/code/elasticsearch-py/dist \
    $product \
    /bin/bash -c "pip install build; python /code/elasticsearch-py/utils/build-dists.py $VERSION"

  # Verify that there are dists in .github/output
	if compgen -G ".github/output/*" > /dev/null; then

	  # Tarball everything up in .github/output
	  if [[ "$WORKFLOW" == 'snapshot' ]]; then
	    cd $repo/.github/output && tar -czvf elasticsearch-py-$VERSION-SNAPSHOT.tar.gz * && cd -
	  else
	    cd $repo/.github/output && tar -czvf elasticsearch-py-$VERSION.tar.gz * && cd -
    fi

		echo -e "\033[32;1mTARGET: successfully assembled client v$VERSION\033[0m"
		exit 0
	else
		echo -e "\033[31;1mTARGET: assemble failed, empty workspace!\033[0m"
		exit 1
	fi
fi

if [[ "$CMD" == "bump" ]]; then
  docker run \
    --rm -v $repo:/code/elasticsearch-py \
    $product \
    /bin/bash -c "python /code/elasticsearch-py/utils/bump-version.py $VERSION"

  exit 0
fi

if [[ "$CMD" == "codegen" ]]; then
  docker run \
     --rm -v $repo:/code/elasticsearch-py \
     $product \
     /bin/bash -c "cd /code && python -m pip install nox && \
     git clone https://$CLIENTS_GITHUB_TOKEN@github.com/elastic/elastic-client-generator-python.git && \
     cd /code/elastic-client-generator-python && GIT_BRANCH=$VERSION python -m nox -s generate-es && \
     cd /code/elasticsearch-py && python -m nox -s format"

  exit 0
fi

if [[ "$CMD" == "docsgen" ]]; then
    echo "TODO"
fi

if [[ "$CMD" == "examplesgen" ]]; then
    echo "TODO"
fi

echo "Must be called with '.github/make.sh [command]"
exit 1

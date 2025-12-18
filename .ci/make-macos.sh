#!/usr/bin/env bash

# macOS-friendly build entry for elastic/elasticsearch-py

set -euo pipefail

# Resolve paths robustly on macOS (no realpath -s)
script_dir=$(
  cd "$(dirname "$0")" >/dev/null 2>&1 || exit 1
  pwd -P
)
repo=$(
  cd "$script_dir/../" >/dev/null 2>&1 || exit 1
  pwd -P
)

CMD=${1:-}
VERSION=${2:-}

product="elastic/elasticsearch-py"
output_folder=".ci/output"
OUTPUT_DIR="$repo/$output_folder"

mkdir -p "$OUTPUT_DIR"

blue="\033[34;1m"; cyan="\033[36;1m"; green="\033[32;1m"; red="\033[31;1m"; reset="\033[0m"

echo -e "${blue}INFO:${reset} PRODUCT ${product}${reset}"
echo -e "${blue}INFO:${reset} VERSION ${VERSION:-<none>}${reset}"
echo -e "${blue}INFO:${reset} OUTPUT_DIR ${OUTPUT_DIR}${reset}"

usage() {
  cat <<EOF
Usage: .ci/make-macos.sh <command> [version]
Commands:
  clean
  assemble <VERSION>
  codegen  <VERSION>   (TODO)
  docsgen  <VERSION>   (TODO)
  examplesgen          (TODO)
  bump     <VERSION>   (TODO)
EOF
}

case "${CMD}" in
  clean)
    echo -e "${cyan}TARGET: clean workspace ${OUTPUT_DIR}${reset}"
    rm -rf "${OUTPUT_DIR}"
    echo -e "${green}done.${reset}"
    exit 0
    ;;
  assemble)
    if [[ -z "${VERSION:-}" ]]; then
      echo -e "${red}TARGET: assemble -> missing version parameter${reset}"
      usage
      exit 1
    fi
    echo -e "${cyan}TARGET: assemble artefact ${VERSION}${reset}"
    ;;
  codegen|docsgen|examplesgen|bump)
    # Placeholder commands — same interface as Linux script
    if [[ "${CMD}" != "examplesgen" && -z "${VERSION:-}" ]]; then
      echo -e "${red}TARGET: ${CMD} -> missing version parameter${reset}"
      usage
      exit 1
    fi
    echo -e "${cyan}TARGET: ${CMD} ${VERSION:-<none>} (TODO)${reset}"
    echo "TODO"
    exit 1
    ;;
  *)
    usage
    exit 1
    ;;
esac

# Build container with correct context and Dockerfile path
echo -e "${blue}INFO: building ${product} container${reset}"
docker build \
  --file "${repo}/.ci/Dockerfile" \
  --tag "${product}" \
  "${repo}"

# Run container and build dists into .ci/output
echo -e "${blue}INFO: running ${product} container${reset}"
docker run \
  --rm -v "${OUTPUT_DIR}:/code/elasticsearch-py/dist" \
  "${product}" \
  /bin/bash -c "python /code/elasticsearch-py/utils/build-dists.py ${VERSION}"

# Verify output and create bundle tarball
if compgen -G "${OUTPUT_DIR}/*" > /dev/null; then
  (cd "${OUTPUT_DIR}" && tar -czvf "elasticsearch-py-${VERSION}.tar.gz" * )
  echo -e "${green}TARGET: successfully assembled client v${VERSION}${reset}"
  exit 0
else
  echo -e "${red}TARGET: assemble failed, empty workspace!${reset}"
  exit 1
fi
#!/bin/bash

if [[ -z "$NOX_SESSION" ]]; then
  NOX_SESSION=test-${PYTHON_VERSION%-dev}
fi
nox -s $NOX_SESSION

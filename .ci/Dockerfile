ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

WORKDIR /code/elasticsearch-py
COPY . .
RUN python -m pip install \
    --no-cache-dir \
    --disable-pip-version-check \
    -e . \
    -r dev-requirements.txt

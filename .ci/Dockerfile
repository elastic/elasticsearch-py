ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

WORKDIR /code/elasticsearch-py
COPY dev-requirements.txt .
RUN python -m pip install \
    -U --no-cache-dir \
    --disable-pip-version-check \
    nox -rdev-requirements.txt

COPY . .
RUN python -m pip install -e .

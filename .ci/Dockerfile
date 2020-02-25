ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

WORKDIR /code/elasticsearch-py

COPY . .

RUN python -m pip install .[requests]

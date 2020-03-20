ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

WORKDIR /code/elasticsearch-py

COPY dev-requirements.txt .
RUN python -m pip install -r dev-requirements.txt

COPY . .

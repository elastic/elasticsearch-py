ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

COPY dev-requirements.txt /tmp
RUN python -m pip install -r /tmp/dev-requirements.txt

WORKDIR /code/elasticsearch-py

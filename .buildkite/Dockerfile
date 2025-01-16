ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}

# Default UID/GID to 1000
# it can be overridden at build time
ARG BUILDER_UID=1000
ARG BUILDER_GID=1000
ENV BUILDER_USER elastic
ENV BUILDER_GROUP elastic
ENV PATH="${PATH}:/var/lib/elastic/.local/bin"

# Create user
RUN groupadd --system -g ${BUILDER_GID} ${BUILDER_GROUP} \
    && useradd --system --shell /bin/bash -u ${BUILDER_UID} -g ${BUILDER_GROUP} -d /var/lib/elastic -m elastic 1>/dev/null 2>/dev/null \
    && mkdir -p /code/elasticsearch-py && mkdir /code/elasticsearch-py/build \
    && chown -R ${BUILDER_USER}:${BUILDER_GROUP} /code/
WORKDIR /code/elasticsearch-py
USER ${BUILDER_USER}:${BUILDER_GROUP}
RUN python -m pip install --disable-pip-version-check nox
COPY --chown=$BUILDER_USER:$BUILDER_GROUP . .

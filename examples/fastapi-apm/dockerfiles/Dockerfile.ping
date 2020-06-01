FROM python:3.8
WORKDIR /
RUN python -m pip install \
    --no-cache \
    --disable-pip-version-check \
    urllib3
COPY ping.py /
CMD python ping.py

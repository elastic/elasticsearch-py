FROM python:3.8

EXPOSE 9292
WORKDIR /

COPY requirements.txt /
RUN python -m pip install \
    --no-cache \
    --disable-pip-version-check \
    -r /requirements.txt

COPY app.py /
CMD uvicorn app:app --host=0.0.0.0 --port=9292

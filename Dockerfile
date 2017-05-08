FROM python:3.4-alpine
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh curl
ADD . /code/elasticsearch-py
WORKDIR /code/elasticsearch-py
RUN pip install requests==1.0.0 nose coverage mock pyaml nosexcover ipdb
RUN python setup.py develop

CMD ["./wait-for-elasticsearch.sh", "http://elasticsearch:9200", "--", "python", "setup.py", "test"]

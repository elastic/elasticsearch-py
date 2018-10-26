clean:
	docker-compose down --remove-orphans --volumes

build:
	PYTHON_VERSION=${PYTHON_VERSION} docker-compose build client

pull:
	ELASTICSEARCH_VERSION=${ELASTICSEARCH_VERSION} PYTHON_VERSION=${PYTHON_VERSION} docker-compose pull

push:
	# requires authentication.
	PYTHON_VERSION=${PYTHON_VERSION} docker-compose push client

run_tests:
	ELASTICSEARCH_VERSION=${ELASTICSEARCH_VERSION} PYTHON_VERSION=${PYTHON_VERSION} docker-compose run client python setup.py test

start_elasticsearch:
	ELASTICSEARCH_VERSION=${ELASTICSEARCH_VERSION} docker-compose up -d elasticsearch

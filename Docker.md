# Getting started with Docker

Getting started with development and and running tests with Docker is quite simple and straight forward. 

## Installation

1. Make sure you have Docker [installed](https://docs.docker.com/engine/installation/) 
2. Make sure you have Docker Compose [installed](https://docs.docker.com/compose/install/)

## Setup

First make sure you have cloned the [elasticsearch](https://github.com/elastic/elasticsearch) repo to the same level as elasticsearch-py. 

If you read the instructions in [test_elasticsearch](https://github.com/elastic/elasticsearch-py/blob/master/test_elasticsearch/README.rst#elasticsearch-py-test-suite) you will notice that
elasticsearch-py has a requirement on a git checkout of elasticsearch in the same directory that elasticsearch-py is cloned at like so: 

```
$ tree `pwd`
/home/develop/elastic
├── elasticsearch
└── elasticsearch-py
```

Now `cd` into the `elasticsearch-py` directory and run the tests:

```
docker-compose up
```

This should run 750+ tests and they all should pass. 
The default command for this docker container is to run the tests `python setup.py test`

## Development

Once we have our environment configured and setup we can begin development. 

Open the code in your favorite editor and start making changes. 

### Tips and Tricks

#### 1. Docker Exec

With `docker exec` you can create a shell in an already runnng container. This is useful for looking a files, running commands in a container etc.. 

First run `docker ps` to get a list of running containers. 
Then run `docker exec -it <container_id> ash` this will create an ash shell prompt running in the container. 

#### 2. Docker Compose Run

Sometimes it's useful to create debug statements in your code. A quick and easy way to run the code to get to a debug prompt is to use the docker-compose run command. 

```
$ docker-compose run --rm client ash
/code/elasticsearch-py #
```

This will create a 1 off container that will be deleted after it closes. You will have an `ash` prompt and can run commands inside the container. Just like the docker exec. Except this container is brand new. 

From here you can run the tests or command to trigger the debug prompt

```
/code/elasticsearch-py # python setup.py test
```

OR

```
/code/elasticsearch-py # python run_tests.py
```

OR

```
/code/elasticsearch-py # nosetests my.specific.test
```

Again all of these commands could be run in one off contaienrs as well with replacing the `ash` with the `command` you want to run, ie:

```
$ docker-compose run --rm client nosetests my.specific.test
```






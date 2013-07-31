import time
import subprocess
import tempfile
import os

import requests

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

from unittest import SkipTest

data_dir = None

CMD = """
    elasticsearch \
    -f \
    -D es.cluster.name=%(cluster_name)s \
    -D es.node.name=test_name \
    -D es.http.port=%(port)s \
    -D es.gateway.type=none \
    -D es.index.store.type=memory \
    -D es.discovery.zen.ping.multicast.enabled=false \
    -D es.path.data=%(data_dir)s \
    -D es.pidfile=%(pidfile)s \
    >/dev/null 2>&1
"""

server = None
pidfile = tempfile.mktemp()

from os import environ
from os.path import join, dirname, pardir, exists

YAML_DIR = environ.get(
    'YAML_TEST_DIR',
    join(
        dirname(__file__),
        pardir, pardir, pardir,
        'elasticsearch-rest-api-spec', 'test'
    )
)

def setup():
    # no integration tests, skip starting the server
    if not exists(YAML_DIR):
        raise SkipTest('')
    global server

    # use running ES instance, don't attempt to start our own
    if 'TEST_ES_SERVER' in os.environ:
        return

    # check installed
    if subprocess.call('which vim >/dev/null 2>&1', shell=True) != 0:
        raise SkipTest("No Elasticsearch server, skipping integration tests.")

    args = {
        'cluster_name': 'es_client_test',
        'port': 9900,
        'data_dir': tempfile.tempdir,
        'pidfile': pidfile
    }

    # check running
    try:
        requests.get('http://localhost:%(port)s' % args)
    except requests.ConnectionError:
        pass
    else:
        raise SkipTest('Elasticsearch already running!')


    cmd = CMD % args

    server = subprocess.Popen(cmd, shell=True)
    os.environ['TEST_ES_SERVER'] = 'localhost:%(port)s' % args
    client = Elasticsearch([os.environ['TEST_ES_SERVER']])

    # wait for green status
    for _ in range(100):
        time.sleep(.1)
        try:
            client.cluster.health(wait_for_status='yellow')
            break
        except ConnectionError:
            continue

    else:
        # timeout
        raise SkipTest("Elasticsearch failed to start.")


def teardown():
    if server is not None:
        with open(pidfile) as pidf:
            pid = pidf.read()
            os.kill(int(pid), 15)
        server.wait()

import time
import subprocess
import tempfile
import os

import requests

from nose import SkipTest

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

def setup():
    global server

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

    # wait for green status
    for _ in range(100):
        response = None
        time.sleep(.1)
        try:
            response = requests.get('http://localhost:%(port)s/_cluster/health?wait_for_status=green' % args)
        except requests.ConnectionError:
            continue

        if response.status_code == 200:
            break

    else:
        # timeout
        raise SkipTest("Elasticsearch failed to start.")


def teardown():
    if server is not None:
        with open(pidfile) as pidf:
            pid = pidf.read()
            os.kill(int(pid), 15)
        server.wait()

import time
import os

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

from ..test_cases import TestCase, SkipTest

client = None

def get_client():
    global client
    if client is not None:
        return client

    # construct kwargs from the environment
    kw = {}
    if 'TEST_ES_CONNECTION' in os.environ:
        from elasticsearch import connection
        kw['connection_class'] = getattr(connection, os.environ['TEST_ES_CONNECTION'])

    # try and locate manual override in the local environment
    try:
        from test_elasticsearch.local import get_client as local_get_client
        client = local_get_client([os.environ.get('TEST_ES_SERVER', {})], **kw)
    except ImportError:
        # fallback to using vanilla client
        client = Elasticsearch([os.environ.get('TEST_ES_SERVER', {})], **kw)

    # wait for yellow status
    for _ in range(200):
        time.sleep(.1)
        try:
            client.cluster.health(wait_for_status='yellow')
            return client
        except ConnectionError:
            continue
    else:
        # timeout
        raise SkipTest("Elasticsearch failed to start.")

def setup():
    get_client()

ES_VERSION = None

def _get_version(version_string):
    version = version_string.strip().split('.')
    return tuple(int(v) if v.isdigit() else 999 for v in version)

class ElasticTestCase(TestCase):
    client = None
    def setUp(self):
        if ElasticTestCase.client is None:
            ElasticTestCase.client = get_client()
        self.client = ElasticTestCase.client

    def tearDown(self):
        self.client.indices.delete('*')
        try:
            self.client.indices.delete_template('*')
        except NotFoundError:
            pass

    @property
    def es_version(self):
        global ES_VERSION
        if ES_VERSION is None:
            version_string = self.client.info()['version']['number']
            ES_VERSION = _get_version(version_string)
        return ES_VERSION


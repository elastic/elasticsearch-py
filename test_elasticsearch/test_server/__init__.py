from elasticsearch.helpers import test
from elasticsearch.helpers.test import ElasticsearchTestCase as BaseTestCase

client = None


def get_client(**kwargs):
    global client
    if client is not None and not kwargs:
        return client

    # try and locate manual override in the local environment
    try:
        from test_elasticsearch.local import get_client as local_get_client

        new_client = local_get_client(**kwargs)
    except ImportError:
        # fallback to using vanilla client
        new_client = test.get_test_client(**kwargs)

    if not kwargs:
        client = new_client

    return new_client


def setup():
    get_client()


class ElasticsearchTestCase(BaseTestCase):
    @staticmethod
    def _get_client(**kwargs):
        return get_client(**kwargs)

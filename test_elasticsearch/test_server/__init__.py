from elasticsearch.helpers.test import get_test_client, ElasticsearchTestCase as BaseTestCase

client = None

def get_client():
    global client
    if client is not None:
        return client

    # try and locate manual override in the local environment
    try:
        from test_elasticsearch.local import get_client as local_get_client
        client = local_get_client()
    except ImportError:
        # fallback to using vanilla client
        client = get_test_client()

    return client


def setup():
    get_client()

class ElasticsearchTestCase(BaseTestCase):
    @staticmethod
    def _get_client():
        return get_client()

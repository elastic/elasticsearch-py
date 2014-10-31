from .http_requests import RequestsHttpConnection
from ..exceptions import ImproperlyConfigured
try:
    from alf.client import Client
    ALF_AVAILABLE = True
except ImportError:
    ALF_AVAILABLE = False


class AlfHttpConnection(RequestsHttpConnection):
    """
    Connection using the OAuth 2, `requests` based, `Alf` library.

    https://github.com/globocom/alf

    :arg oauth: OAuth 2 dict argument, with 3 keys: 'token_endpoint', 'client_id' and 'client_secret'. If this argument is not present, requests is used instead.
    :arg use_ssl: use ssl for the connection if `True`
    """
    def __init__(self, host='localhost', port=9200, oauth=None, use_ssl=False, **kwargs):
        if not ALF_AVAILABLE:
            raise ImproperlyConfigured("Please install alf to use AlfHttpConnection.")

        if oauth is None:
            return super(AlfHttpConnection, self).__init__(host=host, port=port, use_ssl=use_ssl, **kwargs)

        super(RequestsHttpConnection, self).__init__(host= host, port=port, **kwargs)
        self.session = Client(
            token_endpoint=oauth.get('token_endpoint'),
            client_id=oauth.get('client_id'),
            client_secret=oauth.get('client_secret')
        )
        self.base_url = 'http%s://%s:%d%s' % (
            's' if use_ssl else '',
            host, port, self.url_prefix
        )
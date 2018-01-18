from boto.connection import AWSAuthConnection
from boto.provider import Provider
from elasticsearch.connection.base import Connection as BaseConnection

class BotoConnection(AWSAuthConnection, BaseConnection):
    AuthServiceName = 'es'
    def __init__(self, host, **kwargs):
        provider = Provider('aws', access_key=kwargs.get('access_key'), secret_key=kwargs.get('secret_key'))
        super(BotoConnection, self).__init__(provider=provider, host=host)

    def _required_auth_capability(self):
        return ['hmac-v4']

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=(), headers=None):
        data = body or ''
        res = self.make_request(method, url, headers=headers, host=self.host, data=data, auth_path=url)
        return res.status, dict(res.msg.items()), res.read().decode('utf-8')
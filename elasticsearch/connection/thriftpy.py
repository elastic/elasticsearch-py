# coding: utf-8

from __future__ import absolute_import

import os
import time
from socket import timeout as SocketTimeout

THRIFT_FILE = os.path.join(os.path.dirname(__file__), 'elasticsearch.thrift')

try:
    import thriftpy
    from thriftpy.thrift import TException
    from thriftpy.rpc import make_client
    _t = thriftpy.load(THRIFT_FILE, module_name="elasticsearch_thrift")
    THRIFTPY_AVAILABLE = True
except ImportError:
    THRIFTPY_AVAILABLE = False

from ..exceptions import ConnectionError
from .pooling import PoolingConnection

__all__ = ('THRIFT_FILE', 'THRIFTPY_AVAILABLE', 'ThriftpyConnection')


class ThriftpyConnection(PoolingConnection):
    transport_schema = 'thrift'

    def __init__(self, host='localhost', port=9500, **kwargs):
        super(ThriftpyConnection, self).__init__(
            host=host, port=port, **kwargs
        )
        self._tsocket_host = host
        self._tsocket_port = port

    def _make_connection(self):
        client = make_client(
            _t.Rest, self._tsocket_host, self._tsocket_port,
            timeout=self.timeout * 1000.0
        )
        return client

    def perform_request(self, method, url, params=None, body=None,
                        timeout=None, ignore=()):

        request = _t.RestRequest(
            method=_t.Method._NAMES_TO_VALUES[method.upper()],
            uri=url, parameters=params, body=body
        )

        start = time.time()
        tclient = None
        try:
            tclient = self._get_connection()
            response = tclient.execute(request)
            duration = time.time() - start
        except (TException, SocketTimeout) as e:
            self.log_request_fail(
                method, url, body, time.time() - start, exception=e
            )
            raise ConnectionError('N/A', str(e), e)
        finally:
            if tclient:
                self._release_connection(tclient)

        code = response.status
        if not (200 <= code < 300) and code not in ignore:
            self.log_request_fail(method, url, body, duration, code)
            self._raise_error(code, response.body)

        self.log_request_success(
            method, url, url, body, code, response.body, duration
        )

        headers = {}
        if response.headers:
            headers = dict((k.lower(), v) for k, v in response.headers.items())
        return code, headers, response.body or ''

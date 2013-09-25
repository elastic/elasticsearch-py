from __future__ import absolute_import
import time

try:
    from .esthrift import Rest
    from .esthrift.ttypes import Method, RestRequest

    from thrift.transport import TTransport, TSocket, TSSLSocket
    from thrift.protocol import TBinaryProtocol
    from thrift.Thrift import TException
    THRIFT_AVAILABLE = True
except ImportError:
    THRIFT_AVAILABLE = False

from ..exceptions import ConnectionError, ImproperlyConfigured
from .pooling import PoolingConnection

class ThriftConnection(PoolingConnection):
    """
    Connection using the `thrift` protocol to communicate with elasticsearch.

    See https://github.com/elasticsearch/elasticsearch-transport-thrift for additional info.
    """
    transport_schema = 'thrift'

    def __init__(self, host='localhost', port=9500, framed_transport=False, thrift_ssl=False, thrift_socket_extra_args=None, thrift_headers=None, **kwargs):
        """
        :arg framed_transport: use `TTransport.TFramedTransport` instead of
            `TTransport.TBufferedTransport`
        """
        if not THRIFT_AVAILABLE:
            raise ImproperlyConfigured("Thrift is not available.")

        super(ThriftConnection, self).__init__(host=host, port=port, **kwargs)
        self._framed_transport = framed_transport
        self._tsocket_class = TSocket.TSocket
        if thrift_ssl:
            self._tsocket_class = TSSLSocket.TSSLSocket
        self._tsocket_args = (host, port)
        self._tsocket_kwargs = thrift_socket_extra_args or dict()
        self._thrift_headers = thrift_headers or dict()

    def _make_connection(self):
        socket = self._tsocket_class(*self._tsocket_args, **self._tsocket_kwargs)
        socket.setTimeout(self.timeout * 1000.0)
        if self._framed_transport:
            transport = TTransport.TFramedTransport(socket)
        else:
            transport = TTransport.TBufferedTransport(socket)

        protocol = TBinaryProtocol.TBinaryProtocolAccelerated(transport)
        client = Rest.Client(protocol)
        transport.open()
        return client

    def perform_request(self, method, url, params=None, body=None, timeout=None):
        request = RestRequest(method=Method._NAMES_TO_VALUES[method.upper()], uri=url,
                    parameters=params, headers=self._thrift_headers, body=body)

        start = time.time()
        tclient = self._get_connection()
        try:
            response = tclient.execute(request)
            duration = time.time() - start
        except TException as e:
            self.log_request_fail(method, url, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)
        finally:
            self._release_connection(tclient)

        if not (200 <= response.status < 300):
            self.log_request_fail(method, url, duration, response.status)
            self._raise_error(response.status, response.body)

        self.log_request_success(method, url, url, body, response.status,
            response.body, duration)

        return response.status, response.body




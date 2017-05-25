import base64
import time
import warnings

try:
    from google.appengine.api import urlfetch
    URLFETCH_AVAILABLE = True
except ImportError:
    URLFETCH_AVAILABLE = False

from .base import Connection
from ..compat import urlencode, urlparse
from ..exceptions import ConnectionError, ConnectionTimeout, SSLError, ImproperlyConfigured


class URLFetchHttpConnection(Connection):
    """
    Connection using the `requests` library.

    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple. Any value will be passed into requests as `auth`.
    :arg use_ssl: use ssl for the connection if `True`
    :arg verify_certs: whether to verify SSL certificates
    :arg headers: any custom http headers to be add to requests
    """
    headers = {}
    rpc = None
    verify_certs = None

    def __init__(self, host='localhost', port=9200, http_auth=None,
                 use_ssl=False, verify_certs=True, headers=None, **kwargs):
        if not URLFETCH_AVAILABLE:
            raise ImproperlyConfigured('Please install urlfetch to use URLFetchHttpConnection.')

        super(URLFetchHttpConnection, self).__init__(host=host, port=port, **kwargs)

        timeout = kwargs.get('timeout', 60)

        self.rpc = urlfetch.create_rpc(deadline=timeout, callback=None)

        if isinstance(headers, dict):
            self.headers = headers

        if http_auth is not None:
            if isinstance(http_auth, (tuple, list)):
                http_auth = ':'.join(http_auth)
            self.headers.update({
                'Authorization': 'Basic {}'.format(
                    base64.b64encode(http_auth)
                )
            })
        self.base_url = 'http%s://%s:%d%s' % (
            's' if use_ssl else '',
            host, port, self.url_prefix
        )
        self.verify_certs = verify_certs

        if use_ssl and not verify_certs:
            warnings.warn(
                'Connecting to %s using SSL with verify_certs=False is insecure.' % self.base_url)

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        url = self.base_url + url
        if params:
            url = '{}?{}'.format(
                url,
                urlencode(params or {})
            )
        path = urlparse(url).path

        start = time.time()
        try:
            urlfetch.make_fetch_call(self.rpc, url, payload=body, method=method,
                                     headers=self.headers, allow_truncated=False, follow_redirects=True,
                                     validate_certificate=self.verify_certs)
            response = self.rpc.get_result()
            duration = time.time() - start
            raw_data = response.content
        except urlfetch.SSLCertificateError as e:
            self.log_request_fail(method, url, path, body, time.time() - start, exception=e)
            raise SSLError('N/A', str(e), e)
        except urlfetch.DeadlineExceededError as e:
            self.log_request_fail(method, url, path, body, time.time() - start, exception=e)
            raise ConnectionTimeout('TIMEOUT', str(e), e)
        except (urlfetch.ConnectionClosedError, urlfetch.DownloadError, urlfetch.InternalTransientError) as e:
            self.log_request_fail(method, url, path, '', time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)
        except AssertionError as e:
            self.log_request_fail(method, url, path, '', time.time() - start, exception=e)
            raise AssertionError('URLFetchHTTPConnection RPC error: {}'.format(e))

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status_code < 300) and response.status_code not in ignore:
            self.log_request_fail(method, url, path or response.request.path_url, body, duration, response.status_code,
                                  raw_data)
            self._raise_error(response.status_code, raw_data)

        self.log_request_success(method, url, path or response.request.path_url, body, response.status_code, raw_data,
                                 duration)

        return response.status_code, response.headers, raw_data

    def close(self):
        """
        Explicitly closes connections
        """
        pass

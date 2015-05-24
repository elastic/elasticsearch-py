import time
import warnings
try:
    from google.appengine.api import urlfetch
    URLFETCH_AVAILABLE = True
except ImportError:
    URLFETCH_AVAILABLE = False

from .base import Connection
from ..exceptions import ConnectionError, ImproperlyConfigured, ConnectionTimeout, SSLError
from ..compat import urlencode


class UrlfetchHttpConnection(Connection):
    """
    Connection using the app engine's `urlfetch` library.

    Note that urlfetch is limited to work only with 80-90, 440-450,
    1024-65535 ports.

    :arg http_auth: optional http auth information as either ':' separated
        string or a tuple. Any value will be passed into requests as `auth`.
    :arg use_ssl: use ssl for the connection if `True`
    :arg verify_certs: whether to verify SSL certificates
    """
    def __init__(self, host, port=9200, http_auth=None, use_ssl=False,
                 verify_certs=False, **kwargs):
        if not URLFETCH_AVAILABLE:
            raise ImproperlyConfigured("Urlfetch can be used only with Google App Engine runtime.")

        super(UrlfetchHttpConnection, self).__init__(host=host, port=port, **kwargs)
        self.headers = {}
        if http_auth is not None:
            if isinstance(http_auth, (tuple, list)):
                http_auth = ':'.join(http_auth)
            self.headers['Authorization'] = 'Basic %s' % http_auth.encode('base64')
        self.base_url = 'http%s://%s:%d%s' % (
            's' if use_ssl else '',
            host, port, self.url_prefix
        )
        self.validate_certificate = None
        if verify_certs:
          self.validate_certificate = True

        if use_ssl and not verify_certs:
            warnings.warn(
                'Connecting to %s using SSL with verify_certs=False is insecure.' % self.base_url)

    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        start = time.time()
        try:
            response = urlfetch.fetch(
              url='%s?%s' % (self.base_url + url, urlencode(params or {})),
              # dev app server cuts last two characters from the payload,
              # so we will add two spaces as a workaround for this.
              payload=body + '  ',
              method=method,
              headers=self.headers,
              deadline=timeout,
              validate_certificate=self.validate_certificate)
            duration = time.time() - start
            raw_data = response.content
        except urlfetch.SSLCertificateError as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise SSLError('N/A', str(e), e)
        except urlfetch.DeadlineExceededError as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise ConnectionTimeout('TIMEOUT', str(e), e)
        except urlfetch.Error as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status_code < 300) and response.status_code not in ignore:
            self.log_request_fail(method, url, body, duration, response.status_code)
            self._raise_error(response.status_code, raw_data)

        self.log_request_success(method, url, urlencode(params or {}), body, response.status_code, raw_data, duration)

        return response.status_code, response.headers, raw_data

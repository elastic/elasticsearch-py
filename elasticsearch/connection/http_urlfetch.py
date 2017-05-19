from .base import Connection
from ..exceptions import ConnectionError
from ..compat import urlencode
import time
import json

try:
    from google.appengine.api import urlfetch
    URLFETCH_AVAILABLE = True
except ImportError:
    URLFETCH_AVAILABLE = False


class UrlFetchAppEngine(Connection):
    """
    Class using Google App Engine `Urlfetch`. The idea is using this on app
    that need to be server on Google App Engine.
    """
    def __init__(self, host='localhost', port=9200, http_auth=None,
            use_ssl=False, verify_certs=True, ca_certs=None, client_cert=None,
            client_key=None, ssl_version=None, ssl_assert_hostname=None,
            ssl_assert_fingerprint=None, maxsize=10, headers=None, **kwargs):
                """
                :arg host: hostname of the node (default: localhost)
                :arg port: port to use (integer, default: 9200)
                :arg use_ssl: True if necessay to validate.
                :arg url_prefix: optional url prefix for elasticsearch
                :arg timeout: default timeout in seconds (float, default: 10)
                """
                super(UrlFetchAppEngine, self).__init__(host=host, mport=port, use_ssl=use_ssl, **kwargs)

                self.headers = headers.copy() if headers else {}

                if http_auth is not None:
                    if isinstance(http_auth, (tuple, list)):
                        http_auth = ':'.join(http_auth)

                    self.headers['Authorization'] = 'Basic %s' % http_auth.encode('base64')

                if verify_certs:
                    self.validate_certificate = True

                if use_ssl and not verify_certs:
                    print ('Connecting to %s using SSL with verify_certs=False is insecure.' % self.base_url)


    def perform_request(self, method, url, params=None, body=None, timeout=None, ignore=()):
        start = time.time()

        url = self.url_prefix + url
        if params:
            url = '%s?%s' % (url, urlencode(params))
        full_url = self.host + url

        try:
            response = urlfetch.fetch(
              url=full_url,
              payload=body,
              method=method,
              headers=self.headers,
              deadline=timeout,
              validate_certificate=self.validate_certificate)
            duration = time.time() - start
            raw_data = response.content
        except Exception as e:
            self.log_request_fail(method, full_url, url, json.dumps(body), time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status_code < 300) and response.status_code not in ignore:
            self.log_request_fail(method, full_url, url, json.dumps(body), duration, response.status_code)
            self._raise_error(response.status_code, raw_data)

        self.log_request_success(method, full_url, url, json.dumps(body), response.status_code, raw_data, duration)

        return response.status_code, response.headers, raw_data

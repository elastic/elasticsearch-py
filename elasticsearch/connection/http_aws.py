import time
import warnings, hashlib, hmac, os, datetime, base64, sys
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from .base import Connection
from ..exceptions import ConnectionError, ImproperlyConfigured, ConnectionTimeout, SSLError
from ..compat import urlencode, string_types

class AwsHttpConnection(Connection):
    """
    Connection for AWS elastic search that provides supports authentication for IAM users granted access
    to the cluster.

    When you select the option to grant IAM users access to an AWS elasticsearch cluster, any elasticsearch 
    requests must use the same AWS V4 authentication that other AWS APIs use.  This Connection implementation 
    provides the necessary HTTP payload based on the AWS credentials associated with IAM user granted access.  
    The only requirement is that standard AWS credentials be defined as Unix environment variables.  

    Those are: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.

    :arg region: AWS region to which the Elasticsearch cluster is deployed.  Defaults to us-west-1.
    """
    def __init__(self, host='localhost', use_ssl=False, port=80, region='us-west-1', **kwargs):
        super(AwsHttpConnection, self).__init__(host= host, port=port, **kwargs)
        self.session = requests.session()
        self.server = host
        self.region = region
        self.base_url = 'http%s://%s:%d%s' % (
            's' if use_ssl else '',
            host, port, self.url_prefix
        )

        self.access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        self.secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        if self.access_key is None or self.secret_key is None:
            print 'No access key is available.'
            sys.exit()
        self.signed_headers = 'host;x-amz-date'
        self.algorithm = 'AWS4-HMAC-SHA256'
        self.service = 'es'

    def sign(self, key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.sign(('AWS4' + key).encode('utf-8'), dateStamp)
        kRegion = self.sign(kDate, regionName)
        kService = self.sign(kRegion, serviceName)
        kSigning = self.sign(kService, 'aws4_request')
        return kSigning

    def perform_request(self, method, request_url, params=None, body=None, timeout=None, ignore=()):
        url = self.base_url + request_url

        t = datetime.datetime.utcnow()
        amzdate = t.strftime('%Y%m%dT%H%M%SZ')
        datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

        canonical_headers = 'host:' + self.server + '\n' + 'x-amz-date:' + amzdate + '\n'    
        if body is None:
            payload_hash = hashlib.sha256('').hexdigest()
        else:
            payload_hash = hashlib.sha256(body).hexdigest()

        canonical_request = method + '\n' + request_url + '\n' + '' + '\n' + canonical_headers + '\n' + self.signed_headers + '\n' + payload_hash

        credential_scope = datestamp + '/' + self.region + '/' + self.service + '/' + 'aws4_request'

        string_to_sign = self.algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()


        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        signing_key = self.getSignatureKey(self.secret_key, datestamp, self.region, self.service)

        # Sign the string_to_sign using the signing_key
        signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

        authorization_header = self.algorithm + ' ' + 'Credential=' + self.access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + self.signed_headers + ', ' + 'Signature=' + signature

        self.session.headers.update({'x-amz-date':amzdate, 'Authorization':authorization_header})

        if params:
            url = '%s?%s' % (url, urlencode(params or {}))

        start = time.time()
        try:
            response = self.session.request(method, url, data=body, timeout=timeout or self.timeout)
            duration = time.time() - start
            raw_data = response.text
        except requests.exceptions.SSLError as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise SSLError('N/A', str(e), e)
        except requests.Timeout as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise ConnectionTimeout('TIMEOUT', str(e), e)
        except requests.ConnectionError as e:
            self.log_request_fail(method, url, body, time.time() - start, exception=e)
            raise ConnectionError('N/A', str(e), e)

        # raise errors based on http status codes, let the client handle those if needed
        if not (200 <= response.status_code < 300) and response.status_code not in ignore:
            self.log_request_fail(method, url, body, duration, response.status_code)
            self._raise_error(response.status_code, raw_data)

        self.log_request_success(method, url, response.request.path_url, body, response.status_code, raw_data, duration)

        return response.status_code, response.headers, raw_data

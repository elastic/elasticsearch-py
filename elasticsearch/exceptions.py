__all__ = [
    'ImproperlyConfigured', 'ElasticsearchException', 'SerializationError',
    'TransportError', 'NotFoundError', 'ConflictError', 'RequestError'
]

class ImproperlyConfigured(Exception):
    pass

class ElasticsearchException(Exception):
    pass


class SerializationError(ElasticsearchException):
    pass


class TransportError(ElasticsearchException):
    """ Exception raised when ES returns a non-OK (>=400) HTTP status code. """
    @property
    def status_code(self):
        """ The HTTP status code of the response that precipitated the error. """
        return self.args[0]

    @property
    def error(self):
        """ A string error message. """
        return self.args[1]

    @property
    def info(self):
        """ Dict of returned error info from ES, where applicable. """
        return self.args[2]

    def __str__(self):
        return 'TransportError(%d, %r)' % (self.status_code, self.error)


class ConnectionError(TransportError):
    """ Error raised when there was an exception while talking to ES. """
    def __str__(self):
        return 'ConnectionError(%s) caused by: %s(%s)' % (
            self.error, self.info.__class__.__name__, self.info)


class NotFoundError(TransportError):
    pass


class ConflictError(TransportError):
    pass


class RequestError(TransportError):
    pass

# more generic mappings from status_code to python exceptions
HTTP_EXCEPTIONS = {
    400: RequestError,
    404: NotFoundError,
    409: ConflictError,
}

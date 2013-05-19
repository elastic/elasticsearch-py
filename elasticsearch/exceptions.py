__all__ = ['ElastiSearchException', 'SerializationError', 'TransportError', 'NotFoundError']

class ElastiSearchException(Exception):
    pass


class SerializationError(ElastiSearchException):
    pass


class TransportError(ElastiSearchException):
    pass


class ConnectionError(TransportError):
    pass


class NotFoundError(TransportError):
    " 404 "


HTTP_EXCEPTIONS = {
    404: NotFoundError,
}

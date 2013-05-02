class ElastiSearchException(Exception):
    pass


class SerializationError(ElastiSearchException):
    pass


class TransportError(ElastiSearchException):
    pass


class NotFoundError(TransportError):
    " 404 "


HTTP_EXCEPTIONS = {
    404: NotFoundError,
}

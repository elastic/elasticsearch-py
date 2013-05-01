class ElastiSearchException(Exception):
    pass


class TransportError(ElastiSearchException):
    pass


class NotFoundError(TransportError):
    " 404 "


HTTP_EXCEPTIONS = {
    404: NotFoundError,
}

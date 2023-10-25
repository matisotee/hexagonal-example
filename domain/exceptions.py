class BaseApplicationException(Exception):
    pass


class StockNotFound(BaseApplicationException):
    pass


class ServiceCallException(BaseApplicationException):
    pass

from sanic.exceptions import SanicException


class ValidException(SanicException):
    status_code = 400


class ApiReqValidException(ValidException):
    pass


class ApiResValidException(ValidException):
    status_code = 500

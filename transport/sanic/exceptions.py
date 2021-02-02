from sanic.exceptions import SanicException


class SanicReqValidationException(SanicException):
    status_code = 400


class SanicResValidationException(SanicException):
    status_code = 500


class SanicUserConflictException(SanicException):
    status_code = 409


class SanicDBException(SanicException):
    status_code = 500


class SanicMsgNotFoundException(SanicException):
    status_code = 404


class SanicUserNotFoundException(SanicException):
    status_code = 404


class SanicPassHashException(SanicException):
    status_code = 500


class SanicAuthException(SanicException):
    status_code = 401
from . import GoogleException


class CalendarForbiddenException(GoogleException):
    def __init__(self, message: str):
        super().__init__(message=message, code=403)


class CalendarParamsException(GoogleException):
    def __init__(self, message: str):
        super().__init__(message=message, code=422)


class CalendarIdentifierException(GoogleException):
    def __init__(self, message: str, code: int):
        super().__init__(message=message, code=code)

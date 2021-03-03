from abc import ABC

from .. import ServiceParamsException, ServiceException


class GoogleParamsException(ServiceParamsException, ABC):
    pass


class GoogleException(ServiceException):
    def __init__(self, message: str, code: int):
        self.__err_msg = message
        self.__code = code
        super().__init__()

    def _create_exception_message(self) -> str:
        return self.__err_msg

    def _create_exception_response_code(self) -> int:
        return self.__code


class GoogleBackendError(GoogleException):
    __GOOGLE_BACKEND_ERR_MSG = 'Error on Google backend.'
    __GOOGLE_BACKEND_ERR_CODE = 500

    def __init__(self):
        super(GoogleBackendError, self).__init__(message=self.__GOOGLE_BACKEND_ERR_MSG,
                                                 code=self.__GOOGLE_BACKEND_ERR_CODE)


class InvalidAuthenticationCodeException(GoogleParamsException):
    __INVALID_CODE_ERR_MSG = 'Invalid Google Authenticate code'

    def _create_exception_message(self) -> str:
        return self.__INVALID_CODE_ERR_MSG

from . import GoogleParamsException


class TokenException(GoogleParamsException):
    __EXPIRED_CODE_ERR_MSG = 'Invalid token.'

    def _create_exception_message(self) -> str:
        return self.__EXPIRED_CODE_ERR_MSG


class InvalidAccessTokenException(TokenException):
    __EXPIRED_CODE_ERR_MSG = 'Expired access token'

    def _create_exception_message(self) -> str:
        return self.__EXPIRED_CODE_ERR_MSG

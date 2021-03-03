from abc import ABC

from src.api.factory.exceptions import ApplicationException


class UnauthorizedException(ApplicationException, ABC):
    __UNAUTHORIZED_RESPONSE_CODE = 401

    def _create_exception_response_code(self) -> int:
        return self.__UNAUTHORIZED_RESPONSE_CODE


class InvalidAuthorizationException(UnauthorizedException):
    __INVALID_AUTH_ERR_MSG = 'Invalid authorization'

    def _create_exception_message(self) -> str:
        return self.__INVALID_AUTH_ERR_MSG


class MissingAuthorizationException(UnauthorizedException):
    __MISSING_AUTH_ERR_MSG = 'Missing authorization'

    def _create_exception_message(self) -> str:
        return self.__MISSING_AUTH_ERR_MSG

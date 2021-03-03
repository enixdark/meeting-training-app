from abc import ABC

from .. import ApplicationException


class ServiceException(ApplicationException, ABC):
    pass


class ServiceLogicException(ServiceException, ABC):
    __SERVER_ERR_RESPONSE_CODE = 500

    def _create_exception_response_code(self) -> int:
        return self.__SERVER_ERR_RESPONSE_CODE


class ServiceParamsException(ServiceException, ABC):
    __UNPROCESSABLE_ENTITY_RESPONSE_CODE = 422

    def _create_exception_response_code(self) -> int:
        return self.__UNPROCESSABLE_ENTITY_RESPONSE_CODE


class ServiceForbiddenException(ServiceException, ABC):
    __FORBIDDEN_RESPONSE_CODE = 403
    __FORBIDDEN_ERR_MSG = 'Forbidden'

    def _create_exception_response_code(self) -> int:
        return self.__FORBIDDEN_RESPONSE_CODE

    def _create_exception_message(self) -> str:
        return self.__FORBIDDEN_ERR_MSG

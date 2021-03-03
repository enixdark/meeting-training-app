from . import ServiceLogicException


class UnauthenticatedServiceLoginException(ServiceLogicException):
    __ERR_MSG = 'Using invalid authenticated service.'

    def _create_exception_message(self) -> str:
        return self.__ERR_MSG

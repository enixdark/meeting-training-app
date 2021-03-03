from .. import ServiceParamsException


class InvalidUserIdException(ServiceParamsException):
    __INVALID_USER_ERR_MSG = 'Invalid user id'

    def _create_exception_message(self) -> str:
        return self.__INVALID_USER_ERR_MSG

from .. import ServiceParamsException


class InvalidLocationIdException(ServiceParamsException):
    __INVALID_LOCATION_ERR_MSG = 'Invalid location id'

    def _create_exception_message(self) -> str:
        return self.__INVALID_LOCATION_ERR_MSG

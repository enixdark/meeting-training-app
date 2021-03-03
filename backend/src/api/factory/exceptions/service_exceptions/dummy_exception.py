from . import ServiceLogicException


class DummyServiceException(ServiceLogicException):
    def __init__(self, exception: Exception):
        self.__message = str(exception)
        super().__init__()

    def _create_exception_message(self) -> str:
        return self.__message

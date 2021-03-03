from src.api.factory.exceptions import ApplicationException


class EmailException(ApplicationException):
    def __init__(self, exception: Exception):
        self.__email_exception = exception
        super().__init__()

    def _create_exception_message(self) -> str:
        return str(self.__email_exception)

    def _create_exception_response_code(self) -> int:
        return 500

from . import GoogleParamsException


class GoogleEmailException(GoogleParamsException):
    EMAIL_ERR_MSG = 'Invalid email.'

    def _create_exception_message(self) -> str:
        return self.EMAIL_ERR_MSG


class InvalidEmailException(GoogleEmailException):
    EMAIL_ERR_MSG = 'Invalid email'


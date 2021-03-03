from . import GoogleParamsException


class GoogleScopeException(GoogleParamsException):
    SCOPE_ERR_MSG = 'Missing required scopes.'

    def _create_exception_message(self) -> str:
        return self.SCOPE_ERR_MSG


class MissingEmailScopeException(GoogleScopeException):
    SCOPE_ERR_MSG = 'Missing required email scopes.'


class MissingCalendarScopeException(GoogleScopeException):
    SCOPE_ERR_MSG = 'Missing required calendar scopes.'



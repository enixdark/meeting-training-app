from . import ServiceLogicException


class ConnectionException(ServiceLogicException):
    __MAX_RETRIEVE_ERR_MSG = 'Max retries exceeded with Google Oauth2 (v4) token url'

    def _create_exception_message(self) -> str:
        return self.__MAX_RETRIEVE_ERR_MSG

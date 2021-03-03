from .. import ServiceForbiddenException


class InvalidMeetingPermissionException(ServiceForbiddenException):
    __INVALID_MEETING_ERR_MSG = 'Invalid meeting permission.'

    def _create_exception_message(self) -> str:
        return self.__INVALID_MEETING_ERR_MSG


class InvalidCoordinatorException(ServiceForbiddenException):
    __INVALID_MEETING_ERR_MSG = 'Invalid coordinator id.'

    def _create_exception_message(self) -> str:
        return self.__INVALID_MEETING_ERR_MSG

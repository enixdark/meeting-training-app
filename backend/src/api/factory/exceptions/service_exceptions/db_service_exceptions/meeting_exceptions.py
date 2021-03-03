from .. import ServiceParamsException, ServiceForbiddenException


class LocationTimeBoundaryException(ServiceParamsException):
    __LOCATION_TIME_BOUNDARY_ERR_MSG = 'Duplicate with chosen location time boundary'

    def _create_exception_message(self) -> str:
        return self.__LOCATION_TIME_BOUNDARY_ERR_MSG


class InvalidTimeException(ServiceParamsException):
    __INVALID_TIME_ERR_MSG = 'Duplicate with on-going meeting'

    def _create_exception_message(self) -> str:
        return self.__INVALID_TIME_ERR_MSG


class MeetingCoordinatorPermissionException(ServiceForbiddenException):
    __UPDATE_FORBIDDEN_ERR_MSG = 'Update process forbidden. Not a coordinator.'

    def _create_exception_message(self) -> str:
        return self.__UPDATE_FORBIDDEN_ERR_MSG


class InvalidMeetingIdException(ServiceParamsException):
    __INVALID_MEETING_ERR_MSG = 'Invalid meeting id'

    def _create_exception_message(self) -> str:
        return self.__INVALID_MEETING_ERR_MSG


class InvalidPeriodicMeetingException(ServiceParamsException):
    __INVALID_PERIOD_MEETING_ERR_MSG = 'Invalid period meeting.'

    def _create_exception_message(self) -> str:
        return self.__INVALID_PERIOD_MEETING_ERR_MSG

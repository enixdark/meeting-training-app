from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException, MeetingCoordinatorPermissionException
from src.api.factory.exceptions.service_exceptions.google_exceptions.calendar_exceptions import \
    CalendarIdentifierException
from src.api.factory.exceptions.service_exceptions.google_exceptions.token_exceptions import InvalidAccessTokenException
from src.api.factory.libs.google_libs.google_calendar_libs import GoogleCalendarExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.delete_event import DeleteEventExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.maintain_event.insert_event import InsertEventExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.maintain_event.update_event import UpdateEventExecutor
from src.api.pool.services.attendee_services import AttendeeFormService
from src.api.pool.services.meeting_services import MeetingFormService, Meeting
from src.api.pool.services.user_services import UserInstantFormService
from .. import MeetingAuthDecorator


class MeetingSynchronizeDecorator(MeetingAuthDecorator):
    def __init__(self):
        super().__init__()
        self.__refresh_token_count = False

    def update_model(self, meeting_id: int, *args, **kwargs) -> bool:
        meeting_service = MeetingFormService()
        meeting = meeting_service.get_model(_id=meeting_id)
        if not isinstance(meeting, Meeting):
            raise InvalidMeetingIdException()
        if self.__check_coordinator_permission(meeting_id=meeting_id):
            # each time meeting row is updated, the must_synchronized field is set to true
            # -> must synchronized to calendar
            if meeting.must_synchronized:
                # if meeting instance has google_calendar_id, update or delete
                if meeting.google_calendar_id:
                    try:
                        # if meeting state is true, update
                        if meeting.state:
                            google_calendar_executor = UpdateEventExecutor(meeting)
                            self.__request_google_calendar(google_calendar_executor)
                            # after synchronized updated, prevent other redundant synchronizations
                            meeting_service.update_model(_id=meeting_id, must_synchronized=False)
                        # if meeting state is false, delete
                        else:
                            google_calendar_executor = DeleteEventExecutor(meeting)
                            self.__request_google_calendar(google_calendar_executor)
                            meeting_service.update_model(_id=meeting_id, google_calendar_id=None)
                    except CalendarIdentifierException as ce:
                        # if error happened because of calendar_id, remove it
                        # (mostly because of illegal activities on google_calendar_id on db or manually delete event on
                        # Google Calendar server)
                        meeting_service.update_model(_id=meeting_id, google_calendar_id=None)
                        self.commit()
                        raise ce
                else:
                    # if meeting instance has no google_calendar_id, create
                    google_calendar_executor = InsertEventExecutor(meeting)
                    calendar_response = self.__request_google_calendar(google_calendar_executor)

                    meeting_service.update_model(_id=meeting_id,
                                                 must_synchronized=False,
                                                 google_calendar_id=calendar_response['id'])
                self.commit()
                return True

            return False
        else:
            raise MeetingCoordinatorPermissionException()

    def __request_google_calendar(self, calendar_executor: GoogleCalendarExecutor, access_token=None) -> dict:
        """
        Execute service, after check if is invalid access token to refresh a new one.
        :param calendar_executor:
        :return:
        """
        if access_token is None:
            auth_user = self.get_authenticated_user()
            access_token = auth_user.access_token
        try:
            google_response = calendar_executor.execute(access_token=access_token)
            return google_response.data
        except InvalidAccessTokenException as ie:
            # only refresh access_token once
            if not self.__refresh_token_count:
                return self.__refresh_access_token(calendar_executor)
            else:
                # if it's raised, require a new refresh_token (require login again).
                raise ie

    def __refresh_access_token(self, calendar_executor: GoogleCalendarExecutor) -> dict:
        """
        Refresh access token
        :param calendar_executor: Every GoogleService have a refresh token method
        :return:
        """
        auth_user = self.get_authenticated_user()
        refresh_token = auth_user.refresh_token

        new_access_token = calendar_executor.refresh_access_token(refresh_token=refresh_token)
        user_service = UserInstantFormService()
        user_service.update_model(_id=auth_user.id, access_token=new_access_token)

        # prevent infinite recursion call
        self.__refresh_token_count = True

        return self.__request_google_calendar(calendar_executor=calendar_executor,
                                              access_token=new_access_token)

    def __check_coordinator_permission(self, meeting_id: int):
        """
        Check coordinator permission. Only coordinator can synchronize
        :param meeting_id: meeting_id to find coordinator
        :return:True if self.auth_user is coordinator, otherwise, return False
        """
        attendee_service = AttendeeFormService()
        auth_user = self.get_authenticated_user()

        coordinator = attendee_service.get_meeting_coordinator(meeting_id=meeting_id)
        if coordinator.user_id == auth_user.id:
            return True
        return False

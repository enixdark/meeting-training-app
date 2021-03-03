from abc import abstractmethod

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.factory.exceptions.service_exceptions.google_exceptions.token_exceptions import InvalidAccessTokenException
from src.api.factory.libs.google_libs.google_calendar_libs import GoogleCalendarExecutor
from src.api.pool.services.meeting_services import MeetingFormService
from src.api.pool.services.user_services import UserInstantFormService
from src.database.postgres.meeting import Meeting
from src.message_queue.tasks.authenticated_task import AuthenticatedTask
from ..db_connection_task import BaseService


class BaseCalendarTask(AuthenticatedTask):
    calendar_executor = None
    meeting_id = 0
    refresh_token_count = False

    def run(self, meeting_id, user_id, *args, **kwargs):
        # init attributes
        print('Calendar task - {} is running!'.format(type(self).__name__))
        self.auth_user = self._retrieve_authenticated_user(user_id)
        self.meeting_id = meeting_id
        self.calendar_executor = self._create_calendar_executor()
        request_response = self._on_calendar_request()
        self._after_calendar_request(request_response)
        self.close_session()

    @abstractmethod
    def _create_calendar_executor(self) -> GoogleCalendarExecutor:
        pass

    @abstractmethod
    def _after_calendar_request(self, executed_response: dict):
        pass

    def _on_calendar_request(self) -> dict:
        return self._request_google_calendar()

    def _create_service(self) -> BaseService:
        return MeetingFormService()

    def _get_meeting(self) -> Meeting:
        meeting = self._prepared_service().get_model(_id=self.meeting_id)
        if isinstance(meeting, Meeting):
            return meeting
        else:
            raise InvalidMeetingIdException()

    def _request_google_calendar(self, access_token=None) -> dict:
        if access_token is None:
            access_token = self.auth_user.access_token
        try:
            google_response = self.calendar_executor.execute(access_token=access_token)
            return google_response.data
        except InvalidAccessTokenException as ie:
            # only refresh access_token once
            if not self.refresh_token_count:
                return self.__refresh_access_token(self.calendar_executor)
            else:
                # if it's raised, require a new refresh_token (require login again).
                raise ie

    def __refresh_access_token(self, calendar_executor: GoogleCalendarExecutor) -> dict:
        refresh_token = self.auth_user.refresh_token

        new_access_token = calendar_executor.refresh_access_token(refresh_token=refresh_token)
        user_service = self._prepared_service(base_service=UserInstantFormService())
        user_service.update_model(_id=self.auth_user.id, access_token=new_access_token)

        # prevent infinite recursion call
        self.__refresh_token_count = True

        return self._request_google_calendar(access_token=new_access_token)

from abc import abstractmethod

from src.api.factory.exceptions.service_exceptions.google_exceptions import GoogleBackendError, GoogleException
from src.api.factory.exceptions.service_exceptions.google_exceptions.calendar_exceptions import \
    CalendarForbiddenException, CalendarParamsException
from src.api.factory.exceptions.service_exceptions.google_exceptions.token_exceptions import InvalidAccessTokenException
from src.database.postgres.meeting import Meeting
from .. import BaseGoogleExecutor, GoogleResponse


class GoogleCalendarExecutor(BaseGoogleExecutor):
    __GOOGLE_CALENDAR_URL = 'https://www.googleapis.com/calendar/v3/calendars/'

    def __init__(self, meeting: Meeting):
        super(GoogleCalendarExecutor, self).__init__()
        self._calendar_id = 'primary'
        self._meeting = meeting

    def execute(self, access_token: str, *args, **kwargs) -> GoogleResponse:
        # retrieve meeting model data for request
        executed_event = self._retrieve_meeting_data(meeting=self._meeting)
        # send request to google calendar and parse json response to dict
        executed_event_response = self._send_request(meeting_data=executed_event, access_token=access_token)

        # handle google errors
        error = executed_event_response.get('error', None)
        if error:
            code = error['code']
            error_codes = self._create_error_codes(error['message'])
            google_exception = error_codes.get(str(code), GoogleException(message=error['message'], code=422))
            raise google_exception

        return self._create_response(executed_event_response, True)

    def build_calendar_service(self, calendar_id: str) -> 'GoogleCalendarExecutor':
        """
        Create a calendar service instance with specific calendar id.
        :param calendar_id: Google calendar id.
        :return: GoogleCalendarService.
        """
        self._calendar_id = calendar_id
        return self

    def _build_calendar_url(self) -> str:
        return self.__GOOGLE_CALENDAR_URL + self._create_action_endpoint()

    @staticmethod
    def _create_error_codes(error_message: str) -> dict:
        """
        Create service's Google errors list
        :param error_message:
        :return:
        """
        return {
            '401': InvalidAccessTokenException(),
            '403': CalendarForbiddenException(message=error_message),
            '412': CalendarParamsException(message=error_message),
            '500': GoogleBackendError()
        }

    @abstractmethod
    def _create_action_endpoint(self) -> str:
        """
        Create service's endpoint
        :return
        """
        pass

    @abstractmethod
    def _retrieve_meeting_data(self, meeting: Meeting) -> dict:
        """
        Retrieve meeting model data for request.
        :param meeting: Meeting model for retrieve data.
        :return: a dictionary contains necessary data for service to send request.
        """
        pass

    @abstractmethod
    def _send_request(self, meeting_data: dict, access_token: str) -> dict:
        """
        Send request to google calendar and parse json response to dict.
        :param meeting_data: Meeting data to send request.
        :param access_token: Google access token.
        :return: A dictionary contains Google Calendar response.
        """
        pass

import json

import requests

from src.api.factory.exceptions.service_exceptions.google_exceptions.calendar_exceptions import \
    CalendarIdentifierException
from src.database.postgres.meeting import Meeting
from . import GoogleCalendarExecutor


class DeleteEventExecutor(GoogleCalendarExecutor):
    def _create_action_endpoint(self) -> str:
        return self._calendar_id + '/events/' + self._meeting.google_calendar_id

    def _retrieve_meeting_data(self, meeting: Meeting) -> dict:
        return {}

    def _send_request(self, meeting_data: dict, access_token: str) -> dict:
        if self._meeting.google_calendar_id:
            response = requests.delete(url=self._build_calendar_url(), params={'access_token': access_token})
            # if success, Google Calendar API returns an empty body.
            if response.status_code == 204:
                return {}
            return json.loads(response.content.decode())
        # 404 response code also returns no body
        return {'error': {
            'code': 404,
            'message': 'Not Found.'
        }}

    def _create_error_codes(self, error_message: str) -> dict:
        return {
            **super(DeleteEventExecutor, self)._create_error_codes(error_message),
            '404': CalendarIdentifierException(message='Not found.', code=404),
            '410': CalendarIdentifierException(message='Resource has been deleted.', code=410),
        }

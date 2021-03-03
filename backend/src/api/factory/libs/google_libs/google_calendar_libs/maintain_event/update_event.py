import json

import requests

from src.api.factory.exceptions.service_exceptions.google_exceptions.calendar_exceptions import CalendarParamsException, \
    CalendarIdentifierException
from . import MaintainEventExecutor


class UpdateEventExecutor(MaintainEventExecutor):
    def _create_action_endpoint(self) -> str:
        return self._calendar_id + '/events/' + self._meeting.google_calendar_id

    def _send_request(self, meeting_data: dict, access_token: str) -> dict:
        if self._meeting.google_calendar_id:
            response = requests.put(
                **self._build_maintained_request(meeting_data=meeting_data, access_token=access_token))
            return json.loads(response.content.decode())
        # 404 not found returns empty body
        return {'error': {
            'code': 404,
            'message': 'Not Found.'
        }}

    def _create_error_codes(self, error_message: str) -> dict:
        return {
            **super(UpdateEventExecutor, self)._create_error_codes(error_message),
            '404': CalendarIdentifierException(message='Not found.', code=404),
            '409': CalendarParamsException(message=error_message),
        }

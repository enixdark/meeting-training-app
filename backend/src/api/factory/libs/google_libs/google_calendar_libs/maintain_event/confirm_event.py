import json

import requests

from src.database.postgres.meeting import Meeting
from .update_event import UpdateEventExecutor


class ConfirmEventExecutor(UpdateEventExecutor):
    def _retrieve_meeting_data(self, meeting: Meeting) -> dict:
        """
        Build meeting dictionary for post or put.
        :param meeting: Meeting model for retrieve data.
        :return: a dictionary contains necessary data for service to send request.
        """

        event = {
            'attendees': self._build_attendees(meeting),
        }
        return event

    def _send_request(self, meeting_data: dict, access_token: str) -> dict:
        if self._meeting.google_calendar_id:
            response = requests.patch(
                **self._build_maintained_request(meeting_data=meeting_data, access_token=access_token))
            return json.loads(response.content.decode())
        # 404 not found returns empty body
        return {'error': {
            'code': 404,
            'message': 'Not Found.'
        }}

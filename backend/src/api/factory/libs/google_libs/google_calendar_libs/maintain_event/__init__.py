import json
from abc import ABC

from src.api.factory.libs.google_libs.google_calendar_libs.maintain_event.attendee_states.switcher import \
    AttendeeStateSwitcher
from src.database.postgres.meeting import Meeting
from .. import GoogleCalendarExecutor


class MaintainEventExecutor(GoogleCalendarExecutor, ABC):
    def __init__(self, meeting: Meeting):
        super(MaintainEventExecutor, self).__init__(meeting)
        self.__attendee_state_switcher = AttendeeStateSwitcher()

    def _retrieve_meeting_data(self, meeting: Meeting) -> dict:
        """
        Build meeting dictionary for post or put.
        :param meeting: Meeting model for retrieve data.
        :return: a dictionary contains necessary data for service to send request.
        """
        meeting_dict = meeting.serialize(inclusion_rs=['location', 'attendees'])
        meeting_location = meeting_dict['location']

        event = {
            'summary': meeting_dict['name'],
            'location': '{location_name} - {location_address}'.format(
                location_name=meeting_location['name'],
                location_address=meeting_location['address']),
            'description': meeting_dict['description'],
            'start': {
                'dateTime': meeting_dict['started_time'],
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'end': {
                'dateTime': meeting_dict['finished_time'],
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'attendees': self._build_attendees(meeting),
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            }
        }
        return event

    def _build_maintained_request(self, meeting_data: dict, access_token):
        """
        Build an common request information for a maintained request.
        (Note that calendar event must contain header: Content-Type)
        :param meeting_data:
        :param access_token:
        :return:
        """
        return {
            'url': self._build_calendar_url(),
            'headers': {
                'Content-Type': 'application/json'
            },
            'params': {
                'access_token': access_token
            },
            'data': json.dumps(meeting_data)
        }

    def _build_attendees(self, meeting: Meeting) -> list:
        attendees = []
        for associated_user in meeting.associate_users:
            attendee = dict()
            attendee['email'] = associated_user.user.email
            attendee['responseStatus'] = self.__attendee_state_switcher.get_state(associated_user.is_accepted,
                                                                                  associated_user.may_join)
            attendees.append(attendee)
        return attendees

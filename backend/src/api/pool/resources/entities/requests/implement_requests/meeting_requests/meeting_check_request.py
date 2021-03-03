from . import MeetingGetRequest, GetSchema
from .meeting_schemas.meeting_check_schemas import MeetingCheckSchema


class MeetingCheckRequest(MeetingGetRequest):
    def filter_rules(self) -> dict:
        date = self._get_date()
        if date:
            return {
                'location_id': self._get_location_id(),
                'include_meeting': self._get_include_meeting(),
                'date': date
            }
        return {
            'location_id': self._get_location_id(),
            'include_meeting': self._get_include_meeting()
        }

    def _create_schema(self) -> GetSchema:
        return MeetingCheckSchema()

    def _get_location_id(self):
        return self._get_url_parameter('location_id')

    def _get_date(self):
        return self._get_url_parameter('date')

    def _get_include_meeting(self):
        is_include = self._get_url_parameter('include_meeting')
        if is_include == 'true':
            return True
        return False

    def __get_limit(self):
        limit = self._get_url_parameter('limit')
        if limit:
            return limit
        return 30

from datetime import datetime

from . import MeetingGetRequest, GetSchema
from .meeting_schemas.meeting_check_schemas import MeetingListSchema


class MeetingListRequest(MeetingGetRequest):
    def filter_rules(self) -> dict:
        return {
            'location_id': self._get_location_id(),
            'date': self._get_date()
        }

    def _create_schema(self) -> GetSchema:
        return MeetingListSchema()

    def _get_location_id(self):
        location_id = self._get_url_parameter('location_id')
        if location_id:
            return location_id
        return 0

    def _get_date(self):
        date = self._get_url_parameter('date')
        if date:
            return date
        return datetime.now().date().isoformat()

    def __get_limit(self):
        limit = self._get_url_parameter('limit')
        if limit:
            return limit
        return 30

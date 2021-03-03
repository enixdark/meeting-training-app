from datetime import datetime, timedelta

from config import BaseApiConfig
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests import MeetingGetRequest, GetSchema
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_schemas.meeting_search_schema import \
    MeetingSearchSchema


class MeetingSearchRequest(MeetingGetRequest):
    _NOW = datetime.now() + timedelta(hours=BaseApiConfig.TIME_DIFFERENCE)

    def _create_schema(self) -> GetSchema:
        return MeetingSearchSchema()

    def filter_rules(self) -> dict:
        return {
            **super(MeetingSearchRequest, self).filter_rules(),
            'q': self._get_query(),
            'le': self._get_finished_time_pivot(),
            'ge': self._get_started_time_pivot()
        }

    def _get_query(self) -> str:
        return self._get_url_parameter('q')

    def _get_started_time_pivot(self):
        ge = self._get_url_parameter('ge')
        if not ge:
            ge = str(self._NOW.date() - timedelta(days=7))
        return ge

    def _get_finished_time_pivot(self):
        le = self._get_url_parameter('le')
        if not le:
            le = str(self._NOW.date() + timedelta(days=7))
        return le

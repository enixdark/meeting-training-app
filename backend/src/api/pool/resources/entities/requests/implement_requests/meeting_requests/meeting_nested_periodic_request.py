from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_schemas.meeting_nested_schema import \
    MeetingNestedPostSchema
from .meeting_nested_requests import MeetingNestedPostRequest, NestedSchema
from .meeting_schemas.meeting_periodic_nested_post_schema import MeetingPeriodicNestedPostSchema


class MeetingPeriodicNestedPostRequest(MeetingNestedPostRequest):
    def _create_schema(self) -> NestedSchema:
        return MeetingPeriodicNestedPostSchema()

    def _get_raw_data(self) -> dict:
        raw_data = super(MeetingPeriodicNestedPostRequest, self)._get_raw_data()
        periodic = self.__get_periodic()
        if not periodic:
            self._set_schema(MeetingNestedPostSchema())
            return super(MeetingPeriodicNestedPostRequest, self)._get_raw_data()
        return {
            **raw_data,
            'periodic': periodic
        }

    def __get_periodic(self) -> bool:
        periodic = self._get_url_parameter('periodic')
        return periodic == 'true'

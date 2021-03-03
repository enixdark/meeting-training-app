from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_schemas.meeting_periodic_nested_patch_schema import \
    MeetingPeriodicNestedPatchSchema
from .meeting_nested_requests import MeetingNestedPatchRequest, NestedSchema


class MeetingNestedPeriodicApprovalRequest(MeetingNestedPatchRequest):
    def _create_schema(self) -> NestedSchema:
        return MeetingPeriodicNestedPatchSchema()

    def _get_raw_data(self) -> dict:
        raw_data = super(MeetingNestedPeriodicApprovalRequest, self)._get_raw_data()
        periodic = self.__get_periodic()
        return {
            **raw_data,
            'periodic': periodic
        }

    def __get_periodic(self) -> bool:
        periodic = self._get_url_parameter('periodic')
        return periodic == 'true'

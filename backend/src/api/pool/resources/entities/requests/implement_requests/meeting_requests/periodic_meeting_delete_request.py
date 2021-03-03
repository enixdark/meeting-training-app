from src.api.pool.resources.entities.requests.base_requests.schema_requests.base_modified_requests.delete_request import \
    DeleteRequest, DeleteSchema
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_schemas.meeting_periodic_delete_schema import \
    MeetingPeriodicDeleteSchema


class PeriodicMeetingDeleteRequest(DeleteRequest):
    def _create_schema(self) -> DeleteSchema:
        return MeetingPeriodicDeleteSchema()
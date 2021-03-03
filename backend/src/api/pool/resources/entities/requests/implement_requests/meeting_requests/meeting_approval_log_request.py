from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_schemas.meeting_approval_log_schema import \
    MeetingApprovalLogSchema
from . import MeetingGetRequest, GetSchema


class MeetingApprovalLogRequest(MeetingGetRequest):
    def _create_schema(self) -> GetSchema:
        return MeetingApprovalLogSchema()
from .meeting_schemas.meeting_periodic_patch_schema import MeetingPeriodicPatchSchema
from . import MeetingPatchRequest, Schema


class PeriodicMeetingPatchRequest(MeetingPatchRequest):
    def _create_schema(self) -> Schema:
        return MeetingPeriodicPatchSchema()

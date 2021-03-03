from marshmallow import Schema

from .attendee_schema.attendee_coordinator_schema import AttendeeCoordinatorSchema
from ...base_requests.schema_requests.base_modified_requests.patch_request import PatchRequest


class AttendeeCoordinatorRequest(PatchRequest):
    def _create_schema(self) -> Schema:
        return AttendeeCoordinatorSchema()

    def _get_raw_data(self) -> dict:
        return {
            **super()._get_raw_data(),
            'meeting_id': self._get_url_parameter('meeting_id')
        }

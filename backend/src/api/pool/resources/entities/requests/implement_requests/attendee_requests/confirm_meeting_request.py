from marshmallow import Schema

from .attendee_schema.attendee_confirm_schema import AttendeeConfirmSchema
from ...base_requests.schema_requests.base_modified_requests.post_request import PostRequest


class  AttendeeConfirmRequest(PostRequest):
    def _create_schema(self) -> Schema:
        return AttendeeConfirmSchema()

    def _get_raw_data(self) -> dict:
        raw = super()._get_raw_data()
        if not isinstance(raw, dict):
            raw = {}
        return {
            **raw,
            'meeting_id': self._get_url_parameter('meeting_id')
        }

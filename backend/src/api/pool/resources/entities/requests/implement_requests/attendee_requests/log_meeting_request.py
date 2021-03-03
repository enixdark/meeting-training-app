from marshmallow import Schema

from .attendee_schema.attendee_log_schema import AttendeeLogSchema
from ...base_requests.schema_requests.base_get_requests.get_request import GetRequest


class AttendeeLogRequest(GetRequest):
    def filter_rules(self) -> dict:
        return {}

    def _create_schema(self) -> Schema:
        return AttendeeLogSchema()

from marshmallow import fields

from src.api.pool.resources.entities.requests.implement_requests.meeting_requests.meeting_schemas.meeting_nested_schema import \
    MeetingNestedPatchSchema


class MeetingPeriodicNestedPatchSchema(MeetingNestedPatchSchema):
    periodic = fields.Boolean()

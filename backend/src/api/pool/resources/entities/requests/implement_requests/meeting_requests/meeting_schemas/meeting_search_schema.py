from marshmallow import fields

from src.api.pool.resources.entities.requests.base_requests.schemas.common_schemas.common_strings.normal_string import \
    NormalString
from src.api.pool.resources.entities.requests.implement_requests.meeting_requests import MeetingGetSchema


class MeetingSearchSchema(MeetingGetSchema):
    q = NormalString(required=True)
    le = fields.Date()
    ge = fields.Date()

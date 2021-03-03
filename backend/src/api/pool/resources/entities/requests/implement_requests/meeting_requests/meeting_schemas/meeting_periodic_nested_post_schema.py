from src.api.pool.resources.entities.requests.base_requests.schemas.common_schemas.common_lists.periodic_meeting_created_list import \
    PeriodicMeetingCreatedList
from src.api.pool.resources.entities.requests.base_requests.schemas.nested_schemas import NestedSchema
from .meeting_nested_schema import fields
from .meeting_periodic_post_schema import MeetingPeriodicPostSchema


class MeetingPeriodicNestedPostSchema(NestedSchema):
    periodic = fields.Boolean()
    nested = PeriodicMeetingCreatedList(fields.Nested(MeetingPeriodicPostSchema))

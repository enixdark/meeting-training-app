from . import fields, MeetingPostSchema, MeetingPatchSchema, MeetingDeleteSchema
from ....base_requests.schemas.nested_schemas import NestedSchema


class MeetingNestedPostSchema(NestedSchema):
    nested = fields.List(fields.Nested(MeetingPostSchema))


class MeetingNestedPatchSchema(NestedSchema):
    nested = fields.List(fields.Nested(MeetingPatchSchema))


class MeetingNestedDeleteSchema(NestedSchema):
    nested = fields.List(fields.Nested(MeetingDeleteSchema))

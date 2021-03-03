from marshmallow import fields

from ....base_requests.schemas import BaseSchema
from ....base_requests.schemas.common_schemas.common_strings.long_string import LongString
from ....base_requests.schemas.common_schemas.common_strings.normal_string import NormalString
from ....base_requests.schemas.get_schema import GetSchema
from ....base_requests.schemas.patch_schema import PatchSchema


class LocationPostSchema(BaseSchema):
    name = NormalString(required=True)
    is_multi_access = fields.Boolean(default=True)
    opened_time = fields.Time(required=True)
    closed_time = fields.Time(required=True)
    address = LongString(required=True)
    google_map_id = NormalString()


class LocationPatchSchema(PatchSchema):
    name = NormalString()
    is_multi_access = fields.Boolean()
    opened_time = fields.Time()
    closed_time = fields.Time()
    address = LongString()
    google_map_id = NormalString()


class LocationGetSchema(GetSchema):
    @staticmethod
    def sort_rule() -> list:
        return ['id']

    @staticmethod
    def relation_rule() -> list:
        return ['meetings']

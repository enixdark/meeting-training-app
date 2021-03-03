from marshmallow import Schema

from .meeting_schemas import MeetingGetSchema, MeetingPatchSchema
from ...base_requests.schema_requests.base_get_requests.get_request import GetRequest
from ...base_requests.schema_requests.base_modified_requests.patch_request import PatchRequest
from ...base_requests.schemas.get_schema import GetSchema


class MeetingGetRequest(GetRequest):
    def _create_schema(self) -> GetSchema:
        return MeetingGetSchema()

    def filter_rules(self) -> dict:
        return {}


class MeetingPatchRequest(PatchRequest):
    def _create_schema(self) -> Schema:
        return MeetingPatchSchema()

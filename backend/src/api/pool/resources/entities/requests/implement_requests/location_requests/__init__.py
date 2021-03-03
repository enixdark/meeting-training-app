from marshmallow import Schema

from ...base_requests.schema_requests.base_get_requests.get_request import GetRequest
from ...base_requests.schema_requests.base_modified_requests.patch_request import PatchRequest
from ...base_requests.schema_requests.base_modified_requests.post_request import PostRequest
from ...base_requests.schemas.get_schema import GetSchema
from .location_schemas import LocationGetSchema, LocationPostSchema, LocationPatchSchema


class LocationGetRequest(GetRequest):
    def _create_schema(self) -> GetSchema:
        return LocationGetSchema()

    def filter_rules(self) -> dict:
        return {}


class LocationPostRequest(PostRequest):
    def _create_schema(self) -> Schema:
        return LocationPostSchema()


class LocationPatchRequest(PatchRequest):
    def _create_schema(self) -> Schema:
        return LocationPatchSchema()

from marshmallow import Schema

from .user_schemas import TokenLoginSchema, UserGetSchema, CodeLoginSchema
from ...base_requests.schema_requests.base_get_requests.get_request import GetRequest
from ...base_requests.schema_requests.base_modified_requests.post_request import PostRequest
from ...base_requests.schemas.get_schema import GetSchema


class TokenLoginRequest(PostRequest):
    def _create_schema(self) -> Schema:
        return TokenLoginSchema()


class UserGetRequest(GetRequest):
    def _create_schema(self) -> GetSchema:
        return UserGetSchema()

    def filter_rules(self) -> dict:
        return {}


class CodeLoginRequest(PostRequest):
    def _create_schema(self) -> Schema:
        return CodeLoginSchema()

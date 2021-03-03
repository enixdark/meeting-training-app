from ...base_requests.schema_requests.base_get_requests.get_request import GetRequest
from ...base_requests.schemas.get_schema import BaseSchema, GetSchema


class HealthGetRequest(GetRequest):
    def _create_schema(self) -> GetSchema:
        return BaseSchema()

    def filter_rules(self) -> dict:
        return {}

from .meeting_schemas.meeting_nested_schema import MeetingNestedPostSchema, MeetingNestedPatchSchema, \
    MeetingNestedDeleteSchema
from ...base_requests.schema_requests.base_nested_requests import NestedPostRequest, NestedPatchRequest, \
    NestedDeleteRequest
from ...base_requests.schemas.nested_schemas import NestedSchema


class MeetingNestedPostRequest(NestedPostRequest):
    def _create_schema(self) -> NestedSchema:
        return MeetingNestedPostSchema()

    def _get_raw_data(self) -> dict:
        creator = self.get_authentication()
        creator_id = creator['id']
        raw_data = super()._get_raw_data()
        try:
            nested_meetings = raw_data['nested']
            for meeting in nested_meetings:
                meeting['creator_id'] = creator_id
            else:
                raw_data['nested'] = nested_meetings
                return raw_data
        except KeyError:
            return {}


class MeetingNestedPatchRequest(NestedPatchRequest):
    def _create_schema(self) -> NestedSchema:
        return MeetingNestedPatchSchema()


class MeetingNestedDeleteRequest(NestedDeleteRequest):
    def _create_schema(self) -> NestedSchema:
        return MeetingNestedDeleteSchema()

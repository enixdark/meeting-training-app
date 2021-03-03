from marshmallow import Schema

from .meeting_schemas import MeetingPatchSchema
from ...base_requests.schema_requests.base_modified_requests.patch_request import PatchRequest


class MeetingSynchronizedRequest(PatchRequest):
    def _create_schema(self) -> Schema:
        return MeetingPatchSchema()

    def _get_raw_data(self) -> dict:
        return {
            # **super()._get_raw_data(),
            'id': self._get_url_parameter('id')
        }

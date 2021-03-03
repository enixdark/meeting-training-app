from ....base_requests.schemas import BaseSchema
from ....base_requests.schemas.common_schemas.common_unsigned_integer.unsigned_integer import UnsignedInteger


class AttendeeCoordinatorSchema(BaseSchema):
    coordinator_id = UnsignedInteger(required=True)
    meeting_id = UnsignedInteger(required=True)

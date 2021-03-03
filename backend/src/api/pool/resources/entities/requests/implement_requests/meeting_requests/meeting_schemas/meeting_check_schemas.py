from . import MeetingGetSchema, fields, UnsignedInteger
from ....base_requests.schemas.common_schemas.common_dates.checked_date import CheckedDate
from ....base_requests.schemas.common_schemas.common_dates.listed_date import ListedDate


class MeetingListSchema(MeetingGetSchema):
    location_id = UnsignedInteger(validate=lambda n: n >= 0)
    date = ListedDate()


class MeetingCheckSchema(MeetingGetSchema):
    location_id = UnsignedInteger(required=True, validate=lambda n: n >= 0)
    include_meeting = fields.Boolean()
    date = CheckedDate()

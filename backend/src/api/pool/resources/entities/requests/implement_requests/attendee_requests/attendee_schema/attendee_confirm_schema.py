from marshmallow import validates, ValidationError, fields

from ....base_requests.schemas import BaseSchema
from ....base_requests.schemas.common_schemas.common_strings.short_string import ShortString
from ....base_requests.schemas.common_schemas.common_unsigned_integer.unsigned_integer import UnsignedInteger


class AttendeeConfirmSchema(BaseSchema):
    confirm_status = ShortString(required=True)
    meeting_id = UnsignedInteger(required=True)
    note = fields.String(200)

    @validates('confirm_status')
    def _validate_confirm_status(self, confirm_status):
        confirm_status_rules = ['affirmative', 'uncertain', 'negative']
        if confirm_status not in confirm_status_rules:
            raise ValidationError('Invalid confirm status.')

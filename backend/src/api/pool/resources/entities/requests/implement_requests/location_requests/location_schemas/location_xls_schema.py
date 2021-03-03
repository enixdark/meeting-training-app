from src.api.pool.resources.entities.requests.base_requests.schemas import BaseSchema
from src.api.pool.resources.entities.requests.base_requests.schemas.common_schemas.common_unsigned_integer.unsigned_integer import \
    UnsignedInteger
from src.api.pool.resources.entities.requests.base_requests.schemas.nested_schemas import NestedSchema
from marshmallow import fields, validates_schema, ValidationError


class LocationXLSSchema(BaseSchema):
    id = UnsignedInteger(required=True)


class NestedLocationXLSSchema(NestedSchema):
    from_date = fields.Date()
    to_date = fields.Date()
    nested = fields.List(fields.Nested(LocationXLSSchema))

    @validates_schema
    def validate_time_order(self, data, **kwargs):
        errors = {}
        from_date = data.get('from_date', None)
        to_date = data.get('to_date', None)
        if from_date and to_date:
            if from_date >= to_date:
                errors['time_order'] = 'ge be greater than le.'
            days = (to_date - from_date).days
            if days > 256:
                errors['date_order'] = 'le and ge must less than 256.'
            if errors:
                raise ValidationError(errors)

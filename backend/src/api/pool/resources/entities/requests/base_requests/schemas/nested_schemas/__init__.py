from marshmallow import ValidationError, validates_schema

from .. import BaseSchema


class NestedSchema(BaseSchema):
    @validates_schema
    def validate_list(self, data, **kwargs):
        nested = data.get('nested', None)
        if not nested:
            raise ValidationError('Missing list data')

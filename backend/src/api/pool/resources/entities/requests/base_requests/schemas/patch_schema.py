from .common_schemas.common_unsigned_integer.unsigned_integer import UnsignedInteger
from . import BaseSchema


class PatchSchema(BaseSchema):
    id = UnsignedInteger()

    @staticmethod
    def _create_required_attributes() -> list:
        return ['id']

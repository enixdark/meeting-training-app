from abc import ABC, abstractmethod

from marshmallow import fields

from .. import AdditionField, SchemaValidator


class UnsignedIntegerValidator(SchemaValidator, ABC):
    @abstractmethod
    def _do_validate(self, validated_integer: int) -> bool:
        pass


class CommonUnsignedInteger(fields.Integer, AdditionField):
    def _validate(self, value):
        super()._validate(value)
        self._validate_additions(value)

    def _create_addition_validators(self) -> list:
        return [
            *self._unsigned_integer_filter_rules(),
            GreaterThanZeroValidator
        ]

    @staticmethod
    def _unsigned_integer_filter_rules() -> list:
        return []


class GreaterThanZeroValidator(UnsignedIntegerValidator):
    __ERR_MSG = 'Must be greater than or equal to 0.'

    def _do_validate(self, validated_integer: int) -> bool:
        return validated_integer >= 0

    def _create_error_message(self) -> str:
        return self.__ERR_MSG

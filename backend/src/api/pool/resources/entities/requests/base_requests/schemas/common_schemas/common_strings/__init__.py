from abc import ABC, abstractmethod

from marshmallow import fields

from .. import AdditionField, SchemaValidator


class CommonString(fields.String, AdditionField):
    def _validate(self, value):
        super()._validate(value)
        self._validate_additions(value)

    def _create_addition_validators(self) -> list:
        return [
            *self._string_filter_rules(),
            EmptyValidator
        ]

    @staticmethod
    def _string_filter_rules() -> list:
        return []


class StringValidator(SchemaValidator, ABC):
    @abstractmethod
    def _do_validate(self, validated_str: str) -> bool:
        pass


class EmptyValidator(StringValidator):
    __ERR_MSG = 'String must not be null.'

    def _do_validate(self, validated_str: str) -> bool:
        return len(validated_str) > 0

    def _create_error_message(self) -> str:
        return self.__ERR_MSG

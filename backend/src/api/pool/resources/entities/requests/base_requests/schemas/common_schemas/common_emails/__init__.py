from abc import ABC, abstractmethod

from marshmallow import fields

from .. import AdditionField, SchemaValidator


class CommonEmail(fields.Email, AdditionField):
    def _validate(self, value):
        super()._validate(value)
        self._validate_additions(value)

    def _create_addition_validators(self) -> list:
        return [
            *self._email_filter_rules()
        ]

    @staticmethod
    def _email_filter_rules() -> list:
        return []


class EmailValidator(SchemaValidator, ABC):
    @abstractmethod
    def _do_validate(self, validated_email: str) -> bool:
        pass

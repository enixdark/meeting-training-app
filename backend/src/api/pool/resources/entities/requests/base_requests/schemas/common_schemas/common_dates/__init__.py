from abc import ABC, abstractmethod
from datetime import datetime

from marshmallow import fields

from .. import AdditionField, SchemaValidator


class CommonDate(fields.Date, AdditionField):
    def _validate(self, value):
        super()._validate(value)
        self._validate_additions(value)

    def _create_addition_validators(self) -> list:
        return [
            *self._date_filter_rules(),
            DateFormatValidator
        ]

    @staticmethod
    def _date_filter_rules() -> list:
        return []


class DateValidator(SchemaValidator, ABC):
    @abstractmethod
    def _do_validate(self, validated_date: datetime.date) -> bool:
        pass


class DateFormatValidator(DateValidator):
    __DATE_PATTERN = '%Y-%m-%d'
    __ERR_MSG = 'Invalid format. Must be Y-m-d.'

    def _do_validate(self, validated_date: datetime.date) -> bool:
        if validated_date:
            try:
                datetime.strptime(validated_date.isoformat(), self.__DATE_PATTERN)
            except ValueError:
                return False
        return True

    def _create_error_message(self) -> str:
        return self.__ERR_MSG

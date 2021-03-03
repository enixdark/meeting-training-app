from abc import ABC, abstractmethod
from datetime import datetime

from marshmallow import fields
from .. import AdditionField, SchemaValidator


class CommonDatetime(fields.DateTime, AdditionField):
    def _validate(self, value):
        super()._validate(value)
        self._validate_additions(value)

    def _create_addition_validators(self) -> list:
        return [
            *self._datetime_filter_rules(),
            ISOFormatValidator, SecondValidator, MinuteValidator
        ]

    @staticmethod
    def _datetime_filter_rules() -> list:
        return []


class DateTimeValidator(SchemaValidator, ABC):
    @abstractmethod
    def _do_validate(self, validated_datetime: datetime) -> bool:
        pass


class ISOFormatValidator(DateTimeValidator):
    __DATETIME_PATTERN = '%Y-%m-%dT%H:%M:%S'
    __ERR_MSG = 'Invalid format. Must be ISO-8601 format without millisecond.'

    def _do_validate(self, validated_datetime: datetime) -> bool:
        if validated_datetime:
            try:
                datetime.strptime(validated_datetime.isoformat(), self.__DATETIME_PATTERN)
            except ValueError:
                return False
        return True

    def _create_error_message(self) -> str:
        return self.__ERR_MSG


class SecondValidator(DateTimeValidator):
    __ERR_MSG = 'Invalid second format. Must be 00.'

    def _do_validate(self, validated_datetime: datetime) -> bool:
        return validated_datetime.second == 0

    def _create_error_message(self) -> str:
        return self.__ERR_MSG


class MinuteValidator(DateTimeValidator):
    __ERR_MSG = 'Invalid minutes format. Must be 0 or 30.'

    def _do_validate(self, validated_datetime: datetime) -> bool:
        validated_minutes = validated_datetime.minute
        return validated_minutes % 30 == 0

    def _create_error_message(self) -> str:
        return self.__ERR_MSG

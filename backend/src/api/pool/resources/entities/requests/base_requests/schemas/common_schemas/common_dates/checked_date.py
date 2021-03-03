from datetime import datetime

from ..common_dates import CommonDate, DateValidator


class CheckedDate(CommonDate):
    @staticmethod
    def _date_filter_rules() -> list:
        return [DateBoundaryValidator]


class DateBoundaryValidator(DateValidator):
    __DATE_BOUNDARY = 7
    __ERR_MSG = 'Date parameter must be in a week from now.'

    def _do_validate(self, validated_date: datetime.date) -> bool:
        differences = validated_date - datetime.now().date()
        return 0 <= differences.days <= self.__DATE_BOUNDARY

    def _create_error_message(self) -> str:
        return self.__ERR_MSG

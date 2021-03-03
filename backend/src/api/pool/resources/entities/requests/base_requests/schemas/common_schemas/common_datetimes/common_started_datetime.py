from datetime import datetime, timedelta

from config import BaseApiConfig
from . import CommonDatetime, DateTimeValidator


class CommonStartedDatetime(CommonDatetime):
    @staticmethod
    def _datetime_filter_rules() -> list:
        return [PresentSDValidator, FutureBoundarySDValidator]


class PresentSDValidator(DateTimeValidator):
    __ERR_MSG = 'Started time is in the past.'

    def _do_validate(self, validated_datetime: datetime) -> bool:
        return validated_datetime >= datetime.now() + timedelta(hours=int(BaseApiConfig.TIME_DIFFERENCE))

    def _create_error_message(self) -> str:
        return self.__ERR_MSG


class FutureBoundarySDValidator(DateTimeValidator):
    __ERR_MSG = "Started time is further than next week's Saturday."
    __SATURDAY_WEEK_DAY = 5

    def _do_validate(self, validated_datetime: datetime) -> bool:
        now = datetime.now()
        today_week_day = now.weekday()
        week_day_distance = self.__SATURDAY_WEEK_DAY - today_week_day
        next_week_saturday = \
            now.date() + timedelta(hours=int(BaseApiConfig.TIME_DIFFERENCE)) \
            + timedelta(weeks=1) + timedelta(days=week_day_distance)
        return validated_datetime.date() <= next_week_saturday

    def _create_error_message(self) -> str:
        return self.__ERR_MSG

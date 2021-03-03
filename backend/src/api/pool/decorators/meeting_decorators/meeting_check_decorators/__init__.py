from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.location_exception import \
    InvalidLocationIdException
from src.api.pool.decorators.meeting_decorators import MeetingDecorator
from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_time_libs.available_time_block import \
    BaseAvailableTimeBlock
from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_time_libs.meeting_time_block import \
    BaseOccupiedTimeBlock
from src.api.pool.services.location_services import LocationFormService


class BaseCheckMeetingDecorator(MeetingDecorator, ABC):
    @abstractmethod
    def _create_occupied_block_getter(self) -> BaseOccupiedTimeBlock:
        pass

    @abstractmethod
    def _create_available_block_getter(self) -> BaseAvailableTimeBlock:
        pass

    def get_all(self, *args, **kwargs):
        location_id = kwargs.get('location_id', None)
        date = kwargs.get('date', None)
        available_time_block = []
        date_range = self.__initialize_time(date)

        for date in date_range:
            available_time_block.append(
                {
                    'block': self.__create_available_times_blocks(location_id, date),
                    'date': date.isoformat()
                }
            )

        return available_time_block

    def __create_available_times_blocks(self, location_id, date: datetime.date):
        if location_id:
            location_service = LocationFormService()
            location = location_service.get_model(_id=location_id)
            if location:
                location = location.serialize()

                location_opened_time = datetime.strptime(location['opened_time'], '%H:%M:%S').time()
                location_closed_time = datetime.strptime(location['closed_time'], '%H:%M:%S').time()

                meeting_service = self._get_service()
                location_meetings = meeting_service.get_meetings_on_date(date=date, location_id=location_id)

                available_block_block = self._create_available_block_getter()
                occupied_block_getter = self._create_occupied_block_getter()

                occupied_block = occupied_block_getter.get_time_block(location_meetings=location_meetings)
                available_block = available_block_block.get_time_block(date=date,
                                                                       location_closed_time=location_closed_time,
                                                                       location_opened_time=location_opened_time,
                                                                       meeting_time_blocks=occupied_block)

                return available_block
            else:
                raise InvalidLocationIdException()

    @staticmethod
    def __initialize_time(date: datetime) -> list:
        if date:
            return [date]
        else:
            return [datetime.now().date() + timedelta(days=i) for i in range(0, 7)]

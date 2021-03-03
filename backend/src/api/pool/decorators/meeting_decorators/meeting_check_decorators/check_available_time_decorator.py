from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_time_libs.available_time_block import \
    AvailableTimeBlock
from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_time_libs.meeting_time_block import \
    OccupiedTimeBlock
from . import BaseCheckMeetingDecorator, BaseAvailableTimeBlock, BaseOccupiedTimeBlock


class CheckAvailableTimeDecorator(BaseCheckMeetingDecorator):
    def _create_occupied_block_getter(self) -> BaseOccupiedTimeBlock:
        return OccupiedTimeBlock()

    def _create_available_block_getter(self) -> BaseAvailableTimeBlock:
        return AvailableTimeBlock()

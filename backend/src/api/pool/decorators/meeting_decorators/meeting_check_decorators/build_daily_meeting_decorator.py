from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_time_libs.available_time_block import \
    AvailableModuleTimeBlock
from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_time_libs.meeting_time_block import \
    OccupiedModuleTimeBlock
from . import BaseCheckMeetingDecorator, BaseAvailableTimeBlock, BaseOccupiedTimeBlock


class BuildTimeBlockDecorator(BaseCheckMeetingDecorator):
    def _create_occupied_block_getter(self) -> BaseOccupiedTimeBlock:
        return OccupiedModuleTimeBlock()

    def _create_available_block_getter(self) -> BaseAvailableTimeBlock:
        return AvailableModuleTimeBlock()

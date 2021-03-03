from src.api.pool.services import Service
from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.meeting_update_decorator import \
    UpdateMeetingDecorator
from . import BaseCalendarUpdateDecorator


class MeetingCalendarUpdateDecorator(BaseCalendarUpdateDecorator):

    def _create_service(self) -> Service:
        """
        Create update meeting service
        :return:
        """
        return UpdateMeetingDecorator()

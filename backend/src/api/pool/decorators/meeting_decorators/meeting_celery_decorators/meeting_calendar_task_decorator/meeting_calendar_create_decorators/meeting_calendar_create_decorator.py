from src.api.pool.services import Service
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators.meeting_create_decorator import \
    MeetingCreateDecorator
from . import BaseCalendarCreateDecorator


class MeetingCalendarCreateDecorator(BaseCalendarCreateDecorator):
    def _create_service(self) -> Service:
        return MeetingCreateDecorator()

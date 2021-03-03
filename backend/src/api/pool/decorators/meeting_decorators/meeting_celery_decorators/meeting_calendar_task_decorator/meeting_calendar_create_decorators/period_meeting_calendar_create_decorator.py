from src.api.pool.services import Service
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators.periodic_meeting_create_decorators.meeting_periodic_create_decorator import \
    MeetingPeriodicCreateDecorator
from . import BaseCalendarCreateDecorator


class PeriodicMeetingCalendarCreateDecorator(BaseCalendarCreateDecorator):
    def _create_service(self) -> Service:
        return MeetingPeriodicCreateDecorator()


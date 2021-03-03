from src.api.pool.decorators.meeting_decorators.meeting_create_decorators.meeting_admin_create_decorator import \
    MeetingAdminCreateDecorator
from src.api.pool.services import Service
from . import BaseCalendarCreateDecorator


class AdminMeetingCalendarCreateDecorator(BaseCalendarCreateDecorator):
    def _create_service(self) -> Service:
        return MeetingAdminCreateDecorator()


from src.api.pool.decorators.meeting_decorators.meeting_create_decorators.periodic_meeting_create_decorators.admin_periodic_create_decorator import \
    AdminPeriodicCreateDecorator
from src.api.pool.services import Service
from . import BaseCalendarCreateDecorator


class AdminPeriodicCalendarCreateDecorator(BaseCalendarCreateDecorator):
    def _create_service(self) -> Service:
        return AdminPeriodicCreateDecorator()

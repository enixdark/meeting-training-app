from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.periodic_meeting_update_decorators.periodic_active_meeting_update_decorator import \
    PeriodicActiveUpdateDecorator
from src.api.pool.services import Service
from .disapproval_update_decorator import MeetingDisapprovalUpdateDecorator


class PeriodicDisapprovalUpdateDecorator(MeetingDisapprovalUpdateDecorator):
    def _create_service(self) -> Service:
        return PeriodicActiveUpdateDecorator()

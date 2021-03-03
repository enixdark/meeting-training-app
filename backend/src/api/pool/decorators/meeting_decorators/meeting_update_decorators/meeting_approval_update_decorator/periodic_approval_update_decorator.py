from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.periodic_meeting_update_decorators.periodic_inactive_meeting_update_decorator import \
    PeriodicInactiveMeetingUpdateDecorator
from src.api.pool.services import Service
from .approval_update_decorator import MeetingApprovalUpdateDecorator


class PeriodicApprovalUpdateDecorator(MeetingApprovalUpdateDecorator):
    def _create_service(self) -> Service:
        return PeriodicInactiveMeetingUpdateDecorator()
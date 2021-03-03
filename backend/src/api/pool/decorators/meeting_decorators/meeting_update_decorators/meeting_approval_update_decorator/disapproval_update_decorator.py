from src.api.pool.services import Service
from src.api.pool.services.meeting_services import MeetingInstantFormService
from . import BaseApprovalUpdateDecorator


class MeetingDisapprovalUpdateDecorator(BaseApprovalUpdateDecorator):
    def _set_approval_state(self, **kwargs) -> dict:
        kwargs['state'] = False
        kwargs['is_approval'] = True
        return kwargs

    def _create_service(self) -> Service:
        return MeetingInstantFormService()
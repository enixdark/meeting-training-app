from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.meeting_approval_update_decorator.periodic_disapproval_update_decorator import \
    PeriodicDisapprovalUpdateDecorator
from src.api.pool.services import Service
from . import BaseMeetingAdminUpdateProxy


class PeriodicDisapprovalUpdateProxy(BaseMeetingAdminUpdateProxy):
    def _create_service(self) -> Service:
        return PeriodicDisapprovalUpdateDecorator()

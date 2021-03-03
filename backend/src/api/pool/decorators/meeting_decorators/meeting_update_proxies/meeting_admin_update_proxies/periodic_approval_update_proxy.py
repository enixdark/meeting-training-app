from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.meeting_approval_update_decorator.periodic_approval_update_decorator import \
    PeriodicApprovalUpdateDecorator
from src.api.pool.services import Service
from . import BaseMeetingAdminUpdateProxy


class PeriodicApprovalUpdateProxy(BaseMeetingAdminUpdateProxy):
    def _create_service(self) -> Service:
        return PeriodicApprovalUpdateDecorator()

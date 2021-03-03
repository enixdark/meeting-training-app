from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.meeting_email_approval_update_decorators.meeting_email_approval_update_decorator import \
    MeetingEmailApprovalUpdateDecorator
from src.api.pool.services import Service
from . import BaseMeetingAdminUpdateProxy


class MeetingApprovalUpdateProxy(BaseMeetingAdminUpdateProxy):
    def _create_service(self) -> Service:
        return MeetingEmailApprovalUpdateDecorator()

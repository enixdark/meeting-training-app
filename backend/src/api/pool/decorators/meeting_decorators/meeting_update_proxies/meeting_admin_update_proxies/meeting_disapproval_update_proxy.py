from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.meeting_email_approval_update_decorators.meeting_email_disapproval_update_decorator import \
    MeetingEmailDisapprovalUpdateDecorator
from src.api.pool.services import Service
from . import BaseMeetingAdminUpdateProxy


class MeetingDisapprovalUpdateProxy(BaseMeetingAdminUpdateProxy):
    def _create_service(self) -> Service:
        return MeetingEmailDisapprovalUpdateDecorator()
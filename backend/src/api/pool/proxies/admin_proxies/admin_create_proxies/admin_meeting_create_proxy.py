from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.admin_meeting_email_create_decorator import \
    AdminMeetingEmailCreateDecorator
from src.api.pool.proxies.admin_proxies.admin_create_proxies import AdminCreateProxy
from src.api.pool.services import Service


class AdminEmailCreateProxy(AdminCreateProxy):
    def _create_service(self) -> Service:
        return AdminMeetingEmailCreateDecorator()

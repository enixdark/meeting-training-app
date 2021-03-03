from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.meeting_email_delete_decorators import \
    MeetingEmailDeleteDecorator
from src.api.pool.proxies.admin_proxies.admin_delete_proxies import AdminDeleteProxy
from src.api.pool.services import Service


class AdminMeetingDeleteDecorator(AdminDeleteProxy):
    def _create_service(self) -> Service:
        return MeetingEmailDeleteDecorator()

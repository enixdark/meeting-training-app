from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.meeting_email_delete_decorators import \
    MeetingEmailDeleteDecorator
from src.api.pool.proxies.meeting_coordinator_proxies.coordinator_delete_proxies import CoordinatorDeleteProxy
from src.api.pool.services import Service


class CoordinatorMeetingDeleteDecorator(CoordinatorDeleteProxy):
    def _create_service(self) -> Service:
        return MeetingEmailDeleteDecorator()

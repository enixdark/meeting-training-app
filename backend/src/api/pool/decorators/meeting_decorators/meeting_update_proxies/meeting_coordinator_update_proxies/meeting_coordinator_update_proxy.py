from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.meeting_email_update_decorator import \
    MeetingEmailUpdateDecorator
from src.api.pool.services import Service
from . import BaseMeetingCoordinatorUpdateProxy


class MeetingCoordinatorUpdateProxy(BaseMeetingCoordinatorUpdateProxy):
    def _create_service(self) -> Service:
        return MeetingEmailUpdateDecorator()

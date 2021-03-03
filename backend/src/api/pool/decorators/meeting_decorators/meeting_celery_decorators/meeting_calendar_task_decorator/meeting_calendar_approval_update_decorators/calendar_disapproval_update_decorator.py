from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_approval_update_decorators import \
    BaseCalendarApprovalUpdateDecorator
from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.meeting_approval_update_decorator.disapproval_update_decorator import \
    MeetingDisapprovalUpdateDecorator
from src.api.pool.services import Service
from src.message_queue.tasks.calendar_tasks import DeleteEventTask


class MeetingCalendarDisapprovalUpdateDecorator(BaseCalendarApprovalUpdateDecorator):
    def _add_calendar_task(self, meeting_id: int, auth_user_id: int):
        self._add_executor(task=DeleteEventTask(),
                           delay_arguments={
                               'meeting_id': meeting_id,
                               'user_id': auth_user_id
                           })

    def _create_service(self) -> Service:
        return MeetingDisapprovalUpdateDecorator()

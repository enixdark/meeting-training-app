from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_approval_update_decorators.calendar_approval_update_decorator import \
    MeetingCalendarApprovalUpdateDecorator
from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_email_task_decorator.meeting_email_approval_update_decorators import \
    BaseApprovalEmailUpdateDecorator, Meeting, MeetingUser
from src.api.pool.services import Service
from src.message_queue.tasks.email_tasks import InvitedEmailTask, ApprovalEmailTask


class MeetingEmailApprovalUpdateDecorator(BaseApprovalEmailUpdateDecorator):
    def _add_approval_tasks(self, meeting: Meeting, coordinator: MeetingUser):
        self._add_executor(task=ApprovalEmailTask(),
                           delay_arguments={
                               'meeting_id': meeting.id,
                               'received_email': coordinator.user.email
                           })
        for attendee in meeting.associate_users:
            if attendee.user_id is not coordinator.user_id:
                self._add_executor(task=InvitedEmailTask(),
                                   delay_arguments={
                                       'meeting_id': meeting.id,
                                       'received_email': attendee.user.email
                                   })

    def _create_service(self) -> Service:
        return MeetingCalendarApprovalUpdateDecorator()

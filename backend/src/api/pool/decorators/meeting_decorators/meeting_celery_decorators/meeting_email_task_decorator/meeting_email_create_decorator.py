from src.api.pool.decorators.celery_decorator import CeleryDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators import Model
from src.message_queue.tasks.email_tasks import InvitedEmailTask
from ..meeting_calendar_task_decorator.meeting_calendar_create_decorators.meeting_calendar_create_decorator import \
    MeetingCalendarCreateDecorator


class MeetingEmailCreateDecorator(CeleryDecorator):
    def _create_service(self) -> Service:
        return MeetingCalendarCreateDecorator()

    def create_new_model(self, *args, **kwargs) -> Model:
        self._prepare_auth_service()
        new_meeting = super(MeetingEmailCreateDecorator, self).create_new_model(*args, **kwargs)
        attendees = new_meeting.associate_users
        for attendee in attendees:
            if not attendee.is_coordinator:
                self._add_executor(task=InvitedEmailTask(),
                                   delay_arguments={
                                       'meeting_id': new_meeting.id,
                                       'received_email': attendee.user.email
                                   })

        self._execute()
        return new_meeting

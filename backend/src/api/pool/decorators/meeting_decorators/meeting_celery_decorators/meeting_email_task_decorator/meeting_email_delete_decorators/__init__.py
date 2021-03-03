from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.decorators.celery_decorator import CeleryDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_delete_decorators.meeting_calendar_delete_decorator import \
    MeetingCalendarDeleteDecorator
from src.api.pool.services.attendee_services import AttendeeFormService
from src.database.postgres.meeting import Meeting
from src.message_queue.tasks.email_tasks import CancelEmailTask


class MeetingEmailDeleteDecorator(CeleryDecorator):
    def delete_model(self, *args, **kwargs) -> bool:
        meeting = self.get_model(_id=kwargs['_id'])
        if not isinstance(meeting, Meeting):
            raise InvalidMeetingIdException()
        if meeting.state:
            attendee_service = AttendeeFormService()
            coordinator = attendee_service.get_meeting_coordinator(meeting_id=meeting.id)
            for attendee in meeting.associate_users:
                if attendee.user_id is not coordinator.user_id and attendee.may_join is True:
                    self._add_executor(task=CancelEmailTask(),
                                       delay_arguments={
                                           'meeting_id': meeting.id,
                                           'received_email': attendee.user.email
                                       })

        deleted = super(MeetingEmailDeleteDecorator, self).delete_model(*args, **kwargs)
        if deleted:
            self._execute()
        else:
            self._flush_tasks()
        return deleted

    def _create_service(self) -> Service:
        return MeetingCalendarDeleteDecorator()

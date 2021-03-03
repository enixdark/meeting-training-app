from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_delete_decorators import \
    BaseCalendarDeleteDecorator
from src.api.pool.services.meeting_services import Meeting


class MeetingCalendarDeleteDecorator(BaseCalendarDeleteDecorator):
    def _execute_delete(self, meeting: Meeting, *args, **kwargs) -> bool:
        # check google id to execute delete google calendar event celery task
        meeting_id = meeting.id
        google_id = meeting.google_calendar_id
        # add delete calendar task
        self._add_calendar_task(meeting_id, google_id)

        deleted = super(BaseCalendarDeleteDecorator, self).delete_model(_id=meeting.id, *args, **kwargs)
        # commit session
        self.commit()

        return deleted

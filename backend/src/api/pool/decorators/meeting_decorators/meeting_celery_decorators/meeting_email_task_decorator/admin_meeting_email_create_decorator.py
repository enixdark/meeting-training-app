from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_create_decorators.admin_meeting_calendar_create_decorator import \
    AdminMeetingCalendarCreateDecorator
from .meeting_email_create_decorator import MeetingEmailCreateDecorator, Service


class AdminMeetingEmailCreateDecorator(MeetingEmailCreateDecorator):
    def _create_service(self) -> Service:
        return AdminMeetingCalendarCreateDecorator()
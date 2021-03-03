from abc import ABC, abstractmethod

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.decorators.celery_decorator import CeleryDecorator
from src.api.pool.services.attendee_services import AttendeeFormService
from src.database.postgres.meeting import Meeting
from src.database.postgres.meeting_user import MeetingUser
from src.message_queue.tasks.email_tasks.retrieve_meeting_email_task.approval_email_task import ApprovalEmailTask


class BaseApprovalEmailUpdateDecorator(CeleryDecorator, ABC):

    def update_model(self, *args, **kwargs) -> bool:
        updated = super(BaseApprovalEmailUpdateDecorator, self).update_model(*args, **kwargs)
        if updated:
            meeting = self.get_model(_id=kwargs['_id'])
            if not isinstance(meeting, Meeting):
                raise InvalidMeetingIdException()
            attendee_service = AttendeeFormService()
            coordinator = attendee_service.get_meeting_coordinator(meeting_id=meeting.id)
            if meeting.is_approval:
                self._add_approval_tasks(meeting=meeting, coordinator=coordinator)
            self._execute()
        return updated

    @abstractmethod
    def _add_approval_tasks(self, meeting: Meeting, coordinator: MeetingUser):
        """
        Add email tasks to meeting attendees
        :param meeting:
        :param coordinator:
        :return: None
        """
        pass

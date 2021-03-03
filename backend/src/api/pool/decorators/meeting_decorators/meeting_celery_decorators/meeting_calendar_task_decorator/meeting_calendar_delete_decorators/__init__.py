from abc import ABC, abstractmethod

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.decorators.celery_decorator import CeleryDecorator, Service
from src.api.pool.services.attendee_services import AttendeeFormService
from src.api.pool.services.meeting_services import MeetingFormService, Meeting
from src.message_queue.tasks.calendar_tasks import DeleteEventTask


class BaseCalendarDeleteDecorator(CeleryDecorator, ABC):
    def __init__(self):
        super(BaseCalendarDeleteDecorator, self).__init__()
        self.__coordinator = None

    def _create_service(self) -> Service:
        return MeetingFormService()

    def delete_model(self, *args, **kwargs) -> bool:
        # check meeting_id and delete meeting from db
        meeting_id = kwargs.pop('_id')
        meeting = self.get_model(_id=meeting_id)
        if not isinstance(meeting, Meeting):
            raise InvalidMeetingIdException()

        deleted = self._execute_delete(meeting, *args, **kwargs)
        self._execute()
        return deleted

    @abstractmethod
    def _execute_delete(self, meeting: Meeting, *args, **kwargs) -> bool:
        pass

    def _add_calendar_task(self, meeting_id: int, google_id: None):
        if google_id:
            if not self.__coordinator:
                # if admin use this module, use admin access_token to activate DeleteEvenTask
                auth_user = self.get_authenticated_user()
                for role in auth_user.roles:
                    if role == 'admin':
                        self.__coordinator = auth_user
                if not self.__coordinator:
                    # retrieve coordinator to use its access token (auth user is not always coordinator :( )
                    attendee_service = AttendeeFormService()
                    coordinator = attendee_service.get_meeting_coordinator(meeting_id=meeting_id)
                    self.__coordinator = coordinator.user

            # execute delete google calendar event celery task
            self._add_executor(task=DeleteEventTask(),
                               delay_arguments={
                                   'meeting_id': meeting_id,
                                   'user_id': self.__coordinator.id
                               })

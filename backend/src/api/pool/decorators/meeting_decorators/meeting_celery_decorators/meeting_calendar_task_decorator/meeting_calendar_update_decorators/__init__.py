from abc import ABC

from config import BaseApiConfig
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.services.attendee_services import AttendeeFormService
from src.api.pool.decorators.celery_decorator import CeleryDecorator
from src.database.postgres.meeting import Meeting
from src.message_queue.tasks.calendar_tasks import CreateEventTask, UpdateEventTask, DeleteEventTask


class BaseCalendarUpdateDecorator(CeleryDecorator, ABC):
    __DELAY_UPDATED_TIME = BaseApiConfig.CALENDAR_UPDATE_DELAY

    def update_model(self, *args, **kwargs) -> bool:
        """
        After service that is created by self._create_service use update_model, add an celery task to interact with
        Google calendar
        :param args:
        :param kwargs:
        :return: true if Meeting is update successfully, otherwise, return false
        """
        updated = super(BaseCalendarUpdateDecorator, self).update_model(*args, **kwargs)

        meeting_id = kwargs['_id']
        meeting = self.get_model(_id=meeting_id)
        if not isinstance(meeting, Meeting):
            raise InvalidMeetingIdException()

        # retrieve coordinator to use its access token (auth user is not always coordinator :( )
        attendee_service = AttendeeFormService()
        coordinator = attendee_service.get_meeting_coordinator(meeting_id=meeting_id)
        coordinator = coordinator.user

        # check valid google calendar id
        if meeting.google_calendar_id:
            # check meeting state,
            # if true send celery update task,
            # else send celery delete task
            if meeting.state:
                self._add_executor(task=UpdateEventTask(),
                                   delay_arguments={
                                       'meeting_id': meeting_id,
                                       'user_id': coordinator.id
                                   },
                                   async_options={
                                       'countdown': self.__DELAY_UPDATED_TIME
                                   })
            else:
                self._add_executor(task=DeleteEventTask(),
                                   delay_arguments={
                                       'meeting_id': meeting_id,
                                       'user_id': coordinator.id
                                   })
        else:
            self._add_executor(task=CreateEventTask(),
                               delay_arguments={
                                   'meeting_id': meeting_id,
                                   'user_id': coordinator.id
                               })
        self._execute()
        return updated

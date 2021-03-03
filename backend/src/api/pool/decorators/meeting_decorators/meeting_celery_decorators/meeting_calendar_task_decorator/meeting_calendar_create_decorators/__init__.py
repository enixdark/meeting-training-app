from abc import ABC

from src.api.pool.decorators.celery_decorator import CeleryDecorator
from src.database.postgres.base import Model
from src.message_queue.tasks.calendar_tasks.create_event_task import CreateEventTask


class BaseCalendarCreateDecorator(CeleryDecorator, ABC):
    def create_new_model(self, *args, **kwargs) -> Model:
        new_meeting = super(BaseCalendarCreateDecorator, self).create_new_model(*args, **kwargs)
        if new_meeting.is_approval:
            auth_user = self.get_authenticated_user()
            self._add_executor(task=CreateEventTask(),
                               delay_arguments={
                                   'meeting_id': new_meeting.id,
                                   'user_id': auth_user.id
                               })
            self._execute()
        return new_meeting

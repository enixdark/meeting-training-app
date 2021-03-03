from src.api.factory.libs.google_libs.google_calendar_libs import GoogleCalendarExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.maintain_event.insert_event import InsertEventExecutor
from .base_calendar_task import BaseCalendarTask


class CreateEventTask(BaseCalendarTask):
    def _after_calendar_request(self, event: dict):
        self._prepared_service().update_model(_id=self.meeting_id,
                                              google_calendar_id=event['id'],
                                              must_synchronized=False)
        self.commit_session()

    def _create_calendar_executor(self) -> GoogleCalendarExecutor:
        return InsertEventExecutor(self._get_meeting())

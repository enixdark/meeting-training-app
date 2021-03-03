from src.api.factory.libs.google_libs.google_calendar_libs import GoogleCalendarExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.maintain_event.update_event import UpdateEventExecutor
from src.message_queue.tasks.calendar_tasks.id_base_event_task import IdBaseEventTask


class UpdateEventTask(IdBaseEventTask):
    def _after_id_calendar_request(self, executed_response: dict):
        self._prepared_service().update_model(_id=self.meeting_id,
                                              must_synchronized=False)
        self.commit_session()

    def _create_calendar_executor(self) -> GoogleCalendarExecutor:
        return UpdateEventExecutor(self._get_meeting())

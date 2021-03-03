from src.api.factory.libs.google_libs.google_calendar_libs import GoogleCalendarExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.delete_event import DeleteEventExecutor
from src.message_queue.tasks.calendar_tasks.id_base_event_task import IdBaseEventTask


class DeleteEventTask(IdBaseEventTask):
    def _after_id_calendar_request(self, executed_response: dict):
        self._prepared_service().update_model(_id=self.meeting_id,
                                              google_calendar_id=None)
        self.commit_session()

    def _create_calendar_executor(self) -> GoogleCalendarExecutor:
        return DeleteEventExecutor(self._get_meeting())

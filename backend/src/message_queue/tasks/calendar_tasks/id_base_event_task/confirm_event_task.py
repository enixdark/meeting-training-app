from src.api.factory.libs.google_libs.google_calendar_libs import GoogleCalendarExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.maintain_event.confirm_event import ConfirmEventExecutor
from src.message_queue.tasks.calendar_tasks.id_base_event_task import IdBaseEventTask


class ConfirmEventTask(IdBaseEventTask):
    def _after_id_calendar_request(self, event: dict):
        pass

    def _create_calendar_executor(self) -> GoogleCalendarExecutor:
        return ConfirmEventExecutor(self._get_meeting())

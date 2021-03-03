from abc import abstractmethod

from src.api.factory.exceptions.service_exceptions.google_exceptions.calendar_exceptions import \
    CalendarIdentifierException
from src.api.factory.libs.google_libs.google_calendar_libs import GoogleCalendarExecutor
from src.api.factory.libs.google_libs.google_calendar_libs.maintain_event.insert_event import InsertEventExecutor
from src.message_queue.tasks.calendar_tasks.base_calendar_task import BaseCalendarTask


class IdBaseEventTask(BaseCalendarTask):
    @abstractmethod
    def _create_calendar_executor(self) -> GoogleCalendarExecutor:
        pass

    @abstractmethod
    def _after_id_calendar_request(self, executed_response: dict):
        pass

    def _on_calendar_request(self) -> dict:
        try:
            return self._request_google_calendar()
        except CalendarIdentifierException as ce:
            # if error happened because of google_calendar_id, replace it with a new one.
            # (mostly because of illegal activities on google_calendar_id field on meeting table on db
            # or manually delete event on Google Calendar server)
            self.calendar_executor = InsertEventExecutor(self._get_meeting())
            new_event = self._request_google_calendar()
            self._prepared_service().update_model(_id=self.meeting_id,
                                                  google_calendar_id=new_event['id'],
                                                  must_synchronized=False)
            self.commit_session()
            self.close_session()
            return {
                'id_error': True
            }

    def _after_calendar_request(self, executed_response: dict):
        id_error = executed_response.get('id_error', False)
        if not id_error:
            self._after_id_calendar_request(executed_response)

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidPeriodicMeetingException
from src.api.pool.decorators.decorator_helpers.decorator_counters.periodic_delete_counter import PeriodicDeleteCounter
from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_delete_decorators import \
    BaseCalendarDeleteDecorator
from src.api.pool.services.meeting_services import Meeting
from src.api.pool.services.meeting_services.periodic_meeting_services import PeriodicMeetingFormService


class PeriodicCalendarDeleteDecorator(BaseCalendarDeleteDecorator):
    def __init__(self):
        super(PeriodicCalendarDeleteDecorator, self).__init__()
        self.__counter = PeriodicDeleteCounter()

    def _execute_delete(self, meeting: Meeting, *args, **kwargs) -> bool:
        # check valid periodic meeting
        if not meeting.periodic_id:
            raise InvalidPeriodicMeetingException()

        # get all periodic meeting base on input periodic meeting
        periodic_service = PeriodicMeetingFormService()
        periodic_meetings = periodic_service.get_all_periodic_meetings(meeting.periodic_id)

        # for each of them, set a remove calendar event and rm from db
        deleted = True
        deleted_index = 0
        for periodic_meeting in periodic_meetings:
            periodic_meeting_id = periodic_meeting.id
            google_id = periodic_meeting.google_calendar_id
            self._add_calendar_task(periodic_meeting_id, google_id)

            id_deleted = super(BaseCalendarDeleteDecorator, self).delete_model(_id=periodic_meeting_id,
                                                                               *args, **kwargs)
            if id_deleted:
                self.__counter.update_success_states(deleted_index)
            else:
                self.__counter.update_failed_states(deleted_index)
            deleted += id_deleted
            deleted_index += 1

        self.commit()
        return deleted

    def get_success_count(self) -> int:
        return self.__counter.get_success_count()

    def get_failed_count(self) -> int:
        return self.__counter.get_failed_count()

    def get_delete_msg(self) -> dict:
        return self.__counter.get_periodic_messages()

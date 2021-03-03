from abc import ABC, abstractmethod
from datetime import datetime

from src.api.factory.exceptions.service_exceptions import ServiceException
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidPeriodicMeetingException, InvalidMeetingIdException
from src.api.pool.decorators.decorator_helpers.decorator_counters.decorator_update_counter import \
    UpdateDecoratorCounter
from src.api.pool.decorators.meeting_decorators.meeting_celery_decorators.meeting_calendar_task_decorator.meeting_calendar_update_decorators.meeting_calendar_update_decorator import \
    MeetingCalendarUpdateDecorator
from src.api.pool.services.meeting_services.periodic_meeting_services import PeriodicMeetingFormService
from ... import MeetingAuthDecorator, Service


class BasePeriodicMeetingUpdateDecorator(MeetingAuthDecorator, ABC):
    def __init__(self):
        super(BasePeriodicMeetingUpdateDecorator, self).__init__()
        self.__counter = UpdateDecoratorCounter()

    def _create_service(self) -> Service:
        return MeetingCalendarUpdateDecorator()

    def update_model(self, *args, **kwargs) -> bool:
        # find and update all available periodic meetings
        meeting = self.get_model(_id=kwargs['_id'])
        if not meeting:
            raise InvalidMeetingIdException()
        periodic_id = meeting.periodic_id
        if periodic_id:
            # get all available periodic meetings with the same periodic id
            periodic_meeting_service = self._create_periodic_service()
            available_periodic_meetings = periodic_meeting_service.get_available_periodic_meetings(
                periodic_id=periodic_id)

            # update all of periodic meetings
            update_index = 0
            for periodic_meeting in available_periodic_meetings:
                # combine time to periodic meeting's date
                kwargs['_id'] = periodic_meeting.id
                kwargs['started_time'] = self.__combine_time(to_get_date=periodic_meeting.started_time,
                                                             to_get_time=kwargs.get('started_time', None))
                kwargs['finished_time'] = self.__combine_time(to_get_date=periodic_meeting.finished_time,
                                                              to_get_time=kwargs.get('finished_time', None))

                try:
                    updated = super(BasePeriodicMeetingUpdateDecorator, self).update_model(*args, **kwargs)
                    if updated:
                        self.__counter.update_success_states(update_index)
                    else:
                        self.__counter.update_failed_states(update_index)
                    update_index += 1
                except ServiceException as e:
                    self.__counter.update_failed_states(update_index, failed_reason=str(e))
                    update_index += 1
                    continue
            return True
        raise InvalidPeriodicMeetingException()

    @staticmethod
    def __combine_time(to_get_date: datetime, to_get_time: datetime):
        if to_get_time:
            return datetime.combine(date=to_get_date.date(), time=to_get_time.time())
        return to_get_date

    def get_periodic_messages(self) -> dict:
        return self.__counter.get_periodic_messages()

    def get_success_count(self) -> int:
        return self.__counter.get_success_count()

    def get_failed_count(self) -> int:
        return self.__counter.get_failed_count()

    @abstractmethod
    def _create_periodic_service(self) -> PeriodicMeetingFormService:
        pass

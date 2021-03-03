from src.api.factory.exceptions.service_exceptions import ServiceException
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidPeriodicMeetingException, InvalidMeetingIdException
from src.api.pool.services import Service
from src.api.pool.decorators.decorator_helpers.decorator_counters.decorator_update_counter import \
    UpdateDecoratorCounter
from src.api.pool.services.meeting_services import MeetingFormService
from src.api.pool.services.meeting_services.periodic_meeting_services import PeriodicMeetingFormService
from . import ChangeCoordinatorDecorator
from .. import AttendeeAuthDecorator


class PeriodicChangeCoordinatorDecorator(AttendeeAuthDecorator):
    def __init__(self):
        super(PeriodicChangeCoordinatorDecorator, self).__init__()
        self.__counter = UpdateDecoratorCounter()

    def _create_service(self) -> Service:
        return ChangeCoordinatorDecorator()

    def update_model(self, *args, **kwargs) -> bool:
        self._prepare_auth_service()
        meeting_service = MeetingFormService()
        meeting = meeting_service.get_model(_id=kwargs.get('meeting_id', 0))
        if not meeting:
            raise InvalidMeetingIdException()

        periodic_id = meeting.periodic_id
        if not periodic_id:
            raise InvalidPeriodicMeetingException()

        periodic_meeting_service = PeriodicMeetingFormService()
        periodic_meetings = periodic_meeting_service.get_available_periodic_meetings(periodic_id=periodic_id)

        update_index = 0
        for periodic_meeting in periodic_meetings:
            try:
                kwargs['meeting_id'] = periodic_meeting.id
                updated = super(PeriodicChangeCoordinatorDecorator, self).update_model(*args, **kwargs)
                if updated:
                    self.__counter.update_success_states(update_index)
                else:
                    self.__counter.update_failed_states(update_index)
                update_index += 1
            except ServiceException as se:
                self.__counter.update_failed_states(update_index, failed_reason=str(se))
                update_index += 1
                continue
        if self.get_failed_count() > 0:
            return False
        return True

    def get_periodic_messages(self) -> dict:
        return self.__counter.get_periodic_messages()

    def get_success_count(self) -> int:
        return self.__counter.get_success_count()

    def get_failed_count(self) -> int:
        return self.__counter.get_failed_count()

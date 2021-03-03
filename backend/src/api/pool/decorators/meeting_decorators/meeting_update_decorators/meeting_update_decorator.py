from datetime import datetime

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.location_exception import \
    InvalidLocationIdException
from src.api.pool.decorators.meeting_decorators.meeting_update_decorators import BaseUpdateMeetingDecorator, Meeting
from src.api.pool.services.location_services import LocationFormService
from src.database.postgres.location import Location


class UpdateMeetingDecorator(BaseUpdateMeetingDecorator):
    def _validate_updated_fields(self, meeting, *args, **kwargs) -> dict:
        if isinstance(meeting, Meeting):
            # detect update in location_id or meeting time to reset is_accepted and may_joint to False
            if self.__detect_update_location(meeting.location_id, kwargs.get('location_id')) \
                    or self.__detect_update_time(meeting.started_time, meeting.finished_time,
                                                 kwargs.get('started_time'), kwargs.get('finished_time')):
                kwargs = self.__validate_location_id(meeting, **kwargs)
                kwargs = self._validate_time_fields(meeting, **kwargs)
        return kwargs

    @staticmethod
    def __detect_update_location(meeting_location_id: int, updated_location_id: int) -> bool:
        """
        Return true if update location was detected
        :param meeting_location_id:
        :param updated_location_id:
        :return:
        """
        if updated_location_id:
            return meeting_location_id != updated_location_id
        return False

    @staticmethod
    def __detect_update_time(meeting_started_time: datetime, meeting_finished_time: datetime,
                             updated_started_time: datetime, updated_finished_time: datetime):
        """
        Return true if update meeting time was detected
        :param meeting_started_time:
        :param meeting_finished_time:
        :param updated_started_time:
        :param updated_finished_time:
        :return:
        """
        if updated_started_time and updated_finished_time:
            return meeting_started_time != updated_started_time or meeting_finished_time != updated_finished_time
        return False

    @staticmethod
    def __validate_location_id(meeting, **kwargs) -> dict:
        if isinstance(meeting, Meeting):
            location_id = kwargs.get('location_id', meeting.location_id)
            location_service = LocationFormService()
            location = location_service.get_model(_id=location_id)
            if isinstance(location, Location):
                return kwargs
            else:
                raise InvalidLocationIdException()
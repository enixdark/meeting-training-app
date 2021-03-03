from datetime import datetime

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.location_exception import \
    InvalidLocationIdException
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidTimeException, LocationTimeBoundaryException
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.user_exceptions import InvalidUserIdException
from src.api.pool.decorators.meeting_decorators import MeetingDecorator
from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_attendee_libs.attendee_create import \
    CreateMeetingAttendees
from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_location_libs.location_available_checker import \
    LocationAvailableChecker
from src.api.pool.decorators.meeting_decorators.libs_meeting_decorator.meeting_location_libs.location_boundary_checker import \
    LocationBoundaryChecker
from src.api.pool.services.location_services import LocationFormService
from src.api.pool.services.user_services import UserFormService
from src.database.postgres.location import Location, Model


class BaseCreateMeetingDecorator(MeetingDecorator):
    def create_new_model(self, *args, **kwargs) -> Model:
        location_id = kwargs.get('location_id', None)
        if location_id:
            location_service = LocationFormService()
            location = location_service.get_model(_id=location_id)
            if isinstance(location, Location):
                meeting_started_datetime = kwargs['started_time']
                meeting_finished_datetime = kwargs['finished_time']
                if self.__check_valid_meeting_datetime(meeting_started_datetime, meeting_finished_datetime):
                    # check location boundary time
                    location_boundary_checker = LocationBoundaryChecker()
                    if location_boundary_checker.execute(location,
                                                         meeting_started_datetime,
                                                         meeting_finished_datetime):
                        # check available location
                        if location.is_multi_access:
                            return self.__create_meeting(*args, **kwargs)
                        meeting_service = self._get_service()
                        location_meetings = meeting_service.get_available_meetings(location_id=location_id)
                        location_available_checker = LocationAvailableChecker()
                        if location_available_checker.execute(location_meetings,
                                                              meeting_started_datetime,
                                                              meeting_finished_datetime):
                            return self.__create_meeting(*args, **kwargs)
                        else:
                            raise InvalidTimeException()
                    else:
                        raise LocationTimeBoundaryException()
            else:
                raise InvalidLocationIdException()

    @staticmethod
    def __check_valid_meeting_datetime(started_datetime: datetime, finished_datetime: datetime) -> bool:
        meeting_started_date = started_datetime.date()
        meeting_finished_date = finished_datetime.date()
        # check meeting start and finish in a day
        if meeting_started_date == meeting_finished_date:
            # check meeting order date
            if started_datetime < finished_datetime:
                # prevent create meeting start in the past
                if started_datetime > datetime.now():
                    return True
        return False

    def __create_meeting(self, *args, **kwargs):
        creator_id = kwargs.get('creator_id', 0)
        attendees = kwargs.pop('attendees', [])
        user_service = UserFormService()
        if creator_id:
            creator = user_service.get_model(_id=creator_id)
            attendees_creator = CreateMeetingAttendees()
            if creator:
                kwargs['associate_users'] = attendees_creator.create_associated_users(creator_id, attendees)
                new_meeting = super().create_new_model(*args, **kwargs)
                self.commit()
                return new_meeting
            else:
                raise InvalidUserIdException()

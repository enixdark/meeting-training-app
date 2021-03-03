from abc import ABC, abstractmethod
from datetime import datetime

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.location_exception import \
    InvalidLocationIdException
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    LocationTimeBoundaryException, InvalidTimeException, InvalidMeetingIdException
from src.api.pool.services.location_services import LocationFormService
from src.api.pool.services.meeting_services import MeetingFormService
from src.database.postgres.location import Location
from src.database.postgres.meeting import Meeting
from .. import MeetingAuthDecorator
from ..libs_meeting_decorator.meeting_attendee_libs.attendee_reset import ResetMeetingAttendees
from ..libs_meeting_decorator.meeting_attendee_libs.attendee_update import UpdateMeetingAttendees
from ..libs_meeting_decorator.meeting_location_libs.location_boundary_checker import LocationBoundaryChecker
from ..libs_meeting_decorator.meeting_location_libs.location_update_checker import LocationUpdateChecker


class BaseUpdateMeetingDecorator(MeetingAuthDecorator, ABC):
    def __init__(self):
        super().__init__()
        self.__meeting_attendee = UpdateMeetingAttendees()

    def update_model(self, *args, **kwargs) -> bool:
        relations = self._get_service().create_many_to_many_relations()
        auth_user = self.get_authenticated_user()

        meeting = self.get_model(_id=kwargs['_id'])
        if isinstance(meeting, Meeting):
            # detect update in location_id or meeting time to reset is_accepted and may_joint to False
            kwargs = self._validate_updated_fields(meeting=meeting, *args, **kwargs)
            for key, value in kwargs.items():
                if key in relations.keys():
                    if key == 'attendees':
                        value = self.__meeting_attendee.create_associated_users(auth_user.id, value)
                        kwargs[key] = value
                        break
            updated = super().update_model(updated_model=meeting, *args, **kwargs)
            self.commit()
            return updated
        else:
            raise InvalidMeetingIdException()

    @staticmethod
    def __init_updated_attendees(auth_user_id: int, meeting) -> list:
        """
        Build a list of attendees based on existing data
        :param auth_user_id:
        :param meeting:
        :return:
        """
        attendees = []
        if isinstance(meeting, Meeting):
            for associate_user in meeting.associate_users:
                if associate_user.user.id != auth_user_id:
                    attendee = dict()
                    attendee['email'] = associate_user.user.email
                    attendee['is_accepted'] = associate_user.is_accepted
                    attendee['may_join'] = associate_user.may_join
                    attendees.append(attendee)
        return attendees

    def _validate_time_fields(self, meeting, *args, **kwargs) -> dict:
        location_id = kwargs.get('location_id', meeting.location_id)
        meeting_started_datetime = kwargs.get('started_time', meeting.started_time)
        meeting_finished_datetime = kwargs.get('finished_time', meeting.finished_time)

        location_service = LocationFormService()
        location = location_service.get_model(_id=location_id)
        # CHECK UPDATE TIME

        location_boundary_checker = LocationBoundaryChecker()
        if location_boundary_checker.execute(location,
                                             meeting_started_datetime,
                                             meeting_finished_datetime):
            meeting_service = MeetingFormService()
            location_meetings = meeting_service.get_available_meetings(location_id=location_id)
            location_available_checker = LocationUpdateChecker()
            if location_available_checker.execute(meeting.id, location_meetings,
                                                  meeting_started_datetime,
                                                  meeting_finished_datetime):

                # the reset logic that reset all attendees states to false

                return self.__reset_attendees_states(meeting, **kwargs)
            else:
                raise InvalidTimeException()
        else:
            raise LocationTimeBoundaryException()

    def __reset_attendees_states(self, meeting, *args, **kwargs) -> dict:
        auth_user = self.get_authenticated_user()
        # the reset logic that reset all attendees states to false, (if client send attendees)
        self.__meeting_attendee = ResetMeetingAttendees()
        # if update request has no attendees list, create a new one with existing data
        if not kwargs.get('attendees'):
            kwargs['attendees'] = self.__init_updated_attendees(auth_user.id, meeting)
        return kwargs

    @abstractmethod
    def _validate_updated_fields(self, meeting, *args, **kwargs) -> dict:
        pass

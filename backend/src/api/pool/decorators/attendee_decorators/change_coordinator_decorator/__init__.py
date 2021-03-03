from src.api.factory.exceptions.service_exceptions.db_service_exceptions.attendee_exceptions import \
    InvalidMeetingPermissionException, InvalidCoordinatorException
from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.services.attendee_services import AttendeeFormService, MeetingUser
from src.database.postgres.user import User
from .. import AttendeeAuthDecorator


class ChangeCoordinatorDecorator(AttendeeAuthDecorator):
    def update_model(self, *args, **kwargs) -> bool:
        """
        Update is_coordinator fields on MeetingUser table
        :param args:
        :param kwargs:
        :return:
        """
        meeting_id = kwargs['meeting_id']
        coordinator_id = kwargs['coordinator_id']

        attendee_service = AttendeeFormService()
        current_coordinator = attendee_service.get_meeting_coordinator(meeting_id=meeting_id)

        # check valid meeting id
        if current_coordinator:
            if self.__check_valid_coordinator_permission(current_coordinator):
                # set current meeting coordinator to normal meeting attendee
                current_coordinator.is_coordinator = False
                if super().update_model(updated_model=current_coordinator):
                    # update new coordinator
                    new_coordinator = attendee_service.get_meeting_user(meeting_id=meeting_id,
                                                                        user_id=coordinator_id)
                    # check valid new coordinator
                    if self.__check_activated_coordinator(new_coordinator):
                        new_coordinator.is_coordinator = True
                        if super().update_model(updated_model=new_coordinator):
                            self.commit()
                            return True
                        else:
                            self.rollback()
                    else:
                        raise InvalidCoordinatorException()
            else:
                raise InvalidMeetingPermissionException()
        else:
            raise InvalidMeetingIdException()


    @staticmethod
    def __check_activated_coordinator(coordinator) -> bool:
        """
        Check if coordinator had logged in before
        :param coordinator: A User model instance of Meeting coordinator
        :return: True if coordinator's is_activated field is True, otherwise, return False
        """
        if isinstance(coordinator, MeetingUser):
            new_coordinator_user = coordinator.user
            if isinstance(new_coordinator_user, User):
                if new_coordinator_user.is_activated:
                    return True
        return False

    def __check_valid_coordinator_permission(self, coordinator) -> bool:
        """
        Check if self's auth_user is the coordinator of the meeting
        :param coordinator: A User model instance of Meeting coordinator
        :return: True if auth_user and coordinator is the same user, otherwise, return False
        """
        if isinstance(coordinator, MeetingUser):
            auth_user = self.get_authenticated_user()
            coordinator_user = coordinator.user
            if isinstance(coordinator_user, User):
                if coordinator_user.id == auth_user.id:
                    return True
        return False

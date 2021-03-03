from abc import ABC, abstractmethod

from src.api.pool.services.user_services import UserFormService


class MeetingAttendees(ABC):
    def create_associated_users(self, coordinator_id, attendees) -> list:
        """
        Create Meeting model's associated_users field
        :param coordinator_id:
        :param attendees:
        :return:
        """
        associated_users = list()
        associated_users.append(self.create_coordinator(coordinator_id))
        associated_users.extend(self.create_attendees(attendees))
        return associated_users

    @abstractmethod
    def create_coordinator(self, coordinator_id: int):
        """
        Create coordinator attendee
        :param coordinator_id:
        :return:
        """
        pass

    @abstractmethod
    def create_attendees(self, attendees: list) -> list:
        """
        Create attendees
        :param attendees:
        :return:
        """
        pass


class BaseMeetingAttendees(MeetingAttendees, ABC):
    def create_attendees(self, attendees: list) -> list:
        meeting_users = list()
        user_service = UserFormService()
        for attendee in attendees:
            attendee_email = attendee.get('email', None)
            if attendee_email:
                user = user_service.find_model(pairs={'email': attendee_email})
                if user is None:
                    user = user_service.create_new_model(email=attendee_email,
                                                         is_activated=False)
                    user_service.session.commit()
                meeting_user = self._form_attendee(user_id=user.id,
                                                   is_accepted=attendee.get('is_accepted', False),
                                                   may_join=attendee.get('may_join', False))
                meeting_users.append(meeting_user)
        return meeting_users

    @abstractmethod
    def _form_attendee(self, user_id: int, is_accepted=False, may_join=False, is_coordinator=False):
        pass

    @abstractmethod
    def create_coordinator(self, coordinator_id: int):
        pass

from abc import ABC, abstractmethod

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.services.attendee_services import AttendeeFormService, MeetingUser
from .. import AttendeeAuthDecorator


class AttendeeConfirmDecorator(AttendeeAuthDecorator, ABC):
    def update_model(self, *args, **kwargs) -> bool:
        """
        Update is_accepted, may_join on MeetingUser table.
        :param args:
        :param kwargs:
        :return:
        """
        meeting_id = kwargs.get('meeting_id', 0)
        auth_user = self.get_authenticated_user()

        attendee_service = AttendeeFormService()
        attendee = attendee_service.get_meeting_user(meeting_id=meeting_id, user_id=auth_user.id)

        if isinstance(attendee, MeetingUser):
            attendee.note = kwargs.get('note', '')
            attendee = self._modify_attendee(attendee)
            if super().update_model(updated_model=attendee):
                self.commit()
                return True
        else:
            self.rollback()
            raise InvalidMeetingIdException()

    @abstractmethod
    def _modify_attendee(self, attendee: MeetingUser) -> MeetingUser:
        """
        Update MeetingUser model field based on updated confirm state.
        :param attendee: The MeetingUser that confirm to join the meeting.
        :return: Modified MeetingUser that ready to update.
        """
        pass

    @abstractmethod
    def get_email_status(self) -> str:
        pass

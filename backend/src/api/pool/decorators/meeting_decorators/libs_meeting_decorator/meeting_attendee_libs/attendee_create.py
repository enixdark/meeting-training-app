from src.database.postgres.meeting_user import MeetingUser
from . import BaseMeetingAttendees


class CreateMeetingAttendees(BaseMeetingAttendees):
    def _form_attendee(self, user_id: int, is_accepted=False, may_join=False, is_coordinator=False):
        """
        For create Meeting, create MeetingUser models.
        :param user_id:
        :param is_accepted:
        :param may_join:
        :param is_coordinator:
        :return: List of MeetingUser models.
        """
        meeting_user = MeetingUser()
        meeting_user.is_accepted = is_accepted
        meeting_user.is_response = may_join
        meeting_user.is_coordinator = is_coordinator
        meeting_user.user_id = user_id
        return meeting_user

    def create_coordinator(self, coordinator_id: int):
        """
        For create Meeting, create MeetingUser model.
        :param coordinator_id:
        :return: Coordinator MeetingUser model.
        """
        meeting_user = MeetingUser()
        meeting_user.is_coordinator = True
        meeting_user.is_accepted = 1
        meeting_user.user_id = coordinator_id
        return meeting_user

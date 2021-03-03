from . import BaseMeetingAttendees


class UpdateMeetingAttendees(BaseMeetingAttendees):
    def _form_attendee(self, user_id: int, is_accepted=False, may_join=False, is_coordinator=False):
        """
        Create MeetingUser dictionaries for update MeetingModel
        :param user_id:
        :param is_accepted:
        :param may_join:
        :param is_coordinator:
        :return:
        """
        meeting_user = dict()
        meeting_user['is_accepted'] = is_accepted
        meeting_user['may_join'] = may_join
        meeting_user['is_coordinator'] = is_coordinator
        meeting_user['user_id'] = user_id
        return meeting_user

    def create_coordinator(self, coordinator_id: int):
        """
        Create coordinator MeetingUser dictionary
        :param coordinator_id:
        :return:
        """
        meeting_user = dict()
        meeting_user['is_coordinator'] = True
        meeting_user['is_accepted'] = 1
        meeting_user['user_id'] = coordinator_id
        return meeting_user

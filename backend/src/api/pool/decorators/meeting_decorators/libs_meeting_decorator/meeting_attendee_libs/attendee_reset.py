from .attendee_update import UpdateMeetingAttendees


class ResetMeetingAttendees(UpdateMeetingAttendees):
    def _form_attendee(self, user_id: int, is_accepted=False, may_join=False, is_coordinator=False):
        """
        Reset all attendee dict field to False, because of reset meeting location or time
        :param user_id:
        :param is_accepted:
        :param may_join:
        :param is_coordinator:
        :return:
        """
        meeting_user = dict()
        meeting_user['is_accepted'] = False
        meeting_user['may_join'] = False
        meeting_user['is_coordinator'] = is_coordinator
        meeting_user['user_id'] = user_id
        return meeting_user


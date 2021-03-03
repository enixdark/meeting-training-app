from . import AttendeeConfirmDecorator, MeetingUser


class AttendeeAffirmativeDecorator(AttendeeConfirmDecorator):
    __AFFIRMATIVE_EMAIL_STATUS = 'xác nhận'

    def get_email_status(self) -> str:
        return self.__AFFIRMATIVE_EMAIL_STATUS

    def _modify_attendee(self, attendee: MeetingUser) -> MeetingUser:
        """
        If attendee is affirmative to join, set is_accepted and may_join to True
        :param attendee:
        :return:
        """
        attendee.is_accepted = True
        attendee.may_join = True
        attendee.is_response = True
        attendee.note = None
        return attendee

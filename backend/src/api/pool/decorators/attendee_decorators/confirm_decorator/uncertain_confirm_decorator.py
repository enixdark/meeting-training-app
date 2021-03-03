from . import AttendeeConfirmDecorator, MeetingUser


class AttendeeUncertainDecorator(AttendeeConfirmDecorator):
    __UNCERTAIN_EMAIL_STATUS = 'xác nhận có thể'

    def get_email_status(self) -> str:
        return self.__UNCERTAIN_EMAIL_STATUS

    def _modify_attendee(self, attendee: MeetingUser) -> MeetingUser:
        """
        If attendee is uncertain to join, set is_accepted to False and may_join to True
        :param attendee:
        :return:
        """
        attendee.is_accepted = False
        attendee.may_join = True
        attendee.is_response = True
        return attendee

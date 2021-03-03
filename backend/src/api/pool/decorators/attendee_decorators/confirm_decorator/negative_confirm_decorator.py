from . import AttendeeConfirmDecorator, MeetingUser


class AttendeeNegativeDecorator(AttendeeConfirmDecorator):
    __NEGATIVE_CONFIRM_STATUS = 'hủy xác nhận'

    def get_email_status(self) -> str:
        return self.__NEGATIVE_CONFIRM_STATUS

    def _modify_attendee(self, attendee: MeetingUser) -> MeetingUser:
        """
        If attendee is negative to join, set is_accepted and may_join to False
        :param attendee:
        :return:
        """
        attendee.is_accepted = False
        attendee.may_join = False
        attendee.is_response = True
        return attendee

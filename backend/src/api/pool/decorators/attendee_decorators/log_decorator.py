from src.api.pool.services.attendee_services import AttendeeFormService
from src.api.pool.decorators.attendee_decorators import AttendeeAuthDecorator


class AttendeeLogDecorator(AttendeeAuthDecorator):
    def get_all(self, *args, **kwargs):
        attendee_service = AttendeeFormService()
        auth_user = self.get_authenticated_user()

        # pop sort parameters, because we not sort MeetingUser, we sort Meeting from MeetingUser
        sort = kwargs.pop('sort', None)
        order = kwargs.pop('order', None)

        attendees = attendee_service.get_user_meetings(user_id=auth_user.id, **kwargs)

        sorted_attendees = [attendee.serialize(inclusion_rs=['meeting']) for attendee in attendees]
        sorted_attendees.sort(key=lambda n: n['meeting'][sort], reverse=self.__create_order(order))

        return sorted_attendees

    @staticmethod
    def __create_order(order: str) -> bool:
        if order == 'asc':
            return False
        return True

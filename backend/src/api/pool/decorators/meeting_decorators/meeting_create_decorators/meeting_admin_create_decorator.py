from src.api.pool.decorators.meeting_decorators import MeetingDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators import Model
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators.meeting_create_decorator import \
    MeetingCreateDecorator


class MeetingAdminCreateDecorator(MeetingDecorator):
    def _create_service(self) -> Service:
        """
        Create a non-periodic meeting (is_periodic is set to True).
        :return: New meeting
        """
        return MeetingCreateDecorator()

    def create_new_model(self, *args, **kwargs) -> Model:
        """
        Create non periodic meeting from admin. No need to approval
        :param args:
        :param kwargs:
        :return: New non-periodic meeting with state and is_approval equal to True
        """
        kwargs['state'] = True
        kwargs['is_approval'] = True

        return super(MeetingAdminCreateDecorator, self).create_new_model(*args, **kwargs)

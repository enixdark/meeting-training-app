from src.api.pool.decorators.meeting_decorators import MeetingDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_create_decorators import BaseCreateMeetingDecorator, Model


class MeetingCreateDecorator(MeetingDecorator):
    def _create_service(self) -> Service:
        """
        Create new meeting
        :return: New meeting
        """
        return BaseCreateMeetingDecorator()

    def create_new_model(self, *args, **kwargs) -> Model:
        """
        Create non periodic meeting
        :param args:
        :param kwargs:
        :return: New non periodic Meeting
        """
        kwargs['is_periodic'] = False
        return super(MeetingCreateDecorator, self).create_new_model(*args, **kwargs)

from src.api.pool.decorators.meeting_decorators.meeting_update_decorators import BaseUpdateMeetingDecorator


class CheckTimeUpdateDecorator(BaseUpdateMeetingDecorator):

    def _validate_updated_fields(self, meeting, *args, **kwargs) -> dict:
        """
        Always check meeting's time before update
        :param meeting:
        :param args:
        :param kwargs:
        :return:
        """
        kwargs = self._validate_time_fields(meeting, **kwargs)
        return kwargs

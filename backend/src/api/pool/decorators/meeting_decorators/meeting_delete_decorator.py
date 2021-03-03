from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    InvalidMeetingIdException
from src.api.pool.decorators.meeting_decorators import MeetingAuthDecorator


class MeetingDeleteDecorator(MeetingAuthDecorator):
    def update_model(self, *args, **kwargs) -> bool:
        meeting = self.get_model(_id=kwargs.get('_id', 0))
        if not meeting:
            raise InvalidMeetingIdException()
        kwargs.clear()
        kwargs['state'] = False
        return super(MeetingDeleteDecorator, self).update_model(updated_model=meeting, *kwargs)

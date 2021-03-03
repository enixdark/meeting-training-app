from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.check_time_update_decorator import \
    CheckTimeUpdateDecorator
from src.api.pool.services import Service
from . import BaseApprovalUpdateDecorator


class MeetingApprovalUpdateDecorator(BaseApprovalUpdateDecorator):
    def _set_approval_state(self, **kwargs) -> dict:
        kwargs['state'] = True
        kwargs['is_approval'] = True

        updated_meeting = self.get_model(_id=kwargs['_id'])
        if updated_meeting:
            # forbid approving on duplicated meeting by set started_time and finished_time to update kwargs
            kwargs['started_time'] = updated_meeting.started_time
            kwargs['finished_time'] = updated_meeting.finished_time
        return kwargs

    def _create_service(self) -> Service:
        return CheckTimeUpdateDecorator()
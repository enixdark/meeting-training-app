from abc import ABC, abstractmethod

from src.api.pool.decorators.celery_decorator import CeleryDecorator


class BaseCalendarApprovalUpdateDecorator(CeleryDecorator, ABC):
    def update_model(self, *args, **kwargs) -> bool:
        self._prepare_auth_service()
        updated = super(BaseCalendarApprovalUpdateDecorator, self).update_model(*args, **kwargs)

        if updated:
            meeting = self.get_model(_id=kwargs['_id'])
            auth_user = self.get_authenticated_user()
            self._add_calendar_task(meeting.id, auth_user.id)
            self._execute()
        return updated

    @abstractmethod
    def _add_calendar_task(self, meeting_id: int, auth_user_id: int):
        pass

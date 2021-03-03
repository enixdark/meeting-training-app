from abc import ABC, abstractmethod

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    MeetingCoordinatorPermissionException
from src.api.pool.decorators.meeting_decorators import MeetingAuthDecorator, Service
from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.meeting_update_decorator import \
    UpdateMeetingDecorator


class MeetingUpdateProxy(MeetingAuthDecorator, ABC):
    def _create_service(self) -> Service:
        return UpdateMeetingDecorator()

    def update_model(self, *args, **kwargs) -> bool:
        # check authorization to update
        if self._check_update_authorization(*args, **kwargs):
            return super(MeetingUpdateProxy, self).update_model(*args, **kwargs)
        else:
            raise MeetingCoordinatorPermissionException()

    @abstractmethod
    def _check_update_authorization(self, *args, **kwargs) -> bool:
        pass

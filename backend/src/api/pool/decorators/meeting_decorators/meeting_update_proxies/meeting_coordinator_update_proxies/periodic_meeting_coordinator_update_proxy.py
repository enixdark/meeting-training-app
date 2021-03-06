from src.api.pool.decorators.meeting_decorators.meeting_update_decorators.periodic_meeting_update_decorators.periodic_meeting_update_decorator import \
    PeriodicMeetingUpdateDecorator
from src.api.pool.services import Service
from . import BaseMeetingCoordinatorUpdateProxy


class PeriodicMeetingCoordinatorUpdateProxy(BaseMeetingCoordinatorUpdateProxy):
    def _create_service(self) -> Service:
        return PeriodicMeetingUpdateDecorator()

    def get_periodic_update_service(self) -> PeriodicMeetingUpdateDecorator:
        service = self._get_service()
        if isinstance(service, PeriodicMeetingUpdateDecorator):
            return service

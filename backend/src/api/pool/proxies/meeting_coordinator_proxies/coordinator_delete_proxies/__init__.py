from abc import ABC

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    MeetingCoordinatorPermissionException
from src.api.pool.proxies.meeting_coordinator_proxies import CoordinatorProxy


class CoordinatorDeleteProxy(CoordinatorProxy, ABC):
    def delete_model(self, *args, **kwargs) -> bool:
        if self._check_authorization(meeting_id=kwargs.get('_id')):
            return super(CoordinatorDeleteProxy, self).delete_model(*args, **kwargs)
        else:
            raise MeetingCoordinatorPermissionException()

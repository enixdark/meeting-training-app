from abc import ABC

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    MeetingCoordinatorPermissionException
from src.api.pool.proxies.admin_proxies import AdminProxy


class AdminDeleteProxy(AdminProxy, ABC):
    def delete_model(self, *args, **kwargs) -> bool:
        if self._check_authorization():
            return super(AdminDeleteProxy, self).delete_model(*args, **kwargs)
        else:
            raise MeetingCoordinatorPermissionException()
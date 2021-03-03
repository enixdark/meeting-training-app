from abc import ABC

from src.api.factory.exceptions.service_exceptions.db_service_exceptions.meeting_exceptions import \
    MeetingCoordinatorPermissionException
from src.api.pool.proxies.admin_proxies import AdminProxy
from src.database.postgres.base import Model


class AdminCreateProxy(AdminProxy, ABC):
    def create_new_model(self, *args, **kwargs) -> Model:
        if self._check_authorization():
            return super(AdminCreateProxy, self).create_new_model(*args, **kwargs)
        else:
            raise MeetingCoordinatorPermissionException()

from abc import ABC

from src.api.factory.exceptions.service_exceptions.authenticated_exceptions import UnauthenticatedServiceLoginException
from src.api.pool.services.user_services import UserFormService
from src.database.postgres.user import User
from . import BaseDecorator, Model


class AuthenticatedDecorator(BaseDecorator, ABC):
    def __init__(self):
        super().__init__()
        self._auth_user = None
        self.__user_service = UserFormService()

    def get_authenticated_user(self) -> User:
        """
        Get the user that uses this service. Retrieve data from Resource's authentication
        :return: User, raise Exception if self.__auth_user is None
        """
        if self._auth_user:
            return self._auth_user
        raise UnauthenticatedServiceLoginException()

    def set_authenticated_user(self, auth_user_id: dict):
        self._auth_user = self.__user_service.get_model(_id=auth_user_id)

    def _prepare_auth_service(self):
        """
        If decorator's delegated service is an instance of AuthenticatedDecorator, set auth_user for that service.
        :return:
        """
        service = self._get_service()
        if isinstance(service, AuthenticatedDecorator):
            service._auth_user = self._auth_user
            self.set_service(service)

    def update_model(self, *args, **kwargs) -> bool:
        self._prepare_auth_service()
        return super(AuthenticatedDecorator, self).update_model(*args, **kwargs)

    def create_new_model(self, *args, **kwargs) -> Model:
        self._prepare_auth_service()
        return super(AuthenticatedDecorator, self).create_new_model(*args, **kwargs)

    def delete_model(self, *args, **kwargs) -> bool:
        self._prepare_auth_service()
        return super(AuthenticatedDecorator, self).delete_model(*args, **kwargs)
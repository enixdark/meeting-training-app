from abc import abstractmethod, ABC

from src.api.pool.decorators.auth_decorator import AuthenticatedDecorator
from . import AuthenticatedResourceHelper
from .. import Resource, Request


class BaseAuthenticatedResource(Resource, ABC):
    def __init__(self):
        super().__init__()
        self.__authenticated_helper = AuthenticatedResourceHelper()

    @abstractmethod
    def _create_service(self) -> AuthenticatedDecorator:
        pass

    def _get_service(self) -> AuthenticatedDecorator:
        return self._service

    def _set_up_authenticate_service(self, request: Request):
        self._service = self.__authenticated_helper.set_authenticated_user(request, self._service)


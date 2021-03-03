from abc import abstractmethod, ABC

from src.api.pool.decorators.auth_decorator import AuthenticatedDecorator
from . import AuthenticatedResourceHelper
from ..form_resource import BaseFormResource, Request


class BaseAuthenticatedFormResource(BaseFormResource, ABC):
    def __init__(self):
        super().__init__()
        self.__authenticated_helper = AuthenticatedResourceHelper()

    @abstractmethod
    def _create_service(self) -> AuthenticatedDecorator:
        pass

    def _get_service(self) -> AuthenticatedDecorator:
        return self._service

    def get(self, request: Request, *args, **kwargs):
        self._set_up_authenticate_service(request=request)
        return super().get(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        self._set_up_authenticate_service(request=request)
        return super().post(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        self._set_up_authenticate_service(request=request)
        return super().patch(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        self._set_up_authenticate_service(request=request)
        return super().delete(request, *args, **kwargs)

    def _set_up_authenticate_service(self, request: Request):
        self._service = self.__authenticated_helper.set_authenticated_user(request, self._service)

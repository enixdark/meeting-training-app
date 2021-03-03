from src.api.pool.decorators import BaseDecorator, Service
from src.api.pool.services.user_services import UserFormService
from ..auth_decorator import AuthenticatedDecorator


class UserDecorator(BaseDecorator):
    def _create_service(self) -> Service:
        return UserFormService()

    def _get_service(self) -> UserFormService:
        return super()._get_service()


class UserAuthDecorator(AuthenticatedDecorator):
    def _create_service(self) -> Service:
        return UserFormService()

    def _get_service(self) -> UserFormService:
        return super()._get_service()

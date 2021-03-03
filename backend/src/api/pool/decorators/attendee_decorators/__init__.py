from src.api.pool.services import BaseService
from src.api.pool.services.attendee_services import AttendeeDecoratorService
from ..auth_decorator import AuthenticatedDecorator


class AttendeeAuthDecorator(AuthenticatedDecorator):
    def _create_service(self) -> BaseService:
        return AttendeeDecoratorService()

    def _get_service(self) -> AttendeeDecoratorService:
        return super()._get_service()
